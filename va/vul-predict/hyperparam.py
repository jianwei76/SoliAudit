from utils import split_dict

import os
import pandas as pd
import logging

class HyperparamKeeper:
    
    @property
    def df(self):
        self.__check_dirty()
        return self.__params
    
    @property
    def meta_cols(self): return self.__meta_cols
    @property
    def rec_cols(self): return self.__rec_cols
    @property
    def result_cols(self): return self.__result_cols

    #cols = ('data__label', 'data__size', 'vect__ngram_range', 'vect__max_df', 'clf__penalty', 'clf__C', 'cv__fold', 'cv__scoring', 'cv__score')    

    def __init__(self, filename, cols, convs=None, score_idx=-1):

        self.__meta_cols   = tuple(cols[0])
        self.__rec_cols    = tuple(cols[1])
        self.__result_cols = tuple(cols[2])
        cols = [*self.__meta_cols, *self.__rec_cols, *self.__result_cols]

        self.__score_idx = score_idx
        self.__fname = filename
        self.__params = pd.read_csv(self.__fname, index_col=0, converters=convs) if os.path.exists(self.__fname) else\
                        pd.DataFrame([], columns=cols)
        self.__dirty = False
        
    def __str__(self):
        return str(self.__params)
    
    def __check_dirty(self):
        if self.__dirty:
            self.__params.drop_duplicates(inplace=True)
            self.__dirty = False
    
    def __check_pm_name(self, pm, target=None):
        if target is None:
            target = self.__params.columns
        
        if len(pm) != len(target):
            logging.warning("The parameter name length '%d %s' is not match to %d %s" % (len(pm), pm, len(target), target))
            return False
        
        for name in pm:
            if name not in target:
                logging.warning("The parameter name '%s' is not allowed" % name)
                return False
        return True
    
    def __assert_pm_name(self, pm, target=None):
        if not self.__check_pm_name(pm, target):
            raise Exception('Not matched param columns')
            
    def __cond(self, pm):
        for i, (p, v) in enumerate(pm.items()):
            if i == 0:
                cond = (self.__params[p] == v)
            else:
                cond &= (self.__params[p] == v)
        return cond
        
    def __dup_params(self, pm):
        pm = pm.copy()
        for p in self.__result_cols:
            pm.pop(p, None)

        self.__assert_pm_name(pm, [*self.__meta_cols, *self.__rec_cols])   #no result cols
        return self.__params[self.__cond(pm)]

    
    def is_dup(self, pm):
        return not self.__dup_params(pm).empty

    
    def add(self, pm, ifdup='update'):
        self.__assert_pm_name(pm)
        self.__params.loc[len(self.__params)] = pm
        self.__dirty = True

    def save(self):
        self.__check_dirty()
        os.makedirs(os.path.dirname(self.__fname), exist_ok=True)
        self.__params.to_csv(self.__fname)
    
    # put new item and return (new) dict
    @staticmethod
    def __put(d, k, v, inplace=False):
        if not inplace:
            d = d.copy()
        d[k] = v
        return d

    # return the list of pm generated form meta[idx:]
    # @pm is a dict of paramter/value
    @classmethod
    def __gen(cls, meta, idx):
        if idx >= len(meta):
            return [{}]  # empty pm

        p, vals = meta[idx]

        # 'inplace' is not necessary, just for dict reuse
        return [ cls.__put(pm, p, v, inplace=(i==0)) \
                    for pm in cls.__gen(meta, idx + 1) \
                        for i, v in enumerate(vals) ]

    # @pm_rec: not 'score' and not 'meta'
    # return best score and its meta param
    def best_param(self, pm_temp):
        rec, _ = split_dict(pm_temp, self.__rec_cols)

        calidates = self.__params[self.__cond(rec)].iloc[:, self.__score_idx]
        if calidates.empty:
            return None, None
        best = dict(self.__params.iloc[calidates.idxmax()].items())
        
        meta, result, _ = split_dict(best, self.__meta_cols, self.__result_cols)

        #logging.info('best: %s, %s' % (meta, result))
        return meta, result
    
    # @pm_temp: parameter template: contain 'meta' (list) and 'rec' (normal), without 'score' column
    # flaten params and skim the duplicatd params, according to @pm_temp
    def gen_params(self, pm_temp, by='nodup'):
 
        # extract meta parameter from template
        meta, rec, _ = split_dict(pm_temp, self.__meta_cols, self.__rec_cols)
                
        def listify(pm):
            for p in meta:
                v = pm[p]
                pm[p] = [v]
            return pm
        
        metas = []
        for m in self.__gen(list(meta.items()), 0):            
            if not self.is_dup({**m, **rec}):
                metas.append(listify(m))
                
        return metas

        '''
        # a trivial version of __gen(meta,0) is like below, if len(meta) is fixed to 4:
        p1, p2, p3, p4 = meta                
        for v1 in pm_meta[p1]:
            for v2 in pm_meta[p2]:
                for v3 in pm_meta[p3]:
                    for v4 in pm_meta[p4]:
                        pm = {p1: v1, p2: v2, p3: v3, p4: v4}
        '''
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
            format="%(asctime)s.%(msecs)03d [%(levelname)s] [%(module)s] %(message)s", datefmt="%H:%M:%S")


    pm_grid = {
        'clf__C': [30.0],
        'clf__penalty': ['l1'],
        'vect__max_df': [0.5, 0.7],
        'vect__ngram_range': [(1,1), (2,2), (3, 3), (4,4), (5,5), (99,99)],
	}

    convs = {p:eval for p, v in pm_grid.items() if isinstance(v[0], tuple)}

    logging.info("hyperparameters:")
    cols = (sorted(pm_grid.keys()), ('task_name', 'data_size', 'cv_fold', 'cv_scoring'), ('score', 'std'))
    hyparams = HyperparamKeeper('.params-test', cols, convs)
    logging.info(hyparams.df)

    # add pseudo data ===================
    pm1 = {
        'task_name': 'TOD',
        'data_size': 14383,
        'cv_fold': 2,
        'cv_scoring': 'f1',
        'clf__C': 30.0,
        'clf__penalty': 'l1',
        'vect__max_df': 0.5,
        'vect__ngram_range': (1,1), 
        'score': 1.0,
        'std': 0.0
        }

    pm2 = {**pm1, 'vect__ngram_range': (2,2), 'score': 2.0}
    pm3 = {**pm1, 'vect__ngram_range': (3,3), 'score': 3.0}

    hyparams.add(pm1)
    hyparams.add(pm2)

    # test is dup ==================================
    logging.info('')
    for pm in (pm1, pm2, pm3):
        del pm['score']
        logging.info("is params dup: %s %s" % (hyparams.is_dup(pm), pm))

    # testing gen_params  ==================================
    pm_temp = { 
        'task_name': 'TOD',
        'data_size': 14383,
        'cv_fold': 2,
        'cv_scoring': 'f1',
        'clf__C': [30.0],
        'clf__penalty': ['l1'],
        'vect__max_df': [0.5],
        'vect__ngram_range': [(1,1), (2,2), (3,3), (4,4)] 
        }

    pms = [str(pm) for pm in hyparams.gen_params(pm_temp)]
    logging.info('')
    logging.info('\n  '.join(["Generated params: ", *pms]))

    # testing best score  ==================================
    best_pm, best_result = hyparams.best_param(pm_temp)
    logging.info('')
    logging.info("Best result: %s" %  best_result)
    logging.info("Best param: %s" %  best_pm)

