#!/usr/bin/env python3

import op_word2vec
import trainer
from op_word2vec import op_name
from utils import set_logging
from common import get_vul_op_data, sol_to_data, ALL_VULS
from common import print_prediction
from common import ModelRepo
from common import f1

import os
import sys
import logging
from argparse import ArgumentParser
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.externals import joblib
from sklearn.metrics import confusion_matrix

import keras
from keras import backend as K
from keras import models
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D

def get_home_dir():
    return os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))

OP_CSV    = os.path.join(get_home_dir(), 'features/op.csv.xz')
MAX_OP_LEN = 13480

__model_repo = ModelRepo('.model')
W2V_BIN = '.model/evm-op.w2v.bin'
CNN_MOD_NAME = 'w2v-cnn'


def get_input_shape(img_shape):
    if K.image_data_format() == 'channels_first':
        return (1, *img_shape)
    else:
        return (*img_shape, 1)

def opline_to_vec(line, w2v):
    ops = line.split()
    vec = np.zeros((len(ops), w2v.vectors.shape[1]))
    for i, op in enumerate(ops):
        vec[i] = w2v.get_vector(op_name(op))
    return vec

def zero_pad_2d(arr, shape):
    result = np.zeros(shape)
    result[:arr.shape[0],:arr.shape[1]] = arr
    return result

def even(num):
    return int((num + 1) // 2 * 2)

def shuffle_split(x, y, test_ratio=0.2, random_state=42):
    train_size = int(len(x) * (1 - test_ratio))
    np.random.seed(random_state)
    permu = np.random.permutation(len(x))
    x_train, y_train = x[permu][:train_size], y[permu][:train_size]
    x_test , y_test  = x[permu][train_size:], y[permu][train_size:]
    return (x_train, y_train), (x_test, y_test)

# TODO nomalize
def prepare_x(data, max_op_len=None):
    op_word2vec.options(force=False, clean=True)
    w2v = op_word2vec.get_model(OP_CSV, W2V_BIN)

    op_vecs = [ opline_to_vec(row['Opcodes'], w2v) for idx, row in data.iterrows() ]

    if max_op_len is None:
        max_op_len = even(max([ op_vec.shape[0] for op_vec in op_vecs ]))
    w2v_size = w2v.vectors.shape[1]

    input_shape = (max_op_len, w2v_size)
    input_shape_ext = get_input_shape(input_shape)

    x = np.zeros((len(data), *input_shape_ext))
    for i in range(len(data)):
        x[i] = zero_pad_2d(op_vecs[i], input_shape).reshape(input_shape_ext)

    return x

def prepare_y(data):
    y = data.reset_index(drop=True).iloc[:, :-1].values
    return y

def gen_model(in_shape, num_classes):
    model = Sequential()
    model.add(Conv2D(256, kernel_size=(3, 3),
                     activation='relu',
                     padding='same',
                     input_shape=in_shape, name='Cov1'))
    model.add(Conv2D(512, (3, 3), padding='same', activation='relu', name='Cov2'))
    model.add(MaxPooling2D(pool_size=(2, 2), data_format='channels_last', name='MaxPool'))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='sigmoid', name='DenseOut'))

    '''
    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])
    '''
    model.compile(loss=keras.losses.binary_crossentropy,
            optimizer=keras.optimizers.RMSprop(lr=1e-4),
            metrics=[f1])
    
    return model

# TODO 1. uisng k-fold cross-validation
#      2. get best model based on the scores from epoch history 
def train_model(train_test_data, batch_size=128, epochs=50):
    (x_train, y_train), (x_test, y_test) = train_test_data

    input_shape = x_train.shape[1:]
    num_classes = y_train.shape[1]

    logging.info('train size: %d, test size: %d' % (len(x_train), len(x_test)))
    logging.info('input shape: %s, output num of classes: %d' % (input_shape, num_classes))

    K.set_image_dim_ordering('th')
    model = gen_model(input_shape, num_classes)
    model.summary()
    model.fit(x_train, y_train,
            batch_size=batch_size,
            epochs=epochs,
            verbose=1,
            validation_data=(x_test, y_test))  #TODO should not use the test set.

    score = model.evaluate(x_test, y_test, verbose=0)
    print('score: %s' % score)

    return model

