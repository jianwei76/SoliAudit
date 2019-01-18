
sol=$1

if [ -z "$sol" ]; then
    echo "usage $0 <sol-file>"
    exit 1
fi

echo "-------------------------------------"
md5sum "$sol"
python /oyente/oyente/oyente.py -a -s "$sol"
echo ''
