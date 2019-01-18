#!/bin/bash

dir=$(dirname "$(readlink -f "$0")")

# parse arguments
#if [ -z "$FILE" ]; then
#    >&2 echo "usage: $0 <sol>"
#    exit 1
#fi

# get opcode | filter | join multiline
#"$dir/sol-to-opcode.sh" "$@" | grep -xF -f "$dir/pattern.txt" | paste -s -d ' ' -
"$dir/sol-to-opcode.sh" "$@" | grep -F -w -f "$dir/pattern.txt" #| paste -s -d ' ' -

