#!/usr/bin/env python3
import os
import pandas as pd
import sklearn
from asm_parser import AsmParser
from utils import search_path
from sklearn.externals import joblib
from sklearn.pipeline import Pipeline
import keras
import word2vec
from keras.models import Sequential

ALL_VULS = ['Underflow','Overflow','Multisig','CallDepth','TOD','TimeDep','Reentrancy','AssertFail',
            'TxOrigin','CheckEffects','InlineAssembly','BlockTimestamp','LowlevelCalls','BlockHash','SelfDestruct']

def stem(op):
    return op.rstrip('0123456789') 

# TODO integrate ../feature/all-sol-to-opcodes.sh,
# because it should use THE SAME sol-to-opcode converter.
def sol_to_ops(solfile):
    parser = AsmParser(solfile)
    return [ op['name'] for op in parser.opcodes ]

def sol_to_data(sol):
    ops = [ stem(op) for op in sol_to_ops(sol) ]
    return pd.DataFrame({'Opcodes': [ ' '.join(ops) ]})


def f1(y_true, y_pred):
    from keras import backend as K

    def recall(y_true, y_pred):
        """Recall metric.

        Only computes a batch-wise average of recall.

        Computes the recall, a metric for multi-label classification of
        how many relevant items are selected.
        """
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall

    def precision(y_true, y_pred):
        """Precision metric.

        Only computes a batch-wise average of precision.

        Computes the precision, a metric for multi-label classification of
        how many selected items are relevant.
        """
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision
    precision = precision(y_true, y_pred)
    recall = recall(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

class ModelRepo:
    def __init__(self, repo_dir):
        self.__repo_dir = repo_dir
        self.__models = {}  #cache model ,prevent to load everytime

    def load(self, *keys):
        rel_path = os.path.join(*keys)

        model = self.__models.get(rel_path)  #relative path as key
        if model is None:
            model = self.__load(rel_path)
            self.__models[rel_path] = model
        return model

    def __load(self, rel_path):
        path_prefix = os.path.join(self.__repo_dir, rel_path)
        path, suffix = search_path(path_prefix)
        if path is None:
            return None

        if suffix == '.pkl.z' or suffix == '.pkl':
            return joblib.load(path)
        elif suffix == '.h5':
            return keras.models.load_model(path, custom_objects={'f1': f1})
        elif suffix == '.w2v.bin':
            return word2vec.load(path)
        else:
            raise Exception("unknown model type '%s' for '%s'" % (suffix, path))

    def save(self, model, *keys):
        rel_path = os.path.join(*keys)
        self.__models[rel_path] = model

        self.__save(model, rel_path)

    def __save(self, model, rel_path):
        if type(model) is sklearn.pipeline.Pipeline:
            suffix = '.pkl.z'
            func = joblib.dump
        elif type(model) is keras.models.Sequential:
            suffix = '.h5'
            func = lambda m, p: m.save(p)
        elif type(model) is word2vec.WordVectors:
            suffix = '.w2v.bin'
            func = None
        else:
            suffix = '.bin'
            func = joblib.dump

        path = os.path.join(self.__repo_dir, rel_path + suffix)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if func is not None:
            func(model, path)


def _get_vul_op_data(vulfile, ftfile):
    y_mapping = {'r': 1, 'o': 1, 'x': 0}

    data = pd.merge(
            left_index=True,
            left=pd.read_csv(vulfile, compression='xz', index_col=0).replace(y_mapping),
            right_index=True,
            right=pd.read_csv(ftfile, compression='xz', index_col=0),
            how='inner')
    print('data len: %d' % len(data))

    data.drop(columns='MD5', inplace=True)
    data.drop_duplicates(inplace=True)
    data.dropna(axis=0, how='any', inplace=True)
    print('data len: %d' % len(data))

    return data

# if cachefile is not None, using it to save/load data
def get_vul_op_data(vulfile, opfile, cachefile=None):

    has_cache = cachefile is not None and os.path.exists(cachefile)
    save_cache = cachefile is not None and not os.path.exists(cachefile)
    
    data = pd.read_csv(cachefile, index_col=0) if has_cache else \
           _get_vul_op_data(vulfile, opfile)

    if save_cache:
        data.to_csv(cachefile)

    return data

def print_prediction(vuls, preds, pred_fts=None):
    if preds.ndim == 1:
        preds.reshape(1, -1)

    vul_width = max([len(v) for v in vuls])

    for pred in preds:
        for vul, result in zip(vuls, pred):
            print('{0: <{1}} {2}'.format(vul, vul_width, result))

            # print decision features
            fts = pred_fts.get(vul, None)
            if fts is not None:
                print('\n'.join([ "  %.2f%%, %s" % (100*ratio, ft) for ratio, ft in fts ]))


__keepops = {
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

def is_stopop(w):
    return w not in __keepops

def main():
    def test_model_repo():
        repo = ModelRepo('.model')
        model = repo.load('knn', 'TOD')
        repo.save(model, 'my', 'test')
        model2 = repo.load('my', 'test')

    def test_model_repo_keras():
        repo = ModelRepo('.model')
        model = repo.load('w2v-cnn')
        repo.save(model, 'w2v-cnn-test')

    def test_search_op_seq():
        ops = sol_to_ops('../sc-src/0x0000000000b3F879cb30FE243b4Dfee438691c04.sol')
        p, q = search_seq(ops, 'SUB ADD ADD SHA3 SUB'.split(), is_stopop) 
        print(p, q)
        if 0 <= p < q:
            print(ops[p:q])


if __name__ == '__main__':
    main()
