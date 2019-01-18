#!/usr/bin/env python3

from memocv import MemoCV
from utils import get_pipe_model, print_pipe_model

import logging
from pprint import pformat
from math import ceil

import pandas as pd
import numpy as np
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix

def stratified_split(df):
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    for train_idx, test_idx in split.split(df, df.iloc[:, -1]):
        return df.iloc[train_idx], df.iloc[test_idx]

# uttlity to gen ngram
def ngram_grid(n, m):
    return [(i, j) for i in range(n, m + 1) \
                    for j in range(i, m + 1)]

def tokenizer(text):
    return text.split()

def evaluate(y, y_pred):
    total = len(y)
    accu = accuracy_score(y, y_pred)
    [p], [r], [f], [s] = precision_recall_fscore_support(y, y_pred, labels=[1])
    s /= total
    roc = roc_auc_score(y, y_pred)
    score = total, s, accu, p, r, f, roc
    logging.info('[EVAL]size %d, support %.3f, accuracy %.3f, precision %.3f, recall %.3f, fscore %.3f, roc %.3f' % score)
    #score_s = pd.Series(score, index=['Size', 'Support', 'Accuracy', 'Precision', 'Recall', 'F1'])
    return score

class VulnTrainer:
    algo_trainers = {
        "logistic":      "LogisticTrainer",
        "test":          "TestTrainer",
        "svm-linear":    "LinearSvcTrainer",
        "svm":           "SvcTrainer",
        "rnd-forest":    "RndForestTrainer",
        "decision-tree": "DecisionTreeTrainer",
        "knn":           "KnnTrainer",
        "gboost":        "GradientBoostingTrainer",
    }

    @classmethod
    def get_trainer(cls, algo, data, cv_iter_reduce=5):
        trainer = cls.algo_trainers.get(algo)
        if trainer is None:
            raise RuntimeError("unknown algorithm: " + algo)
        return globals()[trainer](data, cv_iter_reduce)

    @property
    def vul_name(self):
        return self.__data.columns[-1]

    @property
    def cv_iter_reduce(self):
        return self.__cv_iter_reduce

    # @data: DataFrame[X, y]
    def __init__(self, data, cv_iter_reduce=5):
        self.__data = data
        self.__cv_iter_reduce = cv_iter_reduce

    def _get_est_and_pmgrid(self):
        pass

    def param_n_inter(self, pmgrid):
        times = 1
        for key, value in pmgrid.items():
            if isinstance(value, list):
                times *= len(value)
        return times

    def __cross_valid(self, X, y):
        logging.info('Cross Validation')
        # train

        est, pmgrid = self._get_est_and_pmgrid()

        cv = MemoCV(estimator=est,
                    param_grid=pmgrid,
                    scoring='f1',
                    cv=5)
        cv.fit(X, y, self.vul_name)

        '''
        cv = RandomizedSearchCV(estimator=est,
                                param_distributions=pmgrid,
                                scoring='f1',
                                n_jobs=-1,
                                cv=5,
                                n_iter=ceil(self.param_n_inter(pmgrid) / self.cv_iter_reduce))
        cv.fit(X, y)
        '''
        clf = cv.best_estimator_

        #logging.info('[Train] Test %s: %.3f' % (cv.scoring, clf.score(X_test, y_test)))
        return clf

    def train(self):
        train, test = stratified_split(self.__data)

        X_train = train.iloc[:, 0].values
        y_train = train.iloc[:, 1].values
        X_test = test.iloc[:, 0].values
        y_test = test.iloc[:, 1].values

        self.clf_ = self.__cross_valid(X_train, y_train)
        logging.info('best clf:\n%s' % print_pipe_model(self.clf_))

        # predict
        #cross_val_predict(clf, X_train, y_train, cv=5)
        y_train_pred = self.clf_.predict(X_train)
        y_test_pred = self.clf_.predict(X_test)
        logging.info('data shape: %s' % X_test.shape)

        #confusion matrix
        self.confusion_matrix_ = confusion_matrix(y_test, y_test_pred)
        logging.info('confusion matrix:\n%s' % pformat(self.confusion_matrix_))

        # wrong prediction
        self.false_neg_ = test[(y_test == 1) & (y_test_pred == 0)]
        self.false_pos_ = test[(y_test == 0) & (y_test_pred == 1)]

        # evaluate
        self.train_score_ = evaluate(y_train, y_train_pred)
        self.test_score_ = evaluate(y_test, y_test_pred)

        # most importance features
        need_std = get_pipe_model(self.clf_, 'std') is None
        self.influence_ = self._get_influence_ft(self.clf_, X_train) if need_std else \
                          self._get_influence_ft(self.clf_)
        logging.info('Influence:\n%s\n...\n%s' % (self.influence_.head(), self.influence_.tail()))


    def _calc_std_influences(self, influences, ft_mat):
            ft_std = [np.std(ft_mat.getcol(i).toarray()) for i in range(ft_mat.shape[1]) ] 
            return [ inf * std for inf, std in zip(influences, ft_std) ]

    def _get_influence_ft(self, model, X=None):
        tfidf = get_pipe_model(model, 'tfidf')
        
        features = tfidf.get_feature_names()
        influences = self._get_influences(model)
        
        if len(features) != len(influences):
            return pd.DataFrame({'feature': features,
                                 'influence': np.zeros(len(features))
                                },
                                columns=['feature', 'influence'])
        
        if X is not None:
            influences = self._calc_std_influences(influences, tfidf.transform(X))

        df = pd.DataFrame({'feature': features,
                           'influence': influences
                          },
                          columns=['feature', 'influence'])

        df.sort_values(by='influence', ascending=False, inplace=True)
        return df

    def _get_influences(self, clf):
        pass
    
