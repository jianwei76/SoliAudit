#!/usr/bin/env python3

import os
import logging
import pandas as pd
import word2vec

__to_force = True
__to_clean = True

# return the value before setting
def options(force=None, clean=None):
    if force is not None:
        global __to_force
        __to_force = force

    if clean is not None:
        global __to_clean
        __to_clean = clean

def op_name(op):
    return op.rstrip('0123456789') 

def filter_op(op_line):
    filter_ops = [ op_name(op) for op in op_line.split() ]
    return ' '.join(filter_ops)

def gen_doc(opfile, docfile):
    logging.info('Generating opcode document...')
    if __to_force or not os.path.exists(docfile):
        op = pd.read_csv(opfile, compression='xz', index_col=0)
        op.dropna(inplace=True)
        op['Opcodes'] = op['Opcodes'].apply(filter_op)
        op.to_csv(docfile, header=False, index=False)

def clean_doc(docfile):
    if __to_clean:
        os.remove(docfile)

def get_model(opfile, binfile, size=5):
    if __to_force or not os.path.exists(binfile):
        docfile = 'op-doc.tmp.txt'
        gen_doc(opfile, docfile)

        logging.info('Training opcode word2vec...in=%s, out=%s, word-embed-size=%d' % (docfile, binfile, size))
        word2vec.word2vec(docfile, binfile, size=size, verbose=True)

        clean_doc(docfile)

    return word2vec.load(binfile)

def init_arguments():
    parser = ArgumentParser(description='train ether opcode word2vec')
    parser.add_argument("-v", "--verbose",  action="count", default=0, help="increse detail information")
    parser.add_argument("-q", "--quiet",  action="count", default=0, help="decrese detail information")
    parser.add_argument("-f", "--force", action="store_true", default=False, help="force to re-generate data")
    parser.add_argument("-c", "--clean", action="store_true", default=False, help="force to clean data")
    return parser.parse_args()

def main():
    from argparse import ArgumentParser
    from utils import set_logging

    args = init_arguments()
    set_logging(args.verbose - args.quiet)

    opfile = '../features/op.csv.xz'
    binfile = 'op-w2v.bin'

    options(force=args.force, clean=args.clean)
    model = get_model(opfile, binfile)
    print("\n".join(model.vocab))

if __name__ == '__main__':
    main()
