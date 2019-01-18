#!/usr/bin/python3

import logging
import os
import urllib
import time
import shutil
from urllib.request import Request, urlopen
from html.parser import HTMLParser

LOCAL_DIR = 'page' 


class EtherHTMLParser(HTMLParser):
    @property
    def contract_info(self):
        return list(zip(self.__addrs, self.__contract_names, self.__compilers))

    def __init__(self):
        super().__init__()
        self.__row = 0
        self.__col = 0
        self.__is_a = False
        self.__is_in = False
        self.__addrs = []
        self.__contract_names = []
        self.__compilers = []

    def handle_starttag(self, tag, attrs):
        if tag == 'tbody': self.__is_in = True
        if tag == 'a': self.__is_a = True

        if tag == 'tr':
            self.__row += 1
            self.__col = 0
        elif tag == 'td':
            self.__col += 1

    def handle_endtag(self, tag):
        if tag == 'tbody': self.__is_in = False
        if tag == 'a': self.__is_a = False

    def handle_data(self, data):
        if self.__is_in:
            data = data.strip()
            if self.__col == 1 and self.__is_a:
                logging.info("Address:" + data)
                self.__addrs.append(data)
            elif self.__col == 2:
                logging.info("ContractName: " + data)
                self.__contract_names.append(data)
            elif self.__col == 3:
                logging.info("Compiler: " + data)
                self.__compilers.append(data)

def download_pages(page):
    try:
        local_path = '%s/%d.html' % (LOCAL_DIR, page)
        if not os.path.exists(local_path):
            url = 'https://etherscan.io/contractsVerified/%d' % page
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            logging.info("[%s] DL %s" % ("SC", url))

            #urllib.urlretrieve(req, local_path)
            with urlopen(req, timeout=30) as resp, open(local_path, 'wb') as out_file:
                shutil.copyfileobj(resp, out_file)
                #tile_data = resp.read()
            logging.info('[%s] DL %s [OK]' % ("SC", url))
            time.sleep(0.3)
    except Exception as ex:
        logging.error('[%s] DL %s [FAILED][%s]' % ("SC", url, str(ex)))

def parse_addr(content, begin):
    addr_pre = "'address-tag'>"
    addr_suf = "</a>"

    begin = content.index(addr_pre, begin)
    if begin > 0:
        end = content.index(addr_suf, begin)
        addr = content[begin + len(addr_pre):end]
        logging.info("parsed: " + addr)
        return end, addr
    else:
        return -1, None

def read_file(path):
    with open(path, 'r') as f:
        return f.read()

def parse_page(page):

    local_path = '%s/%d.html' % (LOCAL_DIR, page)

    try:
        logging.info("[%s] parsing %s" % ("SC", local_path))
        content = read_file(local_path)

        parser = EtherHTMLParser()
        parser.feed(content)
        return parser.contract_info
    except ValueError:
        pass
    except Exception as ex:
        logging.error('[%s] parsing %s [FAILED][%s]' % ("SC", local_path, str(ex)))

    return None

def main():
    logging.basicConfig(level=logging.INFO,
        format="%(asctime)s.%(msecs)03d [%(levelname)s] [%(module)s] %(message)s", datefmt="%H:%M:%S")

    page_last = 1568

    os.makedirs(LOCAL_DIR, exist_ok=True)

    for page in range(1, page_last+1):
        download_pages(page)

    data = []
    for page in range(1, page_last+1):
        data.extend(parse_page(page))

    #print
    logging.info("total %d smart contract" % len(data))
    for addr, con_name, compiler  in data:
        print("%s,%s,%s" % (addr, compiler, con_name))

if __name__ == '__main__':
    main()