class TestTrainer(VulnTrainer):
    def _get_est_and_pmgrid(self):
        est =  Pipeline([('tfidf', TfidfVectorizer(strip_accents=None,
                                                    lowercase=False,
                                                    preprocessor=None,
                                                    stop_words=None, #const.STOP_WORDS,
                                                    tokenizer=tokenizer)),
                         ('std', StandardScaler(with_mean=False)),
                         ('logre', LogisticRegression(random_state=0))
                        ])
        pmgrid = {
                'tfidf__max_df': [0.5],
                'tfidf__ngram_range': [(1,1)],
                'logre__C': [10.0],
                'logre__penalty': ['l1']}

        return est, pmgrid

    def _get_influences(self, model):
        return get_pipe_model(model, 'logre').coef_[0]

class LogisticTrainer(VulnTrainer):
    def _get_est_and_pmgrid(self):
        est =  Pipeline([('tfidf', TfidfVectorizer(strip_accents=None,
                                                    lowercase=False,
                                                    preprocessor=None,
                                                    stop_words=None, #const.STOP_WORDS,
                                                    tokenizer=tokenizer)),
                         ('std', StandardScaler(with_mean=False)),
                         ('logre', LogisticRegression(random_state=0))
                        ])
        pmgrid = {
                'tfidf__max_df': [0.5, 0.7],
                'tfidf__ngram_range': [(1,1),(2,2),(3,3),(4,4),(5,5)],
                'logre__C': [10.0, 30.0, 100.0],
                'logre__penalty': ['l1', 'l2']}
        #'vect__stop_words': [stop, None],
        #'vect__tokenizer': [tokenizer, tokenizer_porter],
        #'vect__use_idf':[False],
        #'vect__norm':[None],

        return est, pmgrid

    def _get_influences(self, model):
        return get_pipe_model(model, 'logre').coef_[0]

class LinearSvcTrainer(VulnTrainer):
    def _get_est_and_pmgrid(self):
        est =  Pipeline([('tfidf', TfidfVectorizer(strip_accents=None,
                                                    lowercase=False,
                                                    preprocessor=None,
                                                    stop_words=None, #const.STOP_WORDS,
                                                    tokenizer=tokenizer)),
                         ('std', StandardScaler(with_mean=False)),
                         ('linear_svc', LinearSVC(loss="hinge")), ])

        pmgrid = {'tfidf__max_df': [0.5, 0.7],
                  'tfidf__ngram_range': [(1,1),(2,2),(3,3),(4,4),(5,5)],
                  'linear_svc__C': [0.1, 1.0, 10.0, 100.0]}
        '''
        pmgrid = {'tfidf__max_df': [0.5],
                  'tfidf__ngram_range': [(1,1)],
                  'linear_svc__C': [0.1]}
        '''

        return est, pmgrid

    def _get_influences(self, model):
        return get_pipe_model(model, -1).coef_[0]

