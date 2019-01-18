#!/usr/bin/env python3

import os
import sys
#sys.path.append(os.path.abspath(os.path.join(__file__, '../../vul-predict')))
#import logging
import pandas as pd
#from utils import set_logging

def main():
    #set_logging();
    #logging.info('start')

    tool_csv, va_csv = sys.argv[1:3]

    # read data
    tool_label = pd.read_csv(tool_csv, index_col=0)
    tool_label.fillna('', inplace=True)
    va_label = pd.read_csv(va_csv, index_col=0)

    # check columns
    begin = tool_label.columns.get_loc('MD5') + 1  #skip MD5
    assert len(tool_label.columns[begin:]) == len(va_label.columns)

    # append VA label
    for idx in tool_label.index:
        for vul in tool_label.columns[begin:]:
            if idx in va_label.index and va_label.loc[idx][vul]:
                tool_label.loc[idx][vul] += 'v'

    # output
    filepath, ext = os.path.splitext(tool_csv)
    tool_label.to_csv(filepath + '.output' + ext)


if __name__ == '__main__':
    main()
