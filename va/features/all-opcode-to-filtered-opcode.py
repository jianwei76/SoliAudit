#!/usr/bin/env python3

import sys

def filter_opcode(f):
    for i, line in enumerate(f):
        line = line.strip()

        if i == 0 and line == HEADERS:
            continue

        addr, op_line = line.split(',', 1)
        ops = [op for op in op_line.split() if op in act_words] # filter

        print('%s,%s' % (addr, ' '.join(ops)))

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print('usage: %s <act-words> <csv>' % sys.argv[0])
        sys.exit(1)

    act_file = sys.argv[1]
    csv_file = sys.argv[2]

    act_words = set(open(act_file).read().splitlines())  # a word per line

    HEADERS = 'Addr,Opcodes'
    print(HEADERS)

    with open(csv_file, 'r', encoding='utf-8') as f:
        filter_opcode(f)



