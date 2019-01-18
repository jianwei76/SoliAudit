#!/usr/bin/env python3

import os
import logging
import numpy as np

def sigmoid(x, derivative=False):
    return x*(1-x) if derivative else 1/(1+np.exp(-x))

def _get_pipe_model_name(pipe, name):
    for n, m in pipe.steps:
        if n == name:
            return m
    return None

def _get_pipe_model_idx(pipe, idx):
    return pipe.steps[idx][1]

def get_pipe_model(pipe, indicator):
    return _get_pipe_model_idx(pipe, indicator) if isinstance(indicator, int) else \
           _get_pipe_model_name(pipe, indicator)

def get_pipe_transform(pipe, x):
    for name, model in pipe.steps[:-1]:
        x = model.transform(x)
    return x


def print_pipe_model(model):
    if model is None:
        return None

    str = ''
    for step in model.steps:
        str += "%s: %s\n" % step;
    return str;


def which_set(sets, k):
    nset = len(sets)
    for i in range(nset):
        if k in sets[i]:
            return i
    return nset

def split_dict(d, *key_sets):
    ret = [{} for _ in range(len(key_sets) + 1)]
    
    for k, v in d.items():
        ret[which_set(key_sets, k)][k] = v
    
    return ret

# search file with its path matching @path_prefix
# if more than one candicate, throw exception
# return:
#    path, suffix
def search_path(path_prefix):
    if os.path.exists(path_prefix):
        return path_prefix, ''

    dir = os.path.dirname(path_prefix)
    prefix = os.path.basename(path_prefix)

    candicates = [f for f in os.listdir(dir) if f.startswith(prefix) ]
    if len(candicates) > 1:
        raise Exception("more than one file under '%s' with filename prefix '%s'" % (dir, prefix))
    elif len(candicates) == 0:
        return None, None
    else:
        path = os.path.join(dir, candicates[0])
        suffix = candicates[0][len(prefix):]
        return path, suffix

# return matched range [begin, end)
def find_seq(seq, subseq, is_eql=None, to_skip=None, begin=0, end=None):
    if to_skip is None:
        to_skip = lambda item: False

    if is_eql is None:
        is_eql = lambda x1, x2: x1 == x2

    if end is None:
        end = len(seq)

    len_subseq = len(subseq)

    for idx in range(begin, end):
        p, q = idx, 0
        while p < end and q < len_subseq:
            if p != idx and to_skip(seq[p]):  #skip stopword if not the frist.
                p += 1
            elif not is_eql(seq[p], subseq[q]):
                break
            else:
                p, q = p+1, q+1

        if q == len_subseq:
            return idx, p

    return -1, -1;

def rfind_seq(seq, subseq, is_eql=None, to_skip=None, begin=0, end=None):
    if to_skip is None:
        to_skip = lambda item: False

    if is_eql is None:
        is_eql = lambda x1, x2: x1 == x2

    if end is None:
        end = len(seq)

    len_subseq = len(subseq)

    for idx in range(end-1, begin-1, -1):
        p, q = idx, len_subseq -1
        while p >= 0 and q >= 0:
            if p != idx and to_skip(seq[p]):  #skip stopword if not the frist.
                p -= 1
            elif not is_eql(seq[p], subseq[q]):
                break
            else:
                p, q = p-1, q-1

        if q == -1:
            return p+1, idx+1

    return -1, -1;

def set_logging(verbose=0):
    log_level = logging.DEBUG   if verbose >= 2 else \
                logging.INFO    if verbose == 1 else \
                logging.WARNING if verbose == 0 else \
                logging.ERROR
    logging.basicConfig(level=log_level,
            format="%(asctime)s.%(msecs)03d [%(levelname)s] [%(module)s] %(message)s", datefmt="%H:%M:%S")


def assert_eq(expected, val):
    if expected != val:
        raise RuntimeError("Assert equal error: Expected '{}' is not equal to '{}'".format(expected, val))

def test_search_path():
    def to_test(path_prefix):
        path, suffix = search_path(path_prefix)
        print("path_prefix: %s ->  path: %s, suffix: %s" % (path_prefix, path, suffix))

    to_test('.model/knn')
    to_test('.model/knn/AssertFail')
    to_test('.model/knn/BadPrefix')
    to_test('/etc/app')

def test_find_seq():
    seq = 'Buying food on the street is nothing new but in the UK this idea is really taking off Its a great way of sampling freshly cooked dishes from around the world Rob and Neil discuss the subject and hear from an expert who explains the popularity in this type of food plus you can learn nothing new vocabulary along the way'.split()

    def to_skip(w):
        return w in {'on', 'the', 'is', 'in', 'a', 'an', 'of', 'from', 'and'}

    assert_eq((1, 7), find_seq(seq, 'food street nothing'.split(), None, to_skip))
    assert_eq((1, 7), find_seq(seq, 'food on the street is nothing'.split()))
    assert_eq((38, 44), find_seq(seq, 'hear expert who explains'.split(), None, to_skip))

    assert_eq((1, 7), rfind_seq(seq, 'food street nothing'.split(), None, to_skip))
    assert_eq((1, 7), rfind_seq(seq, 'food on the street is nothing'.split()))
    assert_eq((38, 44), rfind_seq(seq, 'hear expert who explains'.split(), None, to_skip))

    assert_eq((6, 8), find_seq(seq, 'nothing new'.split(), None, to_skip))
    assert_eq((6, 8), find_seq(seq, 'nothing new'.split(), None, to_skip, 6))
    assert_eq((55, 57), find_seq(seq, 'nothing new'.split(), None, to_skip, 7))

    assert_eq((55, 57), rfind_seq(seq, 'nothing new'.split(), None, to_skip))
    assert_eq((6, 8), rfind_seq(seq, 'nothing new'.split(), None, to_skip, 56))

if __name__  == '__main__':
     test_find_seq()
