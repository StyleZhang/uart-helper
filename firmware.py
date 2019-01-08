import time
import json
import os
from crc16 import *
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QMessageBox,QFileDialog
from PyQt5.QtCore import QTimer,QThread

SEND_FIRMWARE_STATE_IDLE = 0
SEND_FIRMWARE_STATE_START = 1
SEND_FIRMWARE_STATE_DATA = 2
SEND_FIRMWARE_STATE_END = 3


SEND_FIRMWARE_UI_OPEN_FILE_FAIL = 31#打开文件失败

SEND_FIRMWARE_ACK_NONE = 0
SEND_FIRMWARE_ACK_RETRY = 1
SEND_FIRMWARE_ACK_OK = 2
SEND_FIRMWARE_ACK_FAIL = 3
#发送固件对象
class firmware_thread(QThread):
    update_UI_signal = QtCore.pyqtSignal(str)
    def __init__(self,parent):
        super(firmware_thread,self).__init__()
        self.parent = parent
        self.flag = True
        self.number = 0
        self.exit_flag = 0
        
    def exit(self,flag):
        #print('thread exit',flag)
        self.exit_flag = 0
    # 接收数据
    def run(self):
        self.exit_flag = 1
        self.send_firmware_init()#发送起始帧
        if self.exit_flag !=1 :
            return
        self.send_firmware_data()
        if self.exit_flag !=1 :
            return
        #print(self.total_sector,self.firmware_size)
        self.send_end_frame(self.total_sector,self.firmware_size)
        
            
