#!/usr/bin/env python3

import os
import re
import logging
import json
from command import Command
from utils import set_logging
from utils import find_seq, rfind_seq

def __get_opcode_set():
    opfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'evm-ops.lst')
    return set(Command.cmd("awk '{print toupper($2)}' '%s'" % opfile).check().run().stdout.split())

__opcode_set = __get_opcode_set()

def print_asm_lines(opcodes, begin_line_no=0):
    def is_opcode(op):
        return op['name'].isupper()

    i_width = len(str(len(opcodes) + begin_line_no))
    type_width = max([len(op['name']) for op in opcodes])

    def to_type(op):
        return '[{:^{}}]'.format(op['name'], type_width) if is_opcode(op) else \
               '|{:^{}}|'.format(op['name'], type_width)

    for i, op in enumerate(opcodes):
        print("{:<{}} {} {}:{} {}".format(i+begin_line_no, i_width, to_type(op), op['begin'], op['end'], op.get('value', '')))

def skip_till(str, matched):
    idx = str.find(matched)
    if idx > 0:
        return str[idx+len(matched):]
    return str

class AsmParser:
    @property
    def solfile(self):
        return self.__solfile

    @property
    def solbytes(self):
        if self.__solbytes is None:
            with open(self.__solfile, 'rb') as f:
                self.__solbytes = f.read()
        return self.__solbytes

    @property
    def opcodes(self):
        return self.__opcodes

    def __init__(self, solfile):
        self.__solfile = solfile
        self.__solbytes = None

        asm = self.__get_asm(solfile)
        self.__opcodes = self.__to_opcodes(asm)

    def __get_opcode_set(self, opfile):
        opcodes = set(Command.cmd("awk '{print toupper($2)}' '%s'" % opfile).check().run().stdout.split())
        #for i, op in enumerate(opcodes):
        #    print("{0:<{1}} {2}".format(i+1, 5, op))
        return opcodes

    def __get_asm(self, solfile):
        prefix = 'EVM assembly:'
        next_sec = '======='

        content = Command.cmd('solc --asm-json "%s"' % solfile).exp_exit_codes(0).run().stdout

        asm = []

        pos = 0
        while pos < len(content):
            begin = content.find(prefix, pos)
            if begin < 0:
                break

            begin += len(prefix)
            end = content.find(next_sec, begin)
            if end < 0:
                end = len(content)

            pos = end

            sec = json.loads(content[begin:end])
            if sec is not None:
                asm.append(sec)

        return asm

    def __to_opcodes(self, asm):
        opcodes = []
        for sec in asm:
            #opcodes += sec['.code']
            opcodes += sec['.data']['0']['.code']

        # remove tag and INVLAID (because evm does not disasm out the op)
        opcodes = [ op for op in opcodes if op['name'] not in ('tag', 'INVALID')]

        # normalize opname
        for op in opcodes:
            #op['name] = op['name'].upper()
            if op['name']  == 'PUSH [tag]':
                op['name'] = 'PUSH2'
            elif op['name']  == 'PUSH' or op['name'].startswith('PUSH '):
                op['name'] = 'PUSH%d' % self.__hex_to_nbytes(op['value'])
            elif op['name'] == 'KECCAK256':
                op['name'] = 'SHA3'

        return opcodes

    def __hex_to_nbytes(self, hexstr):
        if hexstr.startswith('0x'):
            hexstr = hexstr[2:]
        nbytes = (len(hexstr) + 1) // 2
        return nbytes
        
    def find(self, subseq, begin=0, end=None, reversed=False, op_eql=None, to_skip=None):
        assert isinstance(subseq, list) or isinstance(subseq, tuple) 

        def op_eql_(op_item, op):
            if op_eql is None:
                return op_item['name'] == op.upper()
            else:
                return op_eql(op_item['name'], op.upper())

        find = rfind_seq if reversed else find_seq
        return find(self.__opcodes, subseq, is_eql=op_eql_, begin=begin, end=end)

    def get_ops(self, begin, end):
        return [ op_item['name'] for op_item in self.__opcodes[begin:end] ]
        

def __find_sol_vul_loc(solfile, opseq, try_dec=True):
    parser = AsmParser(solfile)
    print_asm_lines(parser.opcodes)

    len_to_cmp = len(opseq)
    while True:
        begin, end = parser.find(opseq[:len_to_cmp])
        if 0 <= begin < end:
            break
        elif try_dec and len_to_cmp > 1:
            len_to_cmp -= 1
        else:
            return None
    logging.info("Find opcode seq between [%d, %d)" % (begin, end))
    if len_to_cmp != len(opseq):
        logging.info("Truncate the last %d opcodes: '%s'" % (len(opseq) - len_to_cmp, ' '.join(opseq[len_to_cmp:])))

    # debug: found lines
    opcodes = parser.opcodes[begin:end]
    print_asm_lines(opcodes, begin_line_no=begin)

    # find the location of source file
    begin, end = opcodes[0]['begin'], opcodes[0]['end']
    nline, npos = loc_to_linepos(parser.solbytes, begin)
    text = parser.solbytes[begin:end].decode('utf8')

    return nline, npos, text

def usage():
    print('usage:')
    print('    %s find <solfile> <opseq>' % sys.argv[0])
    print('    %s print <solfile>' % sys.argv[0])


if __name__ == '__main__':
    import sys
    from loc2linepos import loc_to_linepos

    set_logging(0)

    try:
        subcmd = sys.argv[1]

        if subcmd == 'find':
            solfile = sys.argv[2]
            opseq = sys.argv[3].split()

            loc = __find_sol_vul_loc(solfile, opseq, try_dec=True)
            if loc is None:
                logging.error("file '{}' cannot find '{}'".format(solfile, opseq))
            else:
                nline, npos, msg = loc
                print("Find: '{}': Line {}: {}: {}\nFor ({})".format(solfile, nline, npos, msg, opseq))

        elif subcmd == 'print':
            solfile = sys.argv[2]
            parser = AsmParser(solfile)
            for op in parser.opcodes:
                print(op['name'])

        else:
            raise ValueError("no subcmd '%s'" % subcmd)

    except Exception as ex:
        logging.error('Error: %s' % str(ex))
        usage()


    




