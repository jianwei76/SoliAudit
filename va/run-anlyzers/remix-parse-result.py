#!/usr/bin/env python3

import sys

vols = (
    'Transaction origin',
    'Check effects',
    'Inline assembly',
    'Block timestamp',
    'Low level calls',
    'Block.blockhash usage',
    'Selfdestruct',
)

class Rec:
    def __init__(self, addr):
        self.addr = addr
        self.txorigin = 0
        self.reentrancy = 0
        self.assembly = 0
        self.timedep = 0
        self.lowcall = 0
        self.blockhash = 0
        self.selfdestruct = 0

    def setVol(self, vol , value):
        idx = vols.index(vol)
        if idx == 0:
            self.txorigin = value
        elif idx == 1:
            self.reentrancy = value
        elif idx == 2:
            self.assembly = value
        elif idx == 3:
            self.timedep = value
        elif idx == 4:
            self.lowcall = value
        elif idx == 5:
            self.blockhash = value
        elif idx == 6:
            self.selfdestruct = value
        else:
            print("error to set unknown volnerability: " + vol, file=sys.stderr)

def parse(block):
    prefix = 'sc-src/'
    suffix = '.sol'

    if len(block) <= 0:
        return None

    first = block[0]
    if not first.endswith(suffix) or not first.startswith(prefix): #filter out non source code file
        return None

    # for the constract file
    addr = first[len(prefix): -len(suffix)]

    rec = Rec(addr)

    for line in block:
        for vol in vols:
            if line.startswith(vol):
                val = int(line[len(vol) + 1:].strip())
                rec.setVol(vol, val)

    return rec

def printRecs(recs):

    def v(val):
        return 'r' if val > 0 else ' '

    headers = list(vols)
    headers.insert(0, "Addr")
    print(", ".join(headers))

    for rec in recs:
        print("%s, %s, %s, %s, %s, %s, %s, %s" %
            (rec.addr, v(rec.txorigin), v(rec.reentrancy), v(rec.assembly), v(rec.timedep), v(rec.lowcall), v(rec.blockhash), v(rec.selfdestruct)))

if __name__ == '__main__':
    report_path = sys.argv[1]

    with open(report_path) as f:
        lines = f.readlines()

    recs = []
    block = []
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        elif line.startswith('-----------'):
            rec = parse(block)
            if rec is not None:
                recs.append(rec)
            block = []
        else:
            block.append(line)

    # output
    printRecs(recs)

        



