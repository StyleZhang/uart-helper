import time
from Crypto.Cipher import AES 
from binascii import b2a_hex, a2b_hex  
import os
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import QTimer,QThread
class aes(object):
    def __init__(self,parent):
        super(aes,self).__init__()
        self.Nb = 4
        self.Nr = 0
        self.Nk = 0
        self.in_data = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]#16字节
        self.out_data = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]#16字节
        self.state = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]#4*4字节，二维数组
        self.RoundKey = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,\
                        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,\
                        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,\
                        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,\
                        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,\
                        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,\
                        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,\
                        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,\
                        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,\
                        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,\
                        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,\
                        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,\
                        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,\
                        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,\
                        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]#240字节

        self.Key = [0x62, 0x6F, 0x6C, 0x6F, 0x72, 0x6F, 0x62, 0x6F,\
                                    0x74, 0x31, 0x39, 0x38, 0x36, 0x36, 0x31, 0x39,\
                                    0x32, 0x30, 0x31, 0x36, 0x30, 0x36, 0x31, 0x36,\
                                    0x18, 0x58, 0x84, 0x62, 0x61, 0x90, 0x07, 0xff ]

        self.Rcon = [0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a,\
                                0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39,\
                                0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a,\
                                0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8,\
                                0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef,\
                                0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc,\
                                0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b,\
                                0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3,\
                                0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94,\
                                0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20,\
                                0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35,\
                                0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f,\
                                0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04,\
                                0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63,\
                                0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd,\
                                0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb ]

        self.rsbox =  [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb\
                                , 0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb\
                                , 0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e\
                                , 0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25\
                                , 0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92\
                                , 0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84\
                                , 0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06\
                                , 0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b\
                                , 0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73\
                                , 0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e\
                                , 0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b\
                                , 0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4\
                                , 0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f\
                                , 0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef\
                                , 0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61\
                                , 0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d ]

        self.sbox = [  #0     1    2      3     4    5     6     7      8    9     A      B    C     D     E     F
                                0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,\
                                0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,\
                                0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,\
                                0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,\
                                0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,\
                                0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,\
                                0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,\
                                0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,\
                                0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,\
                                0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,\
                                0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,\
                                0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,\
                                0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,\
                                0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,\
                                0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,\
                                0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16 ]


    def xtime(self,x):
        return ((x<<1) ^ (((x>>7) & 1) * 0x1b))
    

    def Multiply(self,x,y):
        return (((y & 1) * x) ^ ((y>>1 & 1) * self.xtime(x)) ^ ((y>>2 & 1) * self.xtime(self.xtime(x))) ^ ((y>>3 & 1) * self.xtime(self.xtime(self.xtime(x)))) ^ ((y>>4 & 1) * self.xtime(self.xtime(self.xtime(self.xtime(x))))))
    
    def getSBoxInvert(self,num):
        return self.rsbox[num]
    

    def getSBoxValue(self,num):
        return self.sbox[num]
    

    def KeyExpansion(self):

        temp = [0x00,0x00,0x00,0x00]#4字节
        # The first round key is the key itself.
        for i in range(0,self.Nk):#(i = 0; i<Nk; i++)
            self.RoundKey[i * 4] = self.Key[i * 4]
            self.RoundKey[i * 4 + 1] = self.Key[i * 4 + 1]
            self.RoundKey[i * 4 + 2] = self.Key[i * 4 + 2]
            self.RoundKey[i * 4 + 3] = self.Key[i * 4 + 3]
            #print(self.Key[i * 4+2])
        i += 1
        # All other round keys are found from the previous round keys.
        while (i < (self.Nb * (self.Nr + 1))):
            for j in range(0,4):#(j = 0; j<4; j++)
                temp[j] = self.RoundKey[(i - 1) * 4 + j]
            
            if i % self.Nk == 0:
                # This function rotates the 4 bytes in a word to the left once.
                # [a0,a1,a2,a3] becomes [a1,a2,a3,a0]
                # Function RotWord()
                k = temp[0]
                temp[0] = temp[1]
                temp[1] = temp[2]
                temp[2] = temp[3]
                temp[3] = k
                # SubWord() is a function that takes a four-byte input word and 
                # applies the S-box to each of the four bytes to produce an output word.
                # Function Subword()    
                temp[0] = self.getSBoxValue(temp[0])
                temp[1] = self.getSBoxValue(temp[1])
                temp[2] = self.getSBoxValue(temp[2])
                temp[3] = self.getSBoxValue(temp[3])
                temp[0] = (0xff)&(temp[0] ^ self.Rcon[int(i / self.Nk)])
                
            elif self.Nk > 6 and i % self.Nk == 4:
                # Function Subword()
                temp[0] = self.getSBoxValue(temp[0])
                temp[1] = self.getSBoxValue(temp[1])
                temp[2] = self.getSBoxValue(temp[2])
                temp[3] = self.getSBoxValue(temp[3])
                
            self.RoundKey[i * 4 + 0] = (0xff)&(self.RoundKey[(i - self.Nk) * 4 + 0] ^ temp[0])
            self.RoundKey[i * 4 + 1] = (0xff)&(self.RoundKey[(i - self.Nk) * 4 + 1] ^ temp[1])
            self.RoundKey[i * 4 + 2] = (0xff)&(self.RoundKey[(i - self.Nk) * 4 + 2] ^ temp[2])
            self.RoundKey[i * 4 + 3] = (0xff)&(self.RoundKey[(i - self.Nk) * 4 + 3] ^ temp[3])
            i += 1
        
    def AddRoundKey(self,round):
        for i in range(0,4):#(i = 0; i<4; i++)
            for j in range(0,4):#(j = 0; j<4; j++)
                self.state[(j*4+i)] ^= self.RoundKey[int(round * self.Nb * 4 + i * self.Nb + j)]   
    #The SubBytes Function Substitutes the values in the
    #state matrix with values in an S-box.
    def InvSubBytes(self):
        #int i, j;
        for i in range(0,4):# (i = 0; i<4; i++)
            for j in range(0,4):#(j = 0; j<4; j++)
                self.state[(i*4+j)] = self.getSBoxInvert(self.state[(i*4+j)])

    

    # The SubBytes Function Substitutes the values in the
    # state matrix with values in an S-box.
    def SubBytes(self):
        #int i, j;
        for i in range(0,4):#(i = 0; i<4; i++)
            for j in range(0,4):# (j = 0; j<4; j++)
                self.state[(i*4+j)] = self.getSBoxValue(self.state[(i*4+j)])

    

    # The ShiftRows() function shifts the rows in the state to the left.
    # Each row is shifted with different offset.
    # Offset = Row number. So the first row is not shifted.
    def InvShiftRows(self):
        #temp = 0
        #Rotate first row 1 columns to right	
        temp = self.state[7]#temp = state[1][3];
        self.state[7] = self.state[6]#state[1,3] = state[1,2];
        self.state[6] = self.state[5]#state[1,2] = state[1,1];
        self.state[5] = self.state[4]#state[1,1] = state[1,0];
        self.state[4] = temp#state[1,0] = temp;

        # Rotate second row 2 columns to right	
        temp = self.state[8]#temp = state[2,0];
        self.state[8] = self.state[10]#state[2,0] = state[2,2];
        self.state[10] = temp#state[2,2] = temp;

        temp = self.state[9]#temp = state[2,1];
        self.state[9] = self.state[11]#state[2,1] = state[2,3];
        self.state[11] = temp#state[2,3] = temp;

        # Rotate third row 3 columns to right
        temp = self.state[12]#temp = state[3,0];
        self.state[12] = self.state[13]#state[3,0] = state[3,1];
        self.state[13] = self.state[14]#state[3,1] = state[3,2];
        self.state[14] = self.state[15]#state[3,2] = state[3,3];
        self.state[15] = temp#state[3,3] = temp;
    

    # The ShiftRows() function shifts the rows in the state to the left.
    # Each row is shifted with different offset.
    # Offset = Row number. So the first row is not shifted.
    def ShiftRows(self):
        #byte temp;

        #// Rotate first row 1 columns to left	
        temp = self.state[4]#temp = state[1,0];
        self.state[4] = self.state[5]#state[1,0] = state[1,1];
        self.state[5] = self.state[6]#state[1,1] = state[1,2];
        self.state[6] = self.state[7]#state[1,2] = state[1,3];
        self.state[7] = temp#state[1,3] = temp;

        #// Rotate second row 2 columns to left	
        temp = self.state[8]#temp = state[2,0];
        self.state[8] = self.state[10]#state[2,0] = state[2,2];
        self.state[10] = temp#state[2,2] = temp;

        temp = self.state[9]#temp = state[2,1];
        self.state[9] = self.state[11]#state[2,1] = state[2,3];
        self.state[11] = temp#state[2,3] = temp;

        #// Rotate third row 3 columns to left
        temp = self.state[12]#temp = state[3,0];
        self.state[12] = self.state[15]#state[3,0] = state[3,3];
        self.state[15] = self.state[14]#state[3,3] = state[3,2];
        self.state[14] = self.state[13]#state[3,2] = state[3,1];
        self.state[13] = temp#state[3,1] = temp;
    



    #// MixColumns function mixes the columns of the state matrix.
    #// The method used to multiply may be difficult to understand for the inexperienced.
    #// Please use the references to gain more information.
    def InvMixColumns(self):
        #int i;
        #byte a, b, c, d;
        for i in range(0,4):#for (i = 0; i<4; i++)
            a = self.state[i]
            b = self.state[4+i]
            c = self.state[8+i]
            d = self.state[12+i]
            #state[0,i] = (byte)(Multiply(a, 0x0e) ^ Multiply(b, 0x0b) ^ Multiply(c, 0x0d) ^ Multiply(d, 0x09));
            #state[1,i] = (byte)(Multiply(a, 0x09) ^ Multiply(b, 0x0e) ^ Multiply(c, 0x0b) ^ Multiply(d, 0x0d));
            #state[2,i] = (byte)(Multiply(a, 0x0d) ^ Multiply(b, 0x09) ^ Multiply(c, 0x0e) ^ Multiply(d, 0x0b));
            #state[3,i] = (byte)(Multiply(a, 0x0b) ^ Multiply(b, 0x0d) ^ Multiply(c, 0x09) ^ Multiply(d, 0x0e));
            self.state[i] = ((self.Multiply(a, 0x0e) ^ self.Multiply(b, 0x0b) ^ self.Multiply(c, 0x0d) ^ self.Multiply(d, 0x09))&0xff)
            self.state[4+i] = ((self.Multiply(a, 0x09) ^ self.Multiply(b, 0x0e) ^ self.Multiply(c, 0x0b) ^ self.Multiply(d, 0x0d))&0xff)
            self.state[8+i] = ((self.Multiply(a, 0x0d) ^ self.Multiply(b, 0x09) ^ self.Multiply(c, 0x0e) ^ self.Multiply(d, 0x0b))&0xff)
            self.state[12+i] = ((self.Multiply(a, 0x0b) ^ self.Multiply(b, 0x0d) ^ self.Multiply(c, 0x09) ^ self.Multiply(d, 0x0e))&0xff)
    

    #// MixColumns function mixes the columns of the state matrix
    def MixColumns(self):
        #int i;
        #byte Tmp, Tm, t;
        for i in range(0,4):#for (i = 0; i<4; i++)
            t = self.state[i]
            Tmp = (0xff)&(self.state[i] ^ self.state[4+i] ^ self.state[8+i] ^ self.state[12+i])
            Tm = (0xff)&(self.state[i] ^ self.state[4+i])
            Tm = (0xff)&(self.xtime(Tm))
            self.state[i] ^= (0xff)&(Tm ^ Tmp)

            Tm = (0xff)&(self.state[4+i] ^ self.state[8+i])
            Tm = (0xff)&(self.xtime(Tm)) 
            self.state[4+i] ^= (0xff)&(Tm ^ Tmp)

            Tm = (0xff)&(self.state[8+i] ^ self.state[12+i])
            Tm = (0xff)&(self.xtime(Tm))
            self.state[8+i] ^= (0xff)&(Tm ^ Tmp)

            Tm = (0xff)&(self.state[12+i] ^ t)
            Tm = (0xff)&(self.xtime(Tm))
            self.state[12+i] ^= (0xff)&(Tm ^ Tmp)
        
    

    #// InvCipher is the main function that decrypts the CipherText.
    def InvCipher(self):
        #int i, j, round = 0;

        #//Copy the input CipherText to state array.
        for i in range(0,4):#for (i = 0; i<4; i++)
            for j in range(0,4):#for (j = 0; j<4; j++)
                self.state[(j*4+i)] = self.in_data[(i * 4 + j)]
            

        #// Add the First round key to the state before starting the rounds.
        self.AddRoundKey(self.Nr)

        #// There will be Nr rounds.
        #// The first Nr-1 rounds are identical.
        #// These Nr-1 rounds are executed in the loop below.
        round = self.Nr - 1
        while round > 0:#for (round = Nr - 1; round>0; round--)
            self.InvShiftRows()
            self.InvSubBytes()
            self.AddRoundKey(round)
            self.InvMixColumns()
            round -= 1

        #// The last round is given below.
        #// The MixColumns function is not here in the last round.
        self.InvShiftRows()
        self.InvSubBytes()
        self.AddRoundKey(0)

        #// The decryption process is over.
        #// Copy the state array to output array.
        for i in range(0,4):#for (i = 0; i<4; i++)
            for j in range(0,4):#for (j = 0; j<4; j++)
                self.out_data[i * 4 + j] = self.state[(j*4+i)]
            
    

    #// Cipher is the main function that encrypts the PlainText.
    def Cipher(self):
        #int i, j, round = 0;

        #//Copy the input PlainText to state array.
        for i in range(0,4):#for (i = 0; i<4; i++)
            for j in range(0,4):#for (j = 0; j<4; j++)
                self.state[(j*4+i)] = self.in_data[i * 4 + j]
            

        #// Add the First round key to the state before starting the rounds.
        self.AddRoundKey(0)

        #// There will be Nr rounds.
        #// The first Nr-1 rounds are identical.
        #// These Nr-1 rounds are executed in the loop below.
        for round in range(1,self.Nr):#for (round = 1; round<Nr; round++)
            self.SubBytes()
            self.ShiftRows()
            self.MixColumns()
            self.AddRoundKey(round)
            
        

        #// The last round is given below.
        #// The MixColumns function is not here in the last round.
        self.SubBytes()
        self.ShiftRows()
        self.AddRoundKey(self.Nr)

        #// The encryption process is over.
        #// Copy the state array to output array.
        for i in range(0,4):#for (i = 0; i<4; i++)
            for j in range(0,4):#for (j = 0; j<4; j++)
                self.out_data[i * 4 + j] = self.state[(j*4+i)]
            
    def Encrypt(self,ecpNum, buffer):
    
        #int i;
        self.Nr = ecpNum
        self.Nk = int(self.Nr / 32)
        self.Nr = self.Nk + 6
        for i in range(0,16):#for (i = 0; i<16; i++)
            self.in_data[i] = buffer[i]
        
        #// The KeyExpansion routine must be called before encryption.
        self.KeyExpansion()

        #// The next function call encrypts the PlainText with the Key using AES algorithm.
        self.Cipher()
        #for i in range(0,16):#for (i = 0; i < 16; i++)
        #    output[i] = self.out_data[i]
        return self.out_data

    def Decrypt(self,ecpNum,buffer):
    
        #int i;
        self.Nr = ecpNum
        self.Nk = int(self.Nr / 32)
        self.Nr = self.Nk + 6

        for i in range(0,16):#for (i = 0; i<16; i++)
            self.in_data[i] = buffer[i]
        #//The Key-Expansion routine must be called before the decryption routine.
        self.KeyExpansion()

        #// The next function call decrypts the CipherText with the Key using AES algorithm.
        self.InvCipher()
        #for i in range(0,16):#for (i = 0; i < 16; i++)
        #    output[i] = self.out_data[i]
            #output.
        return self.out_data
