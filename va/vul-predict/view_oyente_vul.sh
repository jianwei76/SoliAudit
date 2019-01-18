
keyword=$1
addr=$2

if [ -z "$addr" ] || [ -z "$keyword" ]; then
    echo "usage: `basename $0` <keyword> <addr>"
fi 

report_file=../run-anlyzers/oyente-vols
source_dir=../sc-src
win_name=VULN


result=$(grep -n "$addr.*$keyword" "$report_file" | head -n1)
report_line=$(echo "$result" | awk -F: '{print $1}')
source_line=$(echo "$result" | awk -F: '{print $5}')

source_flie="$source_dir/$addr.sol"

set -x
tmux new-window -n $win_name view +$report_line $report_file +"vsp +$source_line $source_flie"
#tmux send-keys -t :$win_name C-w h  #focus left vim's pane




