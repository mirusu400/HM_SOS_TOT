# WARNING
All of these are as of *Japanese* version of TOT, It may different structure of USA, EUR version.

# PAPA file
All of PAPA files are not have extension, but they have magic stamp(header) `PAPA`.

Also, all of these are `Little Endian`.
```
Offset  Size                        Info                    Hex
0x00    ascii                       Magic stamp [PAPA]      50 41 50 41
0x04    0x04                        Unknown                 00 00 00 00
0x08    0x04                        Unknown                 0C 00 00 00  
0x0C    0x04                        Size of header (0)
0x10    0x04                        Count of subfile
0x14    0x04 * (Count of subfile)   Array of *block* offset

(0) Size of header + 0x0B = First block offset


On a block offset..
Offset      Size            Info                       
0x00        0x04            block size
0x04        0x04            Count of offset header (Mul 4 == offset size)  
0x08        0x04            Offset of something
0x[Offset]  ascii/unicode   Texts/Flags/Labels

WARNING:
* File sizes may be mod by 4.
* End of block files always 00 00 00 00 00 00 00 00 (A dummy offset).
 
```