def add_buf_16(buf):
    while len(buf) < 16:
        buf += '\0'
    return buf
    #print('len(buf)+',len(buf))


#加密对象
class aes_encrypt_thread(QThread):
    update_UI_signal = QtCore.pyqtSignal(str)
    def __init__(self,parent):
        super(aes_encrypt_thread,self).__init__()
        self.parent = parent
        self.exit_flag = 0
        

    def exit(self,flag):
        #print('aes encrypt thread exit',flag)
        self.exit_flag = 0

    # 接收数据
    def run(self):
        self.exit_flag = 1
        aes_out_buf = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
        file_buf = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
        self.aes_encrypt = aes(self)#新建加密算法对象
        self.encrypt_file = open(self.parent.encrypt_file_name[0],"rb")
        if self.encrypt_file == None :
            #self.parent.send_firmware_result_process(SEND_FIRMWARE_UI_OPEN_FILE_FAIL,0)
            self.update_UI_signal.emit('打开固件文件失败\n')
            self.encrypt_file.close()
            return
        self.encrypt_out_file_name = self.parent.encrypt_file_name[0][:-4] + '_encrypted.bin'#截取文件名
        self.encrypt_out_file = open(self.encrypt_out_file_name,"wb+")#创建文件
        self.encrypt_file_size = os.path.getsize(self.parent.encrypt_file_name[0])#获取文件大小
        self.update_UI_signal.emit('准备对 ' + self.parent.encrypt_file_name[0] + ' 进行加密\n')
        self.update_UI_signal.emit('文件大小:' + str(self.encrypt_file_size) + 'bytes\n')

        self.encrypt_read_size = 0
        percent = 0
        percent_last = 0
        while self.encrypt_file_size - self.encrypt_read_size >= 16 and self.exit_flag == 1:
            file_data = self.encrypt_file.read(16)
            i = 0
            while i < 16:
                if i < len(file_data):
                    file_buf[i] = int(file_data[i])
                else:
                    file_buf[i] = 0x00
                i += 1
            aes_out_buf = self.aes_encrypt.Encrypt(256,file_buf)
            self.encrypt_out_file.write(bytes(aes_out_buf))
            self.encrypt_read_size += 16
            percent = int((self.encrypt_read_size / self.encrypt_file_size)*100)
            if percent - percent_last >=1 :
                self.update_UI_signal.emit('加密完成:' + str(percent) + '%\n')
                percent_last = percent
        if self.exit_flag == 1:
            #最后一帧
            file_data = self.encrypt_file.read()
            i = 0
            while i < 16:
                if i < len(file_data):
                    file_buf[i] = int(file_data[i])
                else:
                    file_buf[i] = 0x00
                i += 1
            file_buf[15] = self.encrypt_file_size - self.encrypt_read_size
            aes_out_buf = self.aes_encrypt.Encrypt(256,file_buf)
            self.encrypt_out_file.write(bytes(aes_out_buf))
            self.update_UI_signal.emit('加密完成:100%\n')
            self.update_UI_signal.emit('输出文件:' + self.encrypt_out_file_name+'\n')

            self.encrypt_out_file.close()
            self.encrypt_file.close()
        else:
            self.encrypt_out_file.close()
            self.encrypt_file.close()
            try:  
                os.remove(self.encrypt_out_file_name)
            except:
                pass
