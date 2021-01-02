# -*- coding: utf-8 -*-

# 일본 버전 ==> Unicode(LE)
# 미국 버전 ==> Shift-jis
# JPN => STAMP TEXT[utf-16] LABEL
# ENG => STAMP LABEL TEXT[shift-jis]

import sys
import os
import struct
import binascii
from xlsxwriter.workbook import Workbook
import chardet

USA = 1
JPN = 2
FileArr=[]

DECODE_TYPE = JPN



def FILETOTXT(FileName, workbook):

    NFileName = os.path.splitext(FileName)[0]
    BaseName = os.path.basename(FileName)
    if len(BaseName) >= 32:
        BaseName = BaseName[0:31]
    if BaseName in FileArr:
        BaseName = BaseName[0:-2] + "2"
    FileArr.append(BaseName)
    print(BaseName)
    worksheet = workbook.add_worksheet(BaseName)
    ListOffset=[]
    #print(OutFileName)
    inFp = open(FileName, "rb")
    buf = inFp.read(4).decode("utf-8")

    if(buf != "PAPA"):
        print("Not PAPA File!")
        return

    inFp.seek(0x0c)
    buf = inFp.read(4)
    DataSize = struct.unpack('<I', buf)[0]

    buf = inFp.read(4)
    FileIndex = struct.unpack('<I',buf)[0]

    while inFp.tell() <= ((FileIndex + 4) * 4):
        buf = inFp.read(4)
        ListOffset.append(struct.unpack('<l',buf)[0])
    for i in range(0,len(ListOffset)):


        #print("Now Seek "+str(hex(inFp.tell())))

        Meta = []

        # inFp.seek(ListOffset[i])
        # test = open(NFileName + "_bin\\test_" + str(i) + ".bin","wb")
        # Length = struct.unpack("<l",inFp.read(0x4))[0]
        # inFp.seek(ListOffset[i])
        # buf = inFp.read(Length)
        # test.write(buf)
        # test.close()

        inFp.seek(ListOffset[i])
        Meta.append(struct.unpack('<l', inFp.read(0x4))[0])
        Secsize = struct.unpack('<l',inFp.read(0x4))[0]
        Meta.append(Secsize)
        if Meta[0] == 0 or Meta[1] == 0:
            break
        for j in range(0,Secsize):
            buf = inFp.read(0x4)
            if not buf:
                break
            Meta.append(struct.unpack('<l',buf)[0])
        if not buf:
            break
        # Meta[0] = Length
        # Meta[1] = Section Count
        # Meta[2] = Magic Stamp 'Msg.' Offset
        # Meta[3] = Text[JPN] Label[USA]
        # Meta[4] = Label[JPN] Text[USA]
        # Lable and Stamp Must be ASCII
        # If JPN, Text should be utf-16, If USA, Text should be shift-jis
        Stamp = ""
        Lable = ""
        Text = ""
        Style = ""
        Type = ""
        ErrorLevel = 0
        inFp.seek(ListOffset[i] + Meta[2])
        Stamp = inFp.read(0x4).decode("ASCII")
        if Meta[1] == 2:
            if DECODE_TYPE == USA:
                try:
                    inFp.seek(ListOffset[i] + Meta[3])
                    Lable = inFp.read(Meta[0] - Meta[3]).decode("cp932")

                    Style = "USA"
                    Type = "SJIS"
                except:
                    print("EXCEPTION ERROR! Something Wrong! Please Issue in my github.")
                    return -1
            else:
                print("Something Wrong! Please Issue in my github.")
                return -1
        #Lable or Text - Section 2 and 3

        elif Meta[1] == 3:
            if DECODE_TYPE == JPN:
                try:
                    inFp.seek(ListOffset[i] + Meta[3])
                    Text = inFp.read(Meta[4] - Meta[3]).decode("utf-16")

                    inFp.seek(ListOffset[i] + Meta[4])
                    Lable = inFp.read(Meta[0] - Meta[4]).decode("cp932")
                    Style = "JPN"
                    Type = "utf-16"

                except: #Error Exception
                    print("Error Exception! Perform like USA, Index ID :",i)
                    inFp.seek(ListOffset[i] + Meta[3])
                    Lable = inFp.read(Meta[4]-Meta[3]).decode("cp932")

                    inFp.seek(ListOffset[i] + Meta[4])
                    Text = inFp.read(Meta[0]-Meta[4]).decode("utf-16")
                    Style = "USA"
                    Type = "SJIS"
            elif DECODE_TYPE == USA:
                try:
                    inFp.seek(ListOffset[i] + Meta[3])
                    Lable = inFp.read(Meta[4] - Meta[3]).decode("cp932")

                    inFp.seek(ListOffset[i] + Meta[4])
                    Text = inFp.read(Meta[0] - Meta[4]).decode("utf-16")
                    Style = "USA"
                    Type = "SJIS"
                except:
                    print("Error Exception! Perform like JPN, Index ID :",i)
                    inFp.seek(ListOffset[i] + Meta[3])
                    Text = inFp.read(Meta[4] - Meta[3]).decode("utf-16")

                    inFp.seek(ListOffset[i] + Meta[4])
                    Lable= inFp.read(Meta[0] - Meta[4]).decode("cp932")
                    Style = "USA"
                    Type = "utf-16"


        worksheet.write(i, 0, str(i))
        worksheet.write(i, 1, Stamp)
        worksheet.write(i, 2, Lable)
        worksheet.write(i, 3, Text)
        worksheet.write(i, 4, Style)
        worksheet.write(i, 5, Type)
        worksheet.write(i, 6, Meta[1])
        #LineReader.writerow([i, Stamp, Lable, Text])
    inFp.close()
    #OutFp.close()
    return


        



if __name__ == '__main__':
    abspath = os.path.abspath(sys.argv[1])

    if(os.path.isdir(abspath)):
        workbook = Workbook(abspath + '.xlsx')
        file_list = os.listdir(abspath)
        for file in file_list:
            OpenFile = str(abspath) + "\\" + str(file)
            FILETOTXT(OpenFile, workbook)
        workbook.close()
    else:
        workbook = Workbook(os.path.splitext(abspath)[0] + '.xlsx')
        FILETOTXT(abspath, workbook)
        workbook.close()
        #print(sys.argv[1] + ".csv")
        #merge_csv_to_a_book([sys.argv[1] + ".csv"], sys.argv[1] + ".xlsx")

