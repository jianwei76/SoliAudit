#!/usr/bin/env python3

import sys

def loc_to_linepos(content, loc):
    carrage = ord('\r')
    newline = ord('\n')

    line = 1
    last_line_pos = 0
    last_ch = None

    for i in range(loc+1):
        ch = content[i]

        if byte_is_linebreak(ch):
            last_line_pos = i

        if ch == carrage or (ch == newline and last_ch != carrage):
            line += 1

        last_ch = ch
            
    return line, loc - last_line_pos

def byte_is_linebreak(b):
    return b == ord('\r') or b == ord('\n')

def get_line_end(content, begin):
    for i in range(begin, len(content)+1):
        if byte_is_linebreak(content[i]):
            return i
    return i

def get_bytes(file):
    with open(file, 'br') as f:
        return f.read()

if __name__ == '__main__':
    content = get_bytes(sys.argv[1])
    begin = int(sys.argv[2])
    end = int(sys.argv[3]) if len(sys.argv) > 3 else \
          get_line_end(content, begin)

    substr = content[begin:end].decode()
    line, pos = loc_to_linepos(content, begin)

    print("Line {}, Pos {}:".format(line, pos))
    print("-------------------")
    print(substr)
    print("-------------------")

        
