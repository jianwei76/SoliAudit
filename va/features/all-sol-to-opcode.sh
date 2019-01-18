#!/bin/bash

exedir=$(dirname `realpath "$0"`)
homedir=$(dirname "$exedir")

soldir="$homedir/sc-src"
vuldir="$homedir/vul-predict"

if [ ! -d "$soldir" ]; then
    echo "sol folder '$soldir' does not exit"
    exit 1
fi
if [ ! -d "$vuldir" ]; then
    echo "vul folder '$vuldir' does not exit"
    exit 1
fi


# headers
echo "Addr,Opcodes"

for f in $soldir/* ; do
    if [[ $f == *.sol ]]; then
        >&2 echo "run solidity $f"

        op=$("$vuldir/asm_parser.py" print "$f" | paste -s -d ' ' -)

        addr=$(basename "$f")
        addr=${addr%.*}

        echo $addr,$op
    fi
done
