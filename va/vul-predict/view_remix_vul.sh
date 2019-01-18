
keyword=$1
addr=$2

if [ -z "$addr" ] || [ -z "$keyword" ]; then
    echo "usage: `basename $0` <keyword> <addr>"
fi 

source_dir=../sc-src
source_flie="$source_dir/$addr.sol"
win_name=VULN


result=$(remix-analysis "$source_flie"| grep -n -e "$keyword.*location: line" | head -n1)
if [ -z "$result" ]; then
    result=$(remix-analysis "$source_flie"| grep -n -e "$keyword.*location" | head -n1)
fi

report_line=${result%%:*}   # greed trim suffix
source_line=${result##* }   # greed trim prefix
if [ "$source_line" == "NA" ]; then
    source_line=0
fi

set -x
tmux new-window -n $win_name "remix-analysis $source_flie | view +$report_line - +\"vsp +$source_line $source_flie \""




