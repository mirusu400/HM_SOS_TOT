# -*- coding: utf-8 -*-

# 일본 버전 ==> Unicode(LE)
# 미국 버전 ==> Shift-jis
# JPN => STAMP TEXT[utf-16] LABEL
# ENG => STAMP LABEL TEXT[shift-jis]

import sys
import os
import struct
import json
from xlsxwriter.workbook import Workbook
import chardet
import codecs

USA = 0x02
JPN = 0x03

DECODE_TYPE = JPN

def subfile(data):
    btext = data["text"].encode("utf-16")
    blabel = data["label"].encode("shift-jis")
    bMsg = b"Msg\x00"
    bom = codecs.BOM_UTF16_LE 
    assert btext.startswith(bom) 
    btext = btext[len(bom):]
    while len(btext) % 4 != 0:
        btext += b"\x00"
    while len(blabel) % 4 != 0:
        blabel += b"\x00"
    blocksize = len(btext) + len(blabel) + len(bMsg) + 0x14
    version = 0x03
    offsetMsg = 0x14
    offsetText = 0x14 + len(bMsg)
    offsetLabel = offsetText + len(btext)
    
    b = struct.pack("<IIIII", blocksize, version, offsetMsg, offsetText, offsetLabel)
    b += bMsg
    b += btext
    b += blabel
    return b
    

def _import(originalfile, jsonfile, outfile):
    bheader = b"PAPA"
    bunknown = b"\x00\x00\x00\x00\x0C\x00\x00\x00"
    size = 0
    json_data = []
    blocks = []
    blockoffsets = []
    with open(jsonfile, 'r', encoding="utf-8") as f:
        json_data = json.load(f)
    
    lensubfile = len(json_data) + 1

    # 1. get blocks    
    for i in json_data:
        b = subfile(i)
        blocks.append(b)

    # Add Dummy
    blocks.append(b"\x00\x00\x00\x00\x00\x00\x00\x00")
    
    # 2. get headers
    headersize = (lensubfile * 4) + 0x08 # Actually you should add 0x10
    real_first_section = (lensubfile * 4) + 0x14

    # 3. get offsets
    blockoffsets.append(real_first_section)
    for i in range(lensubfile-1):
        blockoffsets.append(blockoffsets[i] + len(blocks[i]))
    # 0x00 ~ 0x0C
    b = bheader + bunknown
    # 0x0C ~ 0x10
    b += struct.pack("<I", headersize)
    # 0x10 ~ 0x14
    b += struct.pack("<I", lensubfile)

    for i in blockoffsets:
        b += struct.pack("<I", i)
    
    for i in blocks:
        b += i
    
    with open(outfile, 'wb') as f:
        f.write(b)

    return


        



if __name__ == '__main__':
    # workbook = Workbook("hi" + '.xlsx')
    # FILETOTXT("AnimalMsg", workbook)
    # filename = sys.argv[1]

    abspath = os.path.abspath(sys.argv[1])

    if(os.path.isdir(abspath)):
        # workbook = Workbook(abspath + '.xlsx')
        file_list = os.listdir(abspath)
        for file in file_list:
            filedir = str(abspath) + "\\" + str(file)
            # extract(filedir)
        # workbook.close()
    else:
        filename = sys.argv[1]
        jsonname = os.path.splitext(filename)[0] + '.json'
        if not os.path.isfile(jsonname):
            print(f"File {filename} is not exist!")
            exit()
        outname = os.path.splitext(filename)[0] + '.out'
        _import(filename, jsonname, outname)
