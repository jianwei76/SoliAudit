#!/usr/bin/env python3

from argparse import ArgumentParser
from utils import set_logging
from trainer import VulnTrainer

def init_arguments():
    parser = ArgumentParser(description='smart contract vulnerability analyzer')
    parser.add_argument('subcmd', action='store', help="sub-command: < merge | train | predict >",)
    parser.add_argument('-a', '--algo', action='store', default="logistic",
            help="specified the algorithm to train or predict: < " + " | ".join(VulnTrainer.algo_trainers.keys()) + " >")
    parser.add_argument("-v", "--verbose",  action="count", default=0, help="increse detail information")
    parser.add_argument("-q", "--quiet",  action="count", default=0, help="decrese detail information")
    parser.add_argument("-f", "--force", action="store_true", default=False, help="force to reload data")
    parser.add_argument("-s", "--sol", action="store", default=False, help="Solidity file")
    parser.add_argument("-t", "--targets", action="append", default=None, help="target vulnerability to train / predict")
    parser.add_argument("-d", "--datafile", action="store", default=None, help="Data file to train")
    parser.add_argument('-u', '--vulfile', action='store', default=None, help="vunlerability data")
    parser.add_argument('-o', '--opfile', action='store', default=None, help="feature data")
    parser.add_argument("-p", "--print-stat", action="store_true", default=False, help="pirnt statistics info")
    parser.add_argument("-z", "--fuzz-match", action="store_true", default=False, help="fuzz to match theopcode seqence")
    return parser.parse_args()

Args = init_arguments()
set_logging(Args.verbose - Args.quiet)

#import const
import w2v_cnn
from trainer import TestTrainer, LogisticTrainer, LinearSvcTrainer, SvcTrainer, RndForestTrainer, DecisionTreeTrainer, KnnTrainer, GradientBoostingTrainer
from common import get_vul_op_data, ALL_VULS
from common import stem, sol_to_ops, sol_to_data
#from common import print_prediction
from common import ModelRepo
from utils import get_pipe_model
from utils import get_pipe_transform
from asm_parser import AsmParser
from loc2linepos import loc_to_linepos
import os
import sys
import logging
import time
from itertools import chain
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter
from datetime import datetime

__basedir = os.path.dirname(os.path.abspath(__file__));

_ModelRepo = ModelRepo(os.path.join(__basedir, '.model'))

__keepwords = {
    'ADD',
    'SUB',
    'SHA3',
    'ADDRESS',
    'BALANCE',
    'ORIGIN',
    'CALLER',
    'CALLVALUE',
    'CALLDATALOAD',
    'CALLDATASIZE',
    'CALLDATACOPY',
    'CODESIZE',
    'CODECOPY',
    'GASPRICE',
    'EXTCODESIZE',
    'EXTCODECOPY',
    'BLOCKHASH',
    'COINBASE',
    'TIMESTAMP',
    'NUMBER',
    'DIFFICULTY',
    'GASLIMIT',
    'GAS',
    'CREATE',
    'CALL',
    'CALLCODE',
    'RETURN',
    'DELEGATECALL',
    'SELFDESTRUCT',
    'REVERT'
}

__reduced_keepwords = set(__keepwords)
__reduced_keepwords.remove('ADD')
__reduced_keepwords.remove('SUB')

def is_stopword(w):
    return w not in __keepwords

def is_reduced_stopword(w):
    return w not in __reduced_keepwords

'''
def set_reduced_ops(data):
    data['ReducedOpcodes'] = data['Opcodes'].apply(lambda ops: remove_ops(ops, {'ADD', 'SUB'}))
    return data

def remove_ops(opseq, removed_ops):
    ops = [ op for op in opseq.split() if op not in removed_ops ]
    return ' '.join(ops)
'''

def stem_data(data):
    def _stemming(opseql):
        ops = [ stem(op) for op in opseql.split() ]
        return ' '.join(ops)
    data['Opcodes'] = data['Opcodes'].apply(_stemming)


def train_vul(data, algo, vul):
    logging.info("Training '%s' ===================" % vul)

    if (data[vul] == 1).sum() < 2:    #no enough sample to be grouped and train
        return None

    trainer = VulnTrainer.get_trainer(algo, data, 4)
    trainer.train()

    _ModelRepo.save(trainer.clf_, algo, vul)

    result = [ *trainer.train_score_,
               *trainer.confusion_matrix_.reshape(-1),
               *trainer.test_score_,
               *trainer.influence_.head(n=3).values.reshape(6)]

    # qucik to run predict
    #test_predit(trainer.clf_, vul)

    return result

