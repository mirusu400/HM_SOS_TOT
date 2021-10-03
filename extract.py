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

USA = 0x02
JPN = 0x03

DECODE_TYPE = JPN

def subfile(f, block, size):
    f.seek(block)
    blocksize = struct.unpack('<I', f.read(4))[0]

    # USA == 0x02, JPN == 0x03
    version = struct.unpack('<I', f.read(4))[0]
    if version == 0x00:
        return (0,0)
    elif version == 0x02:
        print(f"File {file} is USA version!")
        print("For now, USA version is not supported. exit program.")
        exit()
    elif version == 0x03:
        msgoffset = struct.unpack('<I', f.read(4))[0]
        textoffset = struct.unpack('<I', f.read(4))[0]
        labeloffset = struct.unpack('<I', f.read(4))[0]

        textsize = labeloffset - textoffset
        labelsize = size - labeloffset

        f.seek(block + textoffset)
        text = f.read(textsize).decode("utf-16")

        f.seek(block + labeloffset)
        label = f.read(labelsize).decode("shift-jis")
        return (text, label)
    

def extract(file):
    out_filename = os.path.splitext(file)[0] + '.json'
    text_list = []
    label_list = []
    out_json = []
    #print(OutFileName)
    with open(file, 'rb') as f:
        buf = f.read(4).decode("utf-8")
        if(buf != "PAPA"):
            print(f"File {file} is not PAPA file!")
            return
        f.seek(0x0c)
        # Offset of blocks
        blockoffsets = []
        # Size of header
        headersize = struct.unpack('<I', f.read(4))[0]
        # Count of subfile
        lensubfile = struct.unpack('<I', f.read(4))[0]
        for i in range(lensubfile):
            blockoffsets.append(struct.unpack('<I', f.read(4))[0])

        
        for i in range(len(blockoffsets)):
            if i == len(blockoffsets) - 1:
                size = os.path.getsize(file) - blockoffsets[i]
            else:
                size = blockoffsets[i + 1] - blockoffsets[i]
            # print(f, hex(blockoffsets[i]), size)
            text, label = subfile(f, blockoffsets[i], size)
            if text == label == 0:
                continue
            data = {
                "idx" : i,
                "label": label,
                "text" : text,
            }
            out_json.append(data)
            # out_json[label] = text
            text_list.append(text)
            label_list.append(label)
    with open(out_filename, 'w', encoding="utf-8") as f:
        f.write(json.dumps(out_json, indent=4 ,ensure_ascii=False))
                
    return


        



if __name__ == '__main__':
    # workbook = Workbook("hi" + '.xlsx')
    # FILETOTXT("AnimalMsg", workbook)
    abspath = os.path.abspath(sys.argv[1])

    if(os.path.isdir(abspath)):
        # workbook = Workbook(abspath + '.xlsx')
        file_list = os.listdir(abspath)
        for file in file_list:
            filedir = str(abspath) + "\\" + str(file)
            extract(filedir)
        # workbook.close()
    else:
        extract(sys.argv[1])
