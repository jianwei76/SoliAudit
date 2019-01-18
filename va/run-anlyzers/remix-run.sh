
sol=$1

if [ -z "$sol" ]; then
    echo "usage $0 <sol-file>"
    exit 1
fi

echo ''
echo $sol
remix-analysis --stat-only "$sol"
echo "-------------------------------------"
