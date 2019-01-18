#!/usr/bin/env python3

import sys

class Rec:
    def __init__(self):
        self.addr = None
        self.hash = None
        self.coverage = False
        self.underflow = False
        self.overflow = False
        self.multisig = False
        self.calldepth = False
        self.tod = False
        self.timedep = False
        self.reentrancy = False
        self.assertfail = False

def printRecs(recs):

    def v(positive):
        return 'o' if positive else ' '

    print("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" %
            ("Addr", "MD5", "Underflow", "Overflow", "Multisig", "CallDepth", "TOD", "TimeDep", "Reentrancy", "AssertFail"))
    for rec in recs:
        print("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" %
            (rec.addr, rec.hash, v(rec.underflow), v(rec.overflow), v(rec.multisig), v(rec.calldepth), v(rec.tod), v(rec.timedep), v(rec.reentrancy), v(rec.assertfail)))

def getValue(n, line):
    vol = [None] * 10
    vol[1] = 'EVM Code Coverage'
    vol[2] = 'Integer Underflow'
    vol[3] = 'Integer Overflow'
    vol[4] = 'Parity Multisig Bug 2'
    vol[5] = 'Callstack Depth Attack Vulnerability'
    vol[6] = 'Transaction-Ordering Dependence (TOD)'
    vol[7] = 'Timestamp Dependency'
    vol[8] = 'Re-Entrancy Vulnerability'
    vol[9] = 'Assertion Failure'

    if not vol[n] in line:
        errmsg = "parsing for '%s' error: %d, %s" % (vol[n], n, line)
        print(errmsg, file=sys.stderr)
        return None
        #raise Exception(errmsg)

    val = line[line.rindex(':') + 1:].strip()
    return val

def orRec(recs):
    if len(recs) == 1:
        return recs[0]

    rec = Rec()
    for r in recs:
        rec.coverage = rec.coverage or r.coverage
        rec.underflow = rec.underflow or r.underflow
        rec.overflow = rec.overflow or r.overflow
        rec.multisig = rec.multisig or r.multisig
        rec.calldepth = rec.calldepth or r.calldepth
        rec.tod = rec.tod or r.tod
        rec.timedep = rec.timedep or r.timedep
        rec.reentrancy = rec.reentrancy or r.reentrancy
        rec.assertfail = rec.assertfail or r.assertfail

    return rec


def parse(block):
    prefix = 'sc-surc/'
    suffix = '.sol'

    if len(block) <= 0:
        return None

    first = block[0]
    if not first.endswith(suffix): #filter out non source code file
        return None

    # for the constract file
    hash = first[:32]
    addr = first[first.index('0x', 32): -len(suffix)]

    # for each contract class
    recs = []
    base = None
    for i, line in enumerate(block):
        if '============ Results ===========' in line:
            rec = Rec()
            base = i;

        if base is None:
            continue

        sn = i - base
        if sn >= 10 or sn <= 0:
            continue

        val = getValue(sn, line)
        if val is None:  #premature end
            recs.append(rec)
            base = None
            continue

        if sn == 1:
            rec.coverage = float(val[:-1])
        elif sn == 2:
            rec.underflow = getValue(sn, line) == 'True'
        elif sn == 3:
            rec.overflow = getValue(sn, line) == 'True'
        elif sn == 4:
            rec.multisig = getValue(sn, line) == 'True'
        elif sn == 5:
            rec.calldepth = getValue(sn, line) == 'True'
        elif sn == 6:
            rec.tod = getValue(sn, line) == 'True'
        elif sn == 7:
            rec.timedep = getValue(sn, line) == 'True'
        elif sn == 8:
            rec.reentrancy = getValue(sn, line) == 'True'
        elif sn == 9:
            rec.assertfail = getValue(sn, line) == 'True'
            recs.append(rec)
            base = None  #normal end

    if len(recs) == 0:
        return None

    # or each rec
    rec = orRec(recs)
    '''
    print("-------- %s ---------" % addr)
    printRecs(recs)
    printRecs([rec])
    print("---------------------")
    '''

    rec.addr = addr
    rec.hash = hash
    return rec

if __name__ == '__main__':
    report_path = sys.argv[1]

    with open(report_path) as f:
        lines = f.readlines()

    recs = []
    block = []
    for line in lines:
        if line.startswith('-----------'):
            rec = parse(block)
            if rec is not None:
                recs.append(rec)
            block = []
        else:
            block.append(line.strip())

    # the last block
    rec = parse(block)
    if rec is not None:
        recs.append(rec)

    # output
    printRecs(recs)

        