class SvcTrainer(VulnTrainer):
    def _get_est_and_pmgrid(self):
        est =  Pipeline([('tfidf', TfidfVectorizer(strip_accents=None,
                                                    lowercase=False,
                                                    preprocessor=None,
                                                    stop_words=None, #const.STOP_WORDS,
                                                    tokenizer=tokenizer)),
                         ('std', StandardScaler(with_mean=False)),
                         ('svc', SVC(kernel="rbf"))
                        ])

        pmgrid = {'tfidf__max_df': [0.5, 0.7],
                  'tfidf__ngram_range': [(1,1),(2,2),(3,3),(4,4),(5,5)],
                  'svc__C': [0.1, 1.0, 10.0, 100.0],
                  'svc__gamma': [0.1, 1.0, 10.0] }

        return est, pmgrid

    def _get_influences(self, model):
        return []

class RndForestTrainer(VulnTrainer):
    def _get_est_and_pmgrid(self):
        est =  Pipeline([('tfidf', TfidfVectorizer(strip_accents=None,
                                                    lowercase=False,
                                                    preprocessor=None,
                                                    stop_words=None, #const.STOP_WORDS,
                                                    tokenizer=tokenizer)),
                         ('std', StandardScaler(with_mean=False)),
                         ('rf', RandomForestClassifier(n_estimators=500, n_jobs=-1, min_samples_leaf=4))
                        ])

        pmgrid = {'tfidf__max_df': [0.5, 0.7],
                  'tfidf__ngram_range': [(1,1),(2,2),(3,3),(4,4),(5,5)],}

        return est, pmgrid

    def _get_influences(self, model):
        return get_pipe_model(model, -1).feature_importances_

class DecisionTreeTrainer(VulnTrainer):
    def _get_est_and_pmgrid(self):
        est =  Pipeline([('tfidf', TfidfVectorizer(strip_accents=None,
                                                    lowercase=False,
                                                    preprocessor=None,
                                                    stop_words=None, #const.STOP_WORDS,
                                                    tokenizer=tokenizer)),
                         ('std', StandardScaler(with_mean=False)),
                         ('tree', DecisionTreeClassifier(min_samples_leaf=4))
                        ])

        pmgrid = {'tfidf__max_df': [0.5, 0.7],
                  'tfidf__ngram_range': [(1,1),(2,2),(3,3),(4,4),(5,5)],
                  'tree__criterion': ['gini', 'entropy'] }

        return est, pmgrid

    def _get_influences(self, model):
        return get_pipe_model(model, -1).feature_importances_

class KnnTrainer(VulnTrainer):
    def _get_est_and_pmgrid(self):
        est =  Pipeline([('tfidf', TfidfVectorizer(strip_accents=None,
                                                    lowercase=False,
                                                    preprocessor=None,
                                                    stop_words=None, #const.STOP_WORDS,
                                                    tokenizer=tokenizer)),
                         ('knn', KNeighborsClassifier()) ])

        pmgrid = {'tfidf__max_df': [0.5, 0.7],
                  'tfidf__ngram_range': [(1,1),(2,2),(3,3),(4,4),(5,5)],
                  'knn__n_neighbors': [5, 7, 9, 11] }

        return est, pmgrid

    def _get_influences(self, model):
        return []

class GradientBoostingTrainer(VulnTrainer):
    def _get_est_and_pmgrid(self):
        est =  Pipeline([('tfidf', TfidfVectorizer(strip_accents=None,
                                                    lowercase=False,
                                                    preprocessor=None,
                                                    stop_words=None, #const.STOP_WORDS,
                                                    tokenizer=tokenizer)),
                         ('std', StandardScaler(with_mean=False)),
                         ('gbc', GradientBoostingClassifier()) ])

        pmgrid = {'tfidf__max_df': [0.5, 0.7],
                  'tfidf__ngram_range': [(1,1),(2,2),(3,3),(4,4),(5,5)],
                  'gbc__n_estimators': [100, 250, 400] }

        return est, pmgrid

    def _get_influences(self, model):
        return get_pipe_model(model, -1).feature_importances_

def test_testtrainer():
    TEST_FILE = 'test-data.csv'
    vul = 'TOD'

    data = pd.read_csv(TEST_FILE, index_col=0) 
    data = data[['Opcodes', vul]]

    trainer = TestTrainer(data, 4)
    trainer.train()

    result = [vul,
            *trainer.train_score_,
            *trainer.confusion_matrix_.reshape(-1),
            *trainer.test_score_,
            *trainer.influence_.head(n=3).values.reshape(6)]


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
            format="%(asctime)s.%(msecs)03d [%(levelname)s] [%(module)s] %(message)s", datefmt="%H:%M:%S")

    test_testtrainer()
    
