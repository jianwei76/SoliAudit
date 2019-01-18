opcode=$1
addr=$2

if [ -z "$opcode" ] || [ -z "$addr" ]; then
    echo "usage: `basename $0` <opcode> <addr>"
    exit 1
fi

src_dir=../sc-src
src_file=$src_dir/$addr.sol

if solc --opcodes "$src_file" 2>/dev/null | grep "$opcode" >/dev/null ; then
    echo "BIN         contain '$opcode': YES"
else
    echo "BIN         contain '$opcode': NO"
fi

if ./sol-to-opcode.sh "$src_file" 2>/dev/null | grep "$opcode" >/dev/null ; then
    echo "BIN-RUNTIME contain '$opcode': YES"
else
    echo "BIN-RUNTIME contain '$opcode': NO"
fi

