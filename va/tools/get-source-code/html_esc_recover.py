#!/usr/bin/python3

import os
import logging

logging.basicConfig(level=logging.INFO,
        format="%(asctime)s.%(msecs)03d [%(levelname)s] [%(module)s] %(message)s", datefmt="%H:%M:%S")

sc_dir = "sc"

def init_esc_num_tbl():
    a = [None] * 2048
    a[39] = "'"
    a[160] = ' '
    a[161] = '¡'
    a[162] = '¢'
    a[163] = '£'
    a[164] = '¤'
    a[165] = '¥'
    a[166] = '¦'
    a[167] = '§'
    a[168] = '¨'
    a[169] = '©'
    a[170] = 'ª'
    a[171] = '«'
    a[172] = '¬'
    a[173] = '-'
    a[174] = '®'
    a[175] = '¯'
    a[176] = '~'
    a[177] = '±'
    a[178] = '²'
    a[180] = '´'
    a[181] = 'µ'
    a[182] = '¶'
    a[183] = '·'
    a[184] = '¸'
    a[185] = '¹'
    a[186] = 'º'
    a[187] = '»'
    a[188] = '¼'
    a[189] = '½'
    a[190] = '¾'
    a[191] = '¿'
    a[193] = 'Á'
    a[194] = 'Â'
    a[195] = 'Ã'
    a[196] = 'Ä'
    a[199] = 'Ç'
    a[205] = 'Í'
    a[207] = 'Ï'
    a[208] = 'Ð'
    a[212] = 'Ô'
    a[214] = 'Ö'
    a[215] = '×'
    a[220] = 'Ü'
    a[224] = 'à'
    a[225] = 'á'
    a[226] = 'â'
    a[227] = 'ã'
    a[228] = 'ä'
    a[229] = 'å'
    a[230] = 'æ'
    a[231] = 'ç'
    a[232] = 'è'
    a[233] = 'é'
    a[234] = 'ê'
    a[236] = 'ì'
    a[237] = 'í'
    a[238] = 'î'
    a[239] = 'ï'
    a[242] = 'ò'
    a[243] = 'ó'
    a[244] = 'ô'
    a[246] = 'ö'
    a[249] = 'ù'
    a[250] = 'ú'
    a[252] = 'ü'
    a[1050] = 'к'
    return a

ESC_NUM_TBL = init_esc_num_tbl();

ESC_TBL = {
    '&gt;': '>',
    '&lt;': '<',
    '&quot;': '"',
    '&amp;': '&',
    '&euro;': '€',

    '&#127801;': '🌹',
    '&#127829;': '🍕',
    '&#127866;': '🍺',
    '&#128165;': '💥',
    '&#128187;': '💻',
    }


def replaceFile(path, content):

    tmp_path = path + ".tmp"

    # save
    with open(tmp_path, 'w', encoding='utf-8') as f:
        f.write(content)

    #content_bin = content.encode('utf-8')  #ensure encode is OK before opening file to write
    #with open(tmp_path, 'wb') as f:
        #f.write(content_bin)

    os.remove(path)
    os.rename(tmp_path, path)

def unescHtml(path):
    # read content
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as ex:
        if "'utf-8' codec can't decode" in str(ex):
            with open(path, 'r', encoding='big5') as f:
                content = f.read()
        else:
            raise ex

    size = len(content)
    
    # replace escaped char
    for escaped, orig in ESC_TBL.items():
        content = content.replace(escaped, orig)

    # replace escaped num char
    try:
        begin = 0;
        while True:
            begin = content.index('&#', begin)
            end = content.index(';', begin)
            txt = content[begin: end + 1]
            num = int(txt[2:-1])
            logging.info("change %s to %s" % (txt, ESC_NUM_TBL[num]))
            content = content.replace(txt, ESC_NUM_TBL[num])
            begin += 1
    except Exception as ex:
        if 'substring not found' not in str(ex):
            raise ex

    # save file if changed
    if len(content) < size:  # a shortcut to tell
        replaceFile(path, content)

if __name__ == '__main__':
    # test
    # unescHtml("sc/0xb1bd9e21ccbec1102e61e6613bdd018eaa24c77b.sol")

    for sc in os.listdir(sc_dir):
        try:
            path = os.path.join(sc_dir, sc)
            unescHtml(path)
        except Exception as ex:
            logging.error("unescape %s error: %s", path, str(ex))


