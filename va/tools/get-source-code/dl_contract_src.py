#!/usr/bin/python3

import sys
import os
import shutil
import time
from urllib.request import Request, urlopen
import logging

logging.basicConfig(level=logging.INFO,
        format="%(asctime)s.%(msecs)03d [%(levelname)s] [%(module)s] %(message)s", datefmt="%H:%M:%S")

def parseCode(html):
    begin = html.index('>', html.index("'js-sourcecopyarea'")) + 1
    end = html.index('</pre>', begin)
    code = html[begin: end]
    return code


def downloadPage(url, filepath):
    if os.path.exists(filepath):
        #logging.info('DL %s [Skip]' % url)
        return

    try:
        logging.info("DL %s" % url)

        # get html page
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=30) as resp:
            html = resp.read().decode('utf-8')
            time.sleep(0.1)

        # retrieve the code
        code = parseCode(html)
        code_bin = code.encode('utf-8')  #ensure encode is OK before opening file to write

        # save
        with open(filepath, 'wb') as f:
            f.write(code_bin)

        logging.info('DL %s [OK]' % url)

    except Exception as ex:
        logging.error('DL %s [FAILED][%s]' % (url, str(ex)))


addrs_file = 'addrs.txt'

def main():

    #if len(sys.argv) != 2:
    #    logging.error("usage: %s <addr>" % sys.argv[0])
    #    sys.exit(1)
    #addr = sys.argv[1].strip()

    with open(addrs_file, 'r') as f:
        addrs = f.readlines()

    for addr in addrs:
        addr = addr.strip()
        url = 'https://etherscan.io/address/%s#code' % addr
        filepath = 'sc/%s.sol' % addr
        downloadPage(url, filepath)

if __name__ == '__main__':
    main()
