#!/bin/bash

# parse options
POSITIONAL=()
TYPE=SRC
KEEP_ARG=0
while [[ $# -gt 0 ]]
do
	key="$1"

	case $key in
		-b|--bytecode)
			TYPE=BYTECODE
			shift # past argument
			;;
        -a|--arg)
            KEEP_ARG=1
            shift
            ;;
		*)    # unknown option
			POSITIONAL+=("$1") # save it in an array for later
			shift # past argument
			;;
	esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

# parse arguments
FILE=$1

# check options/args
# echo TYPE         = "${TYPE}"
# echo FILE         = "${FILE}"
if [ -z "$FILE" ]; then
    >&2 echo "usage: $0 [-b|--bytecode] <sol>"
    exit 1
fi

disasm() {
    #sed groups: 1) offset, 2) opcode, 3) residue if any
    if [ "$KEEP_ARG" == "1" ]; then
        evm disasm "$1" 2>/dev/null | sed -n -e 's#\(^[0-9]\+\): \([A-Z0-9]\+\)\( .*\|$\)#\2\3#p'
    else
        evm disasm "$1" 2>/dev/null | sed -n -e 's#\(^[0-9]\+\): \([A-Z0-9]\+\)\( .*\|$\)#\2#p'
    fi
}

if [ "$TYPE" == "BYTECODE" ]; then
	disasm "$FILE"
else
	# temp place to save
	tempdir=/tmp/sol.$$
	mkdir -p "$tempdir"
    trap "rm -rf $tempdir" EXIT

	# compile and output the bytecode of each contrat to diff files:
	#   compile
	#   only keep every 4th line
	#   remove empty line
	#   save each line
	solc --bin-runtime "$FILE" 2>/dev/null \
		| awk 'NR % 4 == 0' \
		| sed '/^\s*$/d' \
		| split -l 1 - "$tempdir/"

	# read bytecode files
    if [ -z "$(ls -A $tempdir)" ]; then
        >&2 echo "error: no source code compiled."
    else
        for f in $tempdir/* ; do
            disasm "$f"
        done
    fi
fi