#解密对象
class aes_decrypt_thread(QThread):
    update_UI_signal = QtCore.pyqtSignal(str)
    def __init__(self,parent):
        super(aes_decrypt_thread,self).__init__()
        self.parent = parent
        self.exit_flag = 0
        
    def exit(self,flag):
        #print('aes decrypt thread exit',flag)
        self.exit_flag = 0
    # 接收数据
    def run(self):
        self.exit_flag = 1
        aes_out_buf = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
        file_buf = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
        self.aes_decrypt = aes(self)#新建加密算法对象
        self.decrypt_file = open(self.parent.decrypt_file_name[0],"rb")
        if self.decrypt_file == None :
            #self.parent.send_firmware_result_process(SEND_FIRMWARE_UI_OPEN_FILE_FAIL,0)
            self.update_UI_signal.emit('打开固件文件失败!\n')
            return
        self.decrypt_out_file_name = self.parent.decrypt_file_name[0][:-4] + '_decrypted.bin'#截取文件名
        self.decrypt_out_file = open(self.decrypt_out_file_name,"wb+")#创建输出文件
        self.decrypt_file_size = os.path.getsize(self.parent.decrypt_file_name[0])#获取文件大小
        if self.decrypt_file_size < 16 or self.decrypt_file_size % 16 != 0:
            self.update_UI_signal.emit('加密文件格式错误!\n')
            self.decrypt_out_file.close()
            self.decrypt_file.close()
            return
        self.update_UI_signal.emit('准备对 ' + self.parent.decrypt_file_name[0] + ' 进行解密\n')
        self.update_UI_signal.emit('文件大小:' + str(self.decrypt_file_size) + 'bytes\n')

        self.decrypt_read_size = 0
        percent = 0
        percent_last = 0
        while self.decrypt_file_size > self.decrypt_read_size and self.exit_flag == 1:
            file_data = self.decrypt_file.read(16)
            if len(file_data) != 16:#检测非法帧
                self.update_UI_signal.emit('加密过程出现错误!\n')
                self.decrypt_out_file.close()
                os.remove(self.decrypt_out_file_name)
                return
            i = 0
            while i < 16:
                if i < len(file_data):
                    file_buf[i] = int(file_data[i])
                else:
                    file_buf[i] = 0x00
                i += 1
            aes_out_buf = self.aes_decrypt.Decrypt(256,file_buf)
            #最后一帧最后一字节表示该帧的真正大小,需删除后面多余的项
            if self.decrypt_file_size - self.decrypt_read_size == 16:
                size = aes_out_buf[15]
                for i in range(0,16 - size):
                    aes_out_buf.pop(size)
            self.decrypt_out_file.write(bytes(aes_out_buf))
            self.decrypt_read_size += 16
            percent = int((self.decrypt_read_size / self.decrypt_file_size)*100)
            if percent - percent_last >=1 :
                self.update_UI_signal.emit('解密完成:' + str(percent) + '%\n')
                percent_last = percent
        if self.exit_flag == 1:
            self.update_UI_signal.emit('输出文件:' + self.decrypt_out_file_name+'\n')
            self.decrypt_out_file.close()
            self.decrypt_file.close()
        else:
            self.decrypt_out_file.close()
            self.decrypt_file.close()
            try:
                os.remove(self.decrypt_out_file_name)   
            except :
                pass