def train(data, model_name=CNN_MOD_NAME, epochs=100):
    x = prepare_x(data)
    y = prepare_y(data)
    train_test_data = shuffle_split(x, y, 0.2)

    model = train_model(train_test_data, epochs=epochs)
    __model_repo.save(model, model_name)

    results = train_results(model, train_test_data)
    return results


def train_results(model, train_test_data):
    results = pd.DataFrame({}, columns=[
        'train_size', 'train_support', 'train_accuracy', 'train_precision', 'train_recall', 'train_f1', 'train_roc',
        'TrueNeg', 'FalsePos', 'FalseNeg', 'TruePos',
        'size', 'support', 'accuracy', 'precision', 'recall', 'f1', 'roc',
        'top_ft_1', 'top_inf_1', 'top_ft_2', 'top_inf_2','top_ft_3', 'top_inf_3'])

    (x_train, y_train), (x_test, y_test) = train_test_data
    y_train_pred = model_predict(model, x_train)
    y_test_pred = model_predict(model, x_test)

    for i, vul in enumerate(ALL_VULS):
        try:
            train_score_ = trainer.evaluate(y_train[:,i], y_train_pred[:,i])
            test_score_ = trainer.evaluate(y_test[:,i], y_test_pred[:,i])
            confusion_matrix_ = confusion_matrix(y_test[:,i], y_test_pred[:,i])
            influence_ = np.array([['', 0],
                                   ['', 0],
                                   ['', 0]])
            result = [ *train_score_,
                       *confusion_matrix_.reshape(-1),
                       *test_score_,
                       *influence_.reshape(6)]

            results.loc[vul] = result

        except Exception as ex:
            print(vul, '\terror: %s' % ex)

    return results
	

def model_predict(model, x, vuls=None):
    y = (model.predict(x) >= 0.5).astype('int8')
    idxes = [ ALL_VULS.index(vul) for vul in vuls ]
    return y[:, idxes]


def predict(data, vuls):
    logging.debug('preparing data...')
    x = prepare_x(data, MAX_OP_LEN)

    logging.debug('loading cnn model...')
    model = __model_repo.load(CNN_MOD_NAME)

    logging.debug('predicting data...')
    return model_predict(model, x, vuls)


def init_arguments():
    parser = ArgumentParser(description='smart contract vulnerability analyzer')
    parser.add_argument('subcmd', action='store', help="sub-command: < merge | train | predict >", default='train')
    parser.add_argument("-v", "--verbose",  action="count", default=0, help="increse detail information")
    parser.add_argument("-q", "--quiet",  action="count", default=0, help="decrese detail information")
    parser.add_argument("-s", "--sol", action="store", default=None, help="Solidity file")
    parser.add_argument("-d", "--datafile", action="store", default=None, help="Data file to train")
    parser.add_argument('-u', '--vulfile', action='store', default=None, help="vunlerability data")
    parser.add_argument('-o', '--opfile', action='store', default=None, help="feature data")
    return parser.parse_args()

def main():
    args = init_arguments()
    set_logging(args.verbose - args.quiet)

    def file_exists(path):
        return path and os.path.exists(path)

    if args.subcmd == 'train':
        if not file_exists(args.datafile) and not (file_exists(args.vulfile) and file_exists(args.opfile)):
            logging.error("Need to specify the data file or vul/op files to read.")
            logging.error(" For example: %s train -d %s [ -u %s -o %s ]" % 
                    (sys.argv[0], 'data.csv', '../run-anlyzers/vuls.csv.xz', '../features/op-ft.csv.xz'))
            sys.exit(1)

        logging.info('training...')
        data = get_vul_op_data(args.vulfile, args.opfile, args.datafile)
        train(data)

    elif args.subcmd == 'predict':
        if file_exists(args.sol):
            logging.error("No solidty file")
            sys.exit(1)

        logging.info('predicting...')
        vuls = ALL_VULS
        data = sol_to_data(args.sol)

        preds = predict(data, vuls)
        print_prediction(vuls, preds)

    else:
        logging.error("unknown command '%s'" % args.subcmd)
        sys.exit(1)

if __name__ == '__main__':
    main()