############################################起始帧####################################################
    def send_firmware_init(self):
        #print(file_name[0],sector_len)
        self.firmware_file = open(self.parent.file_name[0],"rb")
        if self.firmware_file == None :
            #self.parent.send_firmware_result_process(SEND_FIRMWARE_UI_OPEN_FILE_FAIL,0)
            self.update_UI_signal.emit('打开固件文件失败\n')
            return
        self.firmware_size = os.path.getsize(self.parent.file_name[0])
        #print(firmware_size,firmware_file)
        self.data_sector_len = self.parent.sector_len
        self.data_last_sector_len = int(self.firmware_size%self.data_sector_len)
        self.total_sector = int(self.firmware_size/self.data_sector_len)
        if ((self.firmware_size%self.parent.sector_len)!=0):
            self.total_sector = self.total_sector + 1
        #print(self.total_sector,self.data_sector_len,self.data_last_sector_len,)
        self.parent.set_send_firmware_state(SEND_FIRMWARE_STATE_START)
        if self.send_start_frame(self.total_sector,self.firmware_size) == 1 :
            self.parent.set_send_firmware_state(SEND_FIRMWARE_STATE_DATA)
        else:
            self.parent.set_send_firmware_state(SEND_FIRMWARE_STATE_IDLE)
            return
    def send_start_frame(self,num,size):
        start_frame_buf = [0x30,0x61,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
        self.update_UI_signal.emit('开始发送起始帧...\n')
        self.parent.set_send_firmware_ack(SEND_FIRMWARE_ACK_NONE)
        start_frame_buf[2] = int(num) & 0xff
        start_frame_buf[3] = (int(num) >> 8) & 0xff
        start_frame_buf[4] = int(size) & 0xff 
        start_frame_buf[5] = (int(size) >> 8) & 0xff
        start_frame_buf[6] = (int(size) >> 16) & 0xff
        start_frame_buf[7] = (int(size) >> 24) & 0xff
        crcresult = crc16(start_frame_buf,8)
        start_frame_buf[8] = crcresult & 0xff 
        start_frame_buf[9] = (crcresult >> 8) & 0xff
        try:  
            self.parent.ser.write(bytes(start_frame_buf))
        except :
            pass
        while self.parent.get_send_firmware_ack() == SEND_FIRMWARE_ACK_NONE :
            time.sleep(0.001)
            if self.parent.get_send_firmware_ack() == SEND_FIRMWARE_ACK_RETRY:
                try:
                    self.parent.ser.write(bytes(start_frame_buf))
                except :
                    pass
            elif self.parent.get_send_firmware_ack() == SEND_FIRMWARE_ACK_FAIL:
                self.update_UI_signal.emit('起始帧发送失败\n')
                return 0
            elif self.parent.get_send_firmware_ack() == SEND_FIRMWARE_ACK_OK:
                break
            if self.exit_flag != 1:
                self.update_UI_signal.emit('起始帧发送失败\n')
                return 0
        self.update_UI_signal.emit('起始帧发送完成\n\n')
        return 1

############################################数据帧####################################################    
    def send_firmware_data(self):
        data_frame_buf = []
        self.parent.set_send_firmware_state(SEND_FIRMWARE_STATE_DATA)
        self.update_UI_signal.emit('开始发送数据帧...\n')
        for i in range(0,self.total_sector):
            self.parent.set_send_firmware_ack(SEND_FIRMWARE_ACK_NONE)
            if i < (self.total_sector - 1) or (i == (self.total_sector - 1) and self.data_last_sector_len == 0):#其他帧
                firmware_data_buf = self.firmware_file.read(self.data_sector_len)#读取一帧数据
                data_frame_buf.clear()
                data_frame_buf.append(0x42)
                data_frame_buf.append(0x4c)
                data_frame_buf.append((self.data_sector_len+2) & 0xff)
                data_frame_buf.append((self.data_sector_len+2) >> 8 & 0xff)
                data_frame_buf.append((self.data_sector_len+2) >> 16 & 0xff)
                data_frame_buf.append((self.data_sector_len+2) >> 24 & 0xff)
                data_frame_buf.append((i+1) & 0xff)#sector
                data_frame_buf.append(((i+1) >>8) & 0xff)
                for j in range(0,self.data_sector_len):
                    data_frame_buf.append(int(firmware_data_buf[j]))
                crcresult = crc16(data_frame_buf,len(data_frame_buf))
                data_frame_buf.append(crcresult & 0xff)
                data_frame_buf.append((crcresult >> 8) & 0xff)
            else:#最后一帧
                firmware_data_buf = self.firmware_file.read(self.data_last_sector_len)#读取一帧数据
                data_frame_buf.clear()
                data_frame_buf.append(0x42)
                data_frame_buf.append(0x4c)
                data_frame_buf.append((self.data_last_sector_len+2) & 0xff)
                data_frame_buf.append((self.data_last_sector_len+2) >> 8 & 0xff)
                data_frame_buf.append((self.data_last_sector_len+2) >> 16 & 0xff)
                data_frame_buf.append((self.data_last_sector_len+2) >> 24 & 0xff)
                data_frame_buf.append((i+1) & 0xff)#sector
                data_frame_buf.append(((i+1) >>8) & 0xff)
                for j in range(0,self.data_last_sector_len):
                    data_frame_buf.append(int(firmware_data_buf[j]))
                crcresult = crc16(data_frame_buf,len(data_frame_buf))
                data_frame_buf.append(crcresult & 0xff)
                data_frame_buf.append((crcresult >> 8) & 0xff)
            #print(data_frame_buf)
            try:
                self.parent.ser.write(bytes(data_frame_buf))
            except :
                pass
            while self.parent.get_send_firmware_ack() == SEND_FIRMWARE_ACK_NONE :
                time.sleep(0.001)
                if self.parent.get_send_firmware_ack() == SEND_FIRMWARE_ACK_RETRY:
                    try:
                        self.parent.ser.write(bytes(data_frame_buf))
                    except :
                        pass
                elif self.parent.get_send_firmware_ack() == SEND_FIRMWARE_ACK_FAIL:
                    self.update_UI_signal.emit('数据帧' + str(i) + '发送失败\n')
                    self.parent.set_send_firmware_state(SEND_FIRMWARE_STATE_IDLE)
                    return 0
                elif self.parent.get_send_firmware_ack() == SEND_FIRMWARE_ACK_OK:
                    break
                if self.exit_flag != 1:
                    self.update_UI_signal.emit('数据帧' + str(i) + '发送失败\n')
                    self.parent.set_send_firmware_state(SEND_FIRMWARE_STATE_IDLE)
                    return 0
            self.update_UI_signal.emit('数据帧' + str(i) +'发送完毕\n')
            
        self.update_UI_signal.emit('数据帧发送完毕\n\n')
        self.parent.set_send_firmware_state(SEND_FIRMWARE_STATE_END)
        return 1
############################################结束帧####################################################
    def send_end_frame(self,num,size):

        end_frame_buf = [0x4e,0x52,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
        self.update_UI_signal.emit('发送结束帧...\n')
        self.parent.set_send_firmware_state(SEND_FIRMWARE_STATE_END)
        self.parent.set_send_firmware_ack(SEND_FIRMWARE_ACK_NONE)
        end_frame_buf[2] = int(num) & 0xff
        end_frame_buf[3] = (int(num) >> 8) & 0xff
        end_frame_buf[4] = int(size) & 0xff 
        end_frame_buf[5] = (int(size) >> 8) & 0xff
        end_frame_buf[6] = (int(size) >> 16) & 0xff
        end_frame_buf[7] = (int(size) >> 24) & 0xff
        crcresult = crc16(end_frame_buf,8)
        end_frame_buf[8] = crcresult & 0xff 
        end_frame_buf[9] = (crcresult >> 8) & 0xff
        try:
            self.parent.ser.write(bytes(end_frame_buf))
        except:
            pass
        while self.parent.get_send_firmware_ack() == SEND_FIRMWARE_ACK_NONE :
            time.sleep(0.001)
            if self.parent.get_send_firmware_ack() == SEND_FIRMWARE_ACK_RETRY:
                try:
                    self.parent.ser.write(bytes(end_frame_buf))
                except:
                    pass
            elif self.parent.get_send_firmware_ack() == SEND_FIRMWARE_ACK_FAIL:
                self.update_UI_signal.emit('发送结束帧失败\n')
                return 0
            elif self.parent.get_send_firmware_ack() == SEND_FIRMWARE_ACK_OK:
                break
            if self.exit_flag != 1:
                self.update_UI_signal.emit('发送结束帧失败\n')
                return 0
        self.update_UI_signal.emit('结束帧发送完毕\n')
        self.parent.set_send_firmware_state(SEND_FIRMWARE_STATE_IDLE)
        return 1