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


def check_encoding(btext):
    count = 0
    for char in btext:
        if int(char) == 0x0:
            count += 1
            continue
        if int(char) >= 0x30 and int(char) <= 0x7E:
            continue
        else:
            return "utf-16"
    if count >= 5:
        return "utf-16"
    return "ascii"



def subfile(f, block, size):
    f.seek(block)
    blocksize = struct.unpack('<I', f.read(4))[0]
    offsetcount = struct.unpack('<I', f.read(4))[0]
    if offsetcount == 0x00:
        return (0, 0)
    else:
        offsets = []
        sizes = []
        texts = []
        for i in range(offsetcount):
            offsets.append(struct.unpack('<I', f.read(4))[0])
            if i != 0:
                sizes.append(offsets[i] - offsets[i-1])
        sizes.append(size - offsets[-1])
        # print(sizes)

            

        for (idx, offset) in enumerate(offsets):
            # Exception Handling
            text = b""
            if offset < offsets[0]:
                texts.append("None")
                continue
            # text = read_btext(f, block + offset)
            text = f.read(sizes[idx])
            # Detect encoding, it may utf-16 or shift-jis
            # encoding = chardet.detect(text)['encoding']
            encoding = check_encoding(text)
            if encoding == "ascii":
                texts.append(text.decode("ascii"))
            else:
                texts.append(text.decode("utf-16"))
            
        return (offsets, texts)
    

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
            (offsets, texts) = subfile(f, blockoffsets[i], size)
            
            if texts == 0:
                continue

            data = {
                "idx" : i,
                "offsets": offsets,
            }
            # input()
            for i in range(len(texts)):
                data[str(i)] = texts[i].replace("\u0000","")
            out_json.append(data)
            # out_json[label] = text
            # text_list.append(text)
            # label_list.append(label)
    with open(out_filename, 'w', encoding="utf-8") as f:
        f.write(json.dumps(out_json, indent=4 ,ensure_ascii=False))
                
    return


        



if __name__ == '__main__':
    # workbook = Workbook("hi" + '.xlsx')
    # FILETOTXT("AnimalMsg", workbook)
    abspath = os.path.abspath(sys.argv[1])

    if(os.path.isdir(abspath)):
        file_list = os.listdir(abspath)
        for file in file_list:
            filedir = str(abspath) + "\\" + str(file)
            extract(filedir)
    else:
        extract(sys.argv[1])
