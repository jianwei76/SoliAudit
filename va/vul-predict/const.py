
'''
class _const:
    class ConstError(TypeError):
        pass
    def __setattr__(self,name,value):
        if self.__dict__.has_key(name):
            raise self.ConstError("Can't rebind const(%s)"%name)
        self.__dict__[name]=value

import sys
sys.modules[__name__]=_const()

const.Addr = 'Addr'
const.MD5 = 'MD5'
const.Underflow = 'Underflow'
const.Overflow = 'Overflow'
const.Multisig = 'Multisig'
const.CallDepth = 'CallDepth'
const.TOD = 'TOD'
const.TimeDep = 'TimeDep'
const.Reentrancy = 'Reentrancy'
const.AssertFail = 'AssertFail'
const.TxOrigin = 'TxOrigin'
const.CheckEffects = 'CheckEffects'
const.InlineAssembly = 'InlineAssembly'
const.BlockTimestamp = 'BlockTimestamp'
const.LowlevelCalls = 'LowlevelCalls'
const.BlockHash = 'BlockHash'
const.SelfDestruct = 'SelfDestruct'
'''

STOP_WORDS = [
    #0s: Stop and Arithmetic Operations
    'STOP',
    'ADD',
    'MUL',
    'SUB',
    'DIV',
    'SDIV',
    'MOD',
    'SMOD',
    'ADDMOD',
    'MULMOD',
    'EXP',
    'SIGNEXTEND',
    #10s: Comparison & Bitwise Logic Operations
    'LT',
    'GT',
    'SLT',
    'SGT',
    'EQ',
    'ISZERO',
    'AND',
    'OR',
    'XOR',
    'NOT',
    'BYTE',
    # 50s Stack, Memory, Storage and Flow Operations
    'POP',
    'MLOAD',
    'MSTORE',
    'MSTORE8',
    'SLOAD',
    'SSTORE',
    'JUMP',
    'JUMPI',
    'PC',
    'MSIZE',
    'GAS',
    'JUMPDEST',
    # 60s & 70s: Push Operations
    'PUSH1',
    'PUSH2',
    'PUSH3',
    'PUSH4',
    'PUSH5',
    'PUSH6',
    'PUSH7',
    'PUSH8',
    'PUSH9',
    'PUSH10',
    'PUSH11',
    'PUSH12',
    'PUSH13',
    'PUSH14',
    'PUSH15',
    'PUSH16',
    'PUSH17',
    'PUSH18',
    'PUSH19',
    'PUSH20',
    'PUSH21',
    'PUSH22',
    'PUSH23',
    'PUSH24',
    'PUSH25',
    'PUSH26',
    'PUSH27',
    'PUSH28',
    'PUSH29',
    'PUSH30',
    'PUSH31',
    'PUSH32',
    #80s: Duplication Operations
    'DUP1',
    'DUP2',
    'DUP3',
    'DUP4',
    'DUP5',
    'DUP6',
    'DUP7',
    'DUP8',
    'DUP9',
    'DUP10',
    'DUP11',
    'DUP12',
    'DUP13',
    'DUP14',
    'DUP15',
    'DUP16',
    #90s: Exchange Operations
    'SWAP1',
    'SWAP2',
    'SWAP3',
    'SWAP4',
    'SWAP5',
    'SWAP6',
    'SWAP7',
    'SWAP8',
    'SWAP9',
    'SWAP10',
    'SWAP11',
    'SWAP12',
    'SWAP13',
    'SWAP14',
    'SWAP15',
    'SWAP16',
    #a0s: Logging Operations
    'LOG0',
    'LOG1',
    'LOG2',
    'LOG3',
    'LOG4',
]
