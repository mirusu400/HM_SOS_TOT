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
def check_encoding(text):
    for char in text:
        if ord(char) > 0xFF:
            return "utf-16"
    return "ascii"

def padding(_bytes):
    _bytes += b"\x00"
    while len(_bytes) % 4 != 0:
        _bytes += b"\x00"
    return _bytes

def subfile(data):
    offsets = data["offsets"]
    btexts = []
    blength = 0
    for i in range(len(offsets)):
        text = data[str(i)]
        encoding = data[f"{i}_enc"]
        if text == "None":
            btexts.append(b"")
            blength += 0
        if encoding == "utf-16":
            btext = padding(text.encode("utf-16"))
            # remove BOM
            bom = codecs.BOM_UTF16_LE 
            assert btext.startswith(bom) 
            btext = btext[len(bom):]
        else:
            btext = padding(text.encode("ascii"))
        btexts.append(btext)
        blength += len(btext)
    blocksize = (len(offsets) * 4) + blength + 0x8 # Header size
    countoffsetheader = len(offsets)
    
    b = struct.pack("<II", blocksize, countoffsetheader)
    boffset = offsets[0]
    for i in range(len(offsets)):
        # Exception handling: None of the text is set
        if btexts[i] == "":
            b += struct.pack("<I", offsets[i])
        # Normal case
        else:
            b += struct.pack("<I", boffset)
            boffset += len(btexts[i])
    
    for _ in btexts:
        b += _
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