def ml_train(data, algo, vuls):
    assert data.columns[-1] == 'Opcodes'

    results = pd.DataFrame({}, columns=[
        'train_size', 'train_support', 'train_accuracy', 'train_precision', 'train_recall', 'train_f1', 'train_roc',
        'TrueNeg', 'FalsePos', 'FalseNeg', 'TruePos',
        'size', 'support', 'accuracy', 'precision', 'recall', 'f1', 'roc',
        'top_ft_1', 'top_inf_1', 'top_ft_2', 'top_inf_2','top_ft_3', 'top_inf_3'])

    #set_reduced_ops(data)
    
    for vul in vuls:
        #train_data = data[['Opcodes', vul]] if vul in {'Underflow', 'Overflow'} else \
        #             data[['ReducedOpcodes', vul]]
        #train_data = train_data.drop_duplicates()
        train_data = data[['Opcodes', vul]]

        result = train_vul(train_data, algo, vul)
        if result is not None:
            results.loc[vul] = result

    return results

def to_train(data, algo, vuls):
    stem_data(data)

    results = w2v_cnn.train(data, vuls) if algo == 'cnn' else \
              ml_train(data, algo, vuls)

    path = 'results/%s.%s.csv' % (time.strftime('%m%d-%H%M'), algo)
    logging.info('saving results to %s' % path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    results.to_csv(path)


def get_decision_features(clf, x):
    tfidf = get_pipe_model(clf, 'tfidf')
    logre = get_pipe_model(clf, 'logre')

    # weights of features
    x_trans = get_pipe_transform(clf, x).toarray().reshape(-1)
    coef = logre.coef_.reshape(-1)
    weights = [ (i, v*w) for i, v, w in zip(range(len(x_trans)), x_trans, coef) if v and w ]
    weights = sorted(weights, key=itemgetter(1), reverse=True)

    # trim non-contributing weights
    y = logre.intercept_[0]
    for i, (_, w) in enumerate(weights):
        if y > 0:   # the smaple has became positive
            break
        y += w
    weights = weights[:i]

    # contributing features and weight ratio
    features = tfidf.get_feature_names()
    w_sum = sum([w for _, w in weights])
    decision_fts = [ (w/w_sum, features[i] ) for i, w in weights ]    
    return decision_fts


def predict_vul(data, algo, vul, clf=None):
    if clf is None:
        clf = _ModelRepo.load(algo, vul)

    if clf is None:
        return 0, []
    else:
        x = data.values
        y = clf.predict(x)
        logging.info("%s: %s" % (vul, y))

        fts = get_decision_features(clf, x) if algo == 'logistic' and y else \
              []
        return y, fts

def ml_predict(data, algo, vuls):
    #set_reduced_ops(data)
    assert data.columns[-1] == 'Opcodes'

    shape = len(data), len(ALL_VULS)
    preds = np.zeros(shape).astype('int8')

    # TODO support len(data) >= 2
    pred_fts = {}

    for i, vul in enumerate(vuls):
        #pred_data = data['Opcodes'] if vul in {'Underflow', 'Overflow'} else \
        #            data['ReducedOpcodes']
        pred_data = data['Opcodes']

        pred, fts = predict_vul(pred_data, algo, vul)
        preds[:, i] = pred
        pred_fts[vul] = fts

    return preds, pred_fts

# TODO create result record for each vulnerability examine result
class VulResult:
    pass

class OpLoc:
    @property
    def solfile(self):
        return self.__solfile

    @property
    def opseq(self):
        return self.__opseq

    @property
    def nline(self):
        return self.__nline

    @property
    def npos(self):
        return self.__npos

    @property
    def msg(self):
        return self.__msg

    def __init__(self, solfile, opseq, nline, npos, msg):
        self.__solfile = solfile
        self.__opseq = opseq
        self.__nline = nline
        self.__npos = npos
        self.__msg = msg

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        eq = isinstance(other, self.__class__) \
                and self.solfile == other.solfile \
                and self.opseq == other.opseq \
                and self.nline == other.nline \
                and self.npos == other.npos \
                and self.msg == other.msg
        return eq

    def __hash__(self):
        return hash((self.solfile, self.opseq, self.nline, self.npos, self.msg))

    def __str__(self):
        return "{}:{}:{}:{}:{}".format(self.solfile, self.nline, self.npos, self.msg, self.opseq)

# input:
#    @solfile: sol file path
#    @opseq: stopword timmed opseq
# A @opseq will map to multi original opseq;
# A original opseq should map to a location.
class VulOp:
    @property
    def solfile(self):
        return self.__parser.solfile

    @property
    def ratio(self):
        return self.__ratio

    @property
    def contri_opseq(self):
        return self.__contri_opseq

    @property
    def origin_opseq_locs(self):
        return self.__origin_opseq_locs

    def __init__(self, parser, contri_opseq, to_skip=None):
        self.__parser = parser
        self.__ratio, self.__contri_opseq = contri_opseq
        self.__to_skip = to_skip
        self.__origin_opseq_locs = [ loc for opseq in self.__get_origin_opseqs() \
                                        for loc in self.__origin_opseq_to_locs(opseq) ]
        
    def __origin_opseq_to_locs(self, opseq):
        locs = self.__find_opseq_locs(opseq.split())
        if not locs:
            return [ OpLoc(self.solfile, opseq, 0, 0, '') ]
        else:
            return [ OpLoc(self.solfile, opseq, nline, npos, msg) for nline, npos, msg in locs ]

    def __get_origin_opseqs(self):
        #sol_ops = sol_to_ops(self.solfile)
        #stopword_trimmed_ops = 

        contri_ops = self.__contri_opseq.split()
        op_eql = lambda op1, op2: stem(op1) == stem(op2)

        opseqs = set()
        begin, end = -1, -1
        while True:
            # find subsequence
            begin ,end = self.__parser.find(contri_ops, op_eql=op_eql, begin=begin+1)
            #begin, end = find_seq(sol_ops, stopword_trimmed_ops, to_skip=self.__to_skip, begin=begin+1)
            if not (0 <= begin < end):
                break
            matched_ops = self.__parser.get_ops(begin, end)

            # truncate trailing opcodes
            #s, t = find_seq(opseq, ('STOP', 'LOG1', 'PUSH6', 'SHA3'))
            #if 0 <= s < t:
            #    opseq = opseq[:s]

            if matched_ops:
                opseqs.add(' '.join(matched_ops))  # avoid that opseql is unhashable

        #for opseq in opseqs:
        #    logging.debug('...get original opseq: {}'.format(opseq))
        return opseqs

    '''
    Find location of the opcode sequence.
        @opseqs: the list of opcodes
    '''
    def __find_opseq_locs(self, opseq):
        logging.debug("Finding locations for opseq '%s')" % (' '.join(opseq)))

        locs = set()
        begin, end = -1, -1
        while True:
            #begin, end = self.__parser.find('OPCODE', opseq, begin+1)
            begin, end = self.__find_opseq_loc(opseq, begin+1, match_min=min(5, len(opseq)//2), try_dec=True) if Args.fuzz_match else \
                         self.__find_opseq_loc(opseq, begin+1)
            if not (0 <= begin < end):
                break
            logging.debug("Found opseq located between [%d, %d)" % (begin, end))

            # get opcode sequces
            first_op = self.__parser.opcodes[begin]
            locs.add((first_op['begin'], first_op['end']))  # diff locations of opseql may map to the same locations of src code

        return [ self.__to_sol_loc(begin, end) for begin, end in locs ]

    def __to_sol_loc(self, begin, end):
        nline, npos = loc_to_linepos(self.__parser.solbytes, begin)
        text = self.__parser.solbytes[begin:end].decode('utf8')
        logging.debug("opseq between [%d, %d) to location %d, %d: %s" % (begin, end, nline, npos, text))
        return nline, npos, text

    '''
    @try_dec: decrement opseq if no match found
    '''
    def __find_opseq_loc(self, opseq, from_, match_min=1.0, try_dec=False):
        if isinstance(match_min, float):
            match_min = int(match_min * len(opseq))

        while True:
            begin, end = self.__parser.find(opseq, from_)
            if 0 <= begin < end:
                return begin, end
            elif try_dec and len(opseq) > match_min:
                opseq = opseq[:-1]
            else:
                return -1, -1


class PredictResult:
    @property
    def vuls(self):
        return self.__vuls

    def __init__(self, solfile, vuls, pred_vals, contri_opseqs):
        self.__solfile = solfile
        self.__vuls = vuls
        self.__pred_vals = pred_vals

        self.__vul_ops = {}
        parser = AsmParser(solfile)
        for vul, opseqs in contri_opseqs.items():
            #to_skip = is_stopword if vul in {'Underflow', 'Overflow'} else is_reduced_stopword
            self.__vul_ops[vul] = [ VulOp(parser, opseq) for opseq in opseqs ]

    def is_vulnerable(self, vul):
        return self.__pred_vals[self.__vuls.index(vul)] != 0

    def gte_vul_ops(self, vul):
        return self.__vul_ops.get(vul, [])

def print_stat(txt):
    print("STAT | %s" % txt)

def print_pred_result(result):
    #vul_width = max([len(v) for v in result.vuls])
    print('# Vulnerability Analysis #')
    print('#### %s ####' % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print('')

    for vul in result.vuls:
        print('* {} {}'.format('_`X`_' if result.is_vulnerable(vul) else '__O__', vul))

        for vul_op in result.gte_vul_ops(vul):
            print("{:{}}- {:.0%}, {}".format('', 4, vul_op.ratio, vul_op.contri_opseq))

            # using Set to filter the same location even from different opcode sequence
            locs = sorted({ (loc.nline, loc.npos, loc.msg) for loc in vul_op.origin_opseq_locs }, key=itemgetter(0,1))
            if locs:
                print('')
                for loc in locs:
                    print("{:{}}- Line {}, {} ``{}``".format('', 8, *loc))
                print('')

def to_predict(sol, algo, vuls):
    try:
        logging.info("\nAnalyzing solidity file '{}'".format(sol))
    
        data = sol_to_data(sol)
        logging.debug(data['Opcodes'][0])
        
        if algo == 'cnn':
            pred = w2v_cnn.predict(data, vuls)
            pred_fts = {}
        else:
            pred, pred_fts = ml_predict(data, algo, vuls)
        pred = pred.reshape(-1).tolist()

        result = PredictResult(sol, vuls, pred, pred_fts)
        print_pred_result(result)

        '''
        if Args.print_stat:
            stat = [os.path.basename(sol)] + [str(v) for v in pred]
            print_stat(", ".join(stat))
        '''
    except Exception as ex:
        logging.error("analyzing '{}' error: {}".format(sol, ex))

def to_test_predict(algo):
    dir = '../sc-src'
    for f in os.listdir(dir):
        if not f.endswith('.sol'):
            continue

        logging.info(f)
        f = os.path.join(dir, f)
        try:
            data = sol_to_data(f)
            ml_predict(data, algo)
        except Exception as ex:
            logging.error("predict '%s' error: '%s'" % (f, ex))


def scan_sol(dir):
    sols = [ent.path for ent in os.scandir(dir) if ent.is_file() and ent.name.endswith('.sol') ]
    sols.sort()
    return sols

def file_exists(path):
    return path and os.path.exists(path)

def get_target_vuls():
    if Args.targets:
        diff = set(Args.targets) - set(ALL_VULS)
        if diff:
            raise ValueError("undefined vulnerability '%s'" % diff)
        return Args.targets
    else:
        return ALL_VULS

def main():
    if Args.subcmd == 'train':
        if not file_exists(Args.datafile) and not (file_exists(Args.vulfile) and file_exists(Args.opfile)):
            logging.error("Need to specify the data file or vul/op files to read.")
            logging.error(" For example: %s train -d %s [ -u %s -o %s ]" % 
                    (sys.argv[0], 'data.csv', '../run-anlyzers/vuls.csv.xz', '../features/op.csv.xz'))
            sys.exit(1)

        data = get_vul_op_data(Args.vulfile, Args.opfile, Args.datafile)
        vuls = get_target_vuls()
        to_train(data, Args.algo, vuls)

    elif Args.subcmd == 'predict':
        if not Args.sol:
            logging.error("No solidty file")
            sys.exit(1)

        vuls = get_target_vuls()
        if os.path.isdir(Args.sol):
            if Args.print_stat:
                print_stat(", ".join(['Addr'] + vuls))
            for sol in scan_sol(Args.sol):
                to_predict(sol, Args.algo, vuls)
        else:
            to_predict(Args.sol, Args.algo, vuls)

    elif Args.subcmd == 'test-train-cnn':
        data = get_vul_op_data(None, None, 'data.csv')
        results = w2v_cnn.train(data, 'w2v-cnn-test', 1)
        results.to_csv('results/%s.%s.csv' % (time.strftime('%m%d-%H%M'), 'cnn'))

    elif Args.subcmd == 'test':
        to_test_predict(Args.algo)

    else:
        logging.error("unknown command '%s'" % Args.subcmd)
        sys.exit(1)

if __name__ == '__main__':
    main()
