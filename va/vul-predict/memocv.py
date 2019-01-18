#!/usr/bin/env python3

from hyperparam import HyperparamKeeper
from utils import get_pipe_model
from utils import split_dict

import os
import logging
import sklearn
from pprint import pformat
from sklearn.model_selection import GridSearchCV
from sklearn.base import clone

# A CV wrapper, which remembers its historic tained hyperparameters
# The class uses GridSearchCV as underlying cv, and assumes estimator is Pipeline
class MemoCV:
    @property
    def scoring(self):
        return self.__cv_options['scoring']

    @property
    def fold(self):
        return self.__cv_options['cv']

    #@property
    #def best_estimator_(self):
    #    return self.best_estimator_

    def __init__(self, param_file=None, **cv_options):

        self.__cv_options = cv_options

        if param_file is None:
            param_name = '-'.join([name for name, _ in self.__cv_options['estimator'].steps])
            param_file = os.path.join('.param', param_name)

        pm_grid = self.__cv_options['param_grid']
        convs = {p:eval for p, v in pm_grid.items() if isinstance(v[0], tuple)}
        cols = (sorted(pm_grid.keys()), ('task_name', 'data_size', 'cv_fold', 'cv_scoring'), ('score', 'std'))

        self.__hyparams = HyperparamKeeper(param_file, cols, convs, score_idx=-2)


    def fit(self, X, y, task_name):
        self.best_estimator_ = self._fit(X, y, task_name)

    def _fit(self, X, y, task_name):
        
        # add cv info
        pm_temp = {
            'task_name': task_name,
            'data_size': len(X),
            'cv_fold':  self.__cv_options['cv'],
            'cv_scoring': self.__cv_options['scoring']
            }
        pm_temp.update(self.__cv_options['param_grid'])
        
        params = self.__hyparams.gen_params(pm_temp)

        if params:
            cv_options = {
                    'verbose': 1,
                    'n_jobs': -1,
                    'return_train_score': True}
            cv_options.update(self.__cv_options)
            cv_options['param_grid'] = params

            cv = GridSearchCV(**cv_options)
            cv.fit(X, y)

            #save hyperparameters 
            res = cv.cv_results_
            for pm, score, std in zip(res['params'], res['mean_test_score'], res['std_test_score']):
                pm = {**pm_temp, **pm}
                pm['score'] = score
                pm['std'] = std
                self.__hyparams.add(pm)
            self.__hyparams.save()
         
            # trained model
            cv_model = cv.best_estimator_
        else:
            cv_model = None
            logging.debug('All possbiles hyperparameters are trained: \n%s' % pformat(pm_temp))
        
        # get best params from @pm_temp    
        best_pm, result = self.__hyparams.best_param(pm_temp)
        logging.info('[MemoCV] CV(%s,%d), result: %s, Best parameter: \n%s' %
                (self.__cv_options['scoring'], self.__cv_options['cv'], result, pformat(best_pm)))
       
        # return the model from best params
        if cv_model is not None and split_dict(cv_model.get_params(), best_pm.keys())[0] == best_pm: # optimize for the lucky case
            return cv_model
        else:
            logging.info('[MemoCV] Instaniate model from the best param')
            model = clone(self.__cv_options['estimator'])
            model.set_params(**best_pm)
            model.fit(X, y)
            return model

# TODO Write Unit TEST!!!
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
            format="%(asctime)s.%(msecs)03d [%(levelname)s] [%(module)s] %(message)s", datefmt="%H:%M:%S")

    from sklearn.pipeline import Pipeline
    from sklearn.linear_model import LogisticRegression
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.preprocessing import StandardScaler
    from sklearn.svm import LinearSVC

    def tokenizer(text):
        return text.split()

    def get_estimator():
        vect = TfidfVectorizer(strip_accents=None,
                lowercase=False,
                preprocessor=None,
                stop_words=None, #const.STOP_WORDS,
                tokenizer=tokenizer)

        #clf = LogisticRegression(random_state=0)
        clf = LinearSVC(loss='hinge')
        
        return Pipeline([('test1', vect),
                         ('test2', StandardScaler(with_mean=False)),
                         ('test3', clf)])


    # get Data ======================================
    import pandas as pd
    from sklearn.model_selection import StratifiedShuffleSplit

    def stratifiedSplit(df, colname):
        split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
        for train_idx, test_idx in split.split(df, df[colname]):
            return df.iloc[train_idx], df.iloc[test_idx]

    def splitData(data, volname):
        #train_set, test_set = train_test_split(data, test_size=0.2, random_state=42)
        train_set, test_set = stratifiedSplit(data, volname)

        X_train = train_set['Opcodes'].values
        y_train = train_set[volname].values
        X_test = test_set['Opcodes'].values
        y_test = test_set[volname].values

        return X_train, y_train, X_test, y_test


    # main ========================


    __vulname = 'TOD'

    logging.info('[MemoCV] Loading Data...')
    data = pd.read_csv('data-cache.csv', index_col=0)
    X_train, y_train, X_test, y_test = splitData(data, __vulname)

    # Hyperparameters ========================================
    logging.info('[MemoCV] Traiing...')
    pm_grid = {
            'test3__C': [30.0],
            'test3__penalty': ['l2'],
            'test1__max_df': [0.7],
            'test1__ngram_range': [(1,1)]}
    #'vect__stop_words': [stop, None],
    #'vect__tokenizer': [tokenizer, tokenizer_porter],
    #'vect__use_idf':[False],
    #'vect__norm':[None],

    est = get_estimator()

    # Create CV ========================================
    logging.info('[MemoCV] Create CV')

    cv = MemoCV(
            #param_file='.param-test',
            estimator=est,
            param_grid=pm_grid,
            scoring='f1',
            cv=2)


    # traiing ========================================
    model = cv.fit(X_train, y_train, __vulname)

    # rsult
    logging.info('[MemoCV][%s] Test score: %.3f' % (cv.scoring, model.score(X_test, y_test)))


