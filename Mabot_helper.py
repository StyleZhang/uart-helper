import sys
import serial
import os
import serial.tools.list_ports
import time
import json
import binascii
from aes import aes_encrypt_thread,aes_decrypt_thread
from firmware import *
from crc16 import *
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QMessageBox,QFileDialog
from PyQt5.QtCore import QTimer,QThread
from ui_demo_1 import Ui_Form
#UI 对象
class Pyqt5_Serial(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(Pyqt5_Serial, self).__init__()
        self.setupUi(self)
        self.init()
        self.setWindowTitle("Mabot helper")
        self.ser = serial.Serial()

        #配置信息
        self.serial_config_dict = {}
        self.configfile = open('.config','a+')
        self.configfile.seek(0,0)
        self.json_str = self.configfile.read()
        if self.json_str == '':
            pass
        elif isinstance(self.json_str,str) :
            try:
                self.serial_config_dict = json.loads(self.json_str)
                #print(self.serial_config_dict['port'])
            except :
                os.remove('.config')
                        
        self.port_check()
        # 接收数据和发送数据数目置零
        self.data_num_received = 0
        self.lineEdit.setText(str(self.data_num_received))
        self.data_num_sended = 0
        self.lineEdit_2.setText(str(self.data_num_sended))
        self.send_firmware_state = SEND_FIRMWARE_STATE_IDLE
        self.send_firmware_ack = SEND_FIRMWARE_ACK_NONE

        self.file_name = ''
        self.sector_len = 0

    def init(self):
        # 串口检测按钮
        self.s1__box_1.clicked.connect(self.port_check)

        # 串口信息显示
        self.s1__box_2.currentTextChanged.connect(self.port_imf)

        # 打开串口按钮
        self.open_button.clicked.connect(self.port_open)

        # 关闭串口按钮
        self.close_button.clicked.connect(self.port_close)

        # 发送数据按钮
        self.s3__send_button.clicked.connect(self.data_send)
        #添加校验码
        self.add_crc_button.clicked.connect(self.add_crc_to_send)
        # 红外球升级按钮
        self.infrared_update_button.clicked.connect(self.send_infrared_update_ready)
        self.color_update_button.clicked.connect(self.send_color_update_ready)
        self.touch_update_button.clicked.connect(self.send_touch_update_ready)
        self.driver_update_button.clicked.connect(self.send_driver_update_ready)
        self.hsrv_update_button.clicked.connect(self.send_hsrv_update_ready)
        self.vsrv_update_button.clicked.connect(self.send_vsrv_update_ready)
        self.ultrasonic_update_button.clicked.connect(self.send_ultrasonic_update_ready)
        self.rocker_update_button.clicked.connect(self.send_rocker_update_ready)
        self.temperature_update_button.clicked.connect(self.send_temperature_update_ready)
        self.voice_update_button.clicked.connect(self.send_voice_update_ready)
        self.p2p_update_button.clicked.connect(self.send_P2P_update_ready)
        self.led_board_update_button.clicked.connect(self.send_led_board_update_ready)
        self.pyroelectric_update_button.clicked.connect(self.send_pyroelectric_update_ready)
        self.main_update_button.clicked.connect(self.send_main_update_ready)

        self.infrared_firm_check_button.clicked.connect(self.send_infrared_firm_check_ready)
        self.color_firm_check_button.clicked.connect(self.send_color_firm_check_ready)
        self.touch_firm_check_button.clicked.connect(self.send_touch_firm_check_ready)
        self.driver_firm_check_button.clicked.connect(self.send_driver_firm_check_ready)
        self.hsrv_firm_check_button.clicked.connect(self.send_hsrv_firm_check_ready)
        self.vsrv_firm_check_button.clicked.connect(self.send_vsrv_firm_check_ready)
        self.ultrasonic_firm_check_button.clicked.connect(self.send_ultrasonic_firm_check_ready)
        self.rocker_firm_check_button.clicked.connect(self.send_rocker_firm_check_ready)
        self.temperature_firm_check_button.clicked.connect(self.send_temperature_firm_check_ready)
        self.voice_firm_check_button.clicked.connect(self.send_voice_firm_check_ready)
        self.p2p_firm_check_button.clicked.connect(self.send_P2P_firm_check_ready)
        self.led_board_firm_check_button.clicked.connect(self.send_led_board_firm_check_ready)
        self.pyroelectric_firm_check_button.clicked.connect(self.send_pyroelectric_firm_check_ready)
        self.main_firm_check_button.clicked.connect(self.send_main_firm_check_ready)

        self.encryption_button.clicked.connect(self.encryption_firmware)
        self.decrypt_button.clicked.connect(self.decrypt_firmware)
        self.sel_file_button.clicked.connect(self.send_firmware_file)
        # 定时发送数据
        self.timer_send = QTimer()
        self.timer_send.timeout.connect(self.data_send)
        self.timer_send_cb.stateChanged.connect(self.data_send_timer)

        # 定时器接收数据
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.data_receive)
        #发送固件线程
        self.rec_thread = firmware_thread(self)
        self.rec_thread.update_UI_signal.connect(self.signal_process)
        #加密线程
        self.encrypt_thread = aes_encrypt_thread(self)
        self.encrypt_thread.update_UI_signal.connect(self.encrypt_signal_process)
        #解密线程
        self.decrypt_thread = aes_decrypt_thread(self)
        self.decrypt_thread.update_UI_signal.connect(self.decrypt_signal_process)
        # 清除发送窗口
        self.s3__clear_button.clicked.connect(self.send_data_clear)

        # 清除接收窗口
        self.s2__clear_button.clicked.connect(self.receive_data_clear)
        # 清除LOG窗口
        self.log_clear_button.clicked.connect(self.log_text_clear)
    def get_send_firmware_state(self):
        return self.send_firmware_state

    def set_send_firmware_state(self,state):
        self.send_firmware_state = state 

    def get_send_firmware_ack(self):
        return self.send_firmware_ack
    def set_send_firmware_ack(self,ack):
        self.send_firmware_ack = ack
    # 串口检测
    def port_check(self):
        # 检测所有存在的串口，将信息存储在字典中
        self.Com_Dict = {}
        port_list = list(serial.tools.list_ports.comports())
        self.s1__box_2.clear()
        for port in port_list:
            self.Com_Dict["%s" % port[0]] = "%s" % port[1]
            self.s1__box_2.addItem(port[0])
        
        if len(self.Com_Dict) == 0:
            self.state_label.setText(" 无串口")
        elif ('port' in self.serial_config_dict) and (self.serial_config_dict['port'] in self.Com_Dict):
            self.s1__box_2.setCurrentText(self.serial_config_dict['port'])
            self.s1__box_3.setCurrentText(self.serial_config_dict['baudrate'])
            self.s1__box_4.setCurrentText(self.serial_config_dict['bytesize'])
            self.s1__box_6.setCurrentText(self.serial_config_dict['stopbits'])
            self.s1__box_5.setCurrentText(self.serial_config_dict['parity'])
    # 串口信息
    def port_imf(self):
        # 显示选定的串口的详细信息
        imf_s = self.s1__box_2.currentText()
        if imf_s != "":
            self.state_label.setText(self.Com_Dict[self.s1__box_2.currentText()])

    # 打开串口
    def port_open(self):
        self.ser.port = self.s1__box_2.currentText()
        self.ser.baudrate = int(self.s1__box_3.currentText())
        self.ser.bytesize = int(self.s1__box_4.currentText())
        self.ser.stopbits = int(self.s1__box_6.currentText())
        self.ser.parity = self.s1__box_5.currentText()

        try:
            self.ser.open()
        except:
            QMessageBox.critical(self, "Port Error", "此串口不能被打开！")
            return None

        
        # 打开串口接收定时器，周期为2ms
        self.timer.start(2)
        
        if self.ser.isOpen():
            self.open_button.setEnabled(False)
            self.close_button.setEnabled(True)
            self.formGroupBox1.setTitle("串口状态（已开启）")
        
        #save config to json
        self.serial_config_dict.update(port=self.ser.port)
        self.serial_config_dict.update(baudrate=self.s1__box_3.currentText())
        self.serial_config_dict.update(bytesize=self.s1__box_4.currentText())
        self.serial_config_dict.update(stopbits=self.s1__box_6.currentText())
        self.serial_config_dict.update(parity=self.ser.parity)
        try:
            self.configfile.close()
            os.remove('.config')#清除源文件
            self.configfile = open('.config','a+')
            self.configfile.write(json.dumps(self.serial_config_dict))#write to .config file
            self.configfile.flush()
        except :
            pass
    # 关闭串口
    def port_close(self):
        if self.rec_thread.isRunning():
            print('thread runing')
            self.rec_thread.exit(23)
        self.timer.stop()
        self.timer_send.stop()
        try:
            self.ser.close()
        except:
            pass
        self.open_button.setEnabled(True)
        self.close_button.setEnabled(False)
        self.lineEdit_3.setEnabled(True)
        # 接收数据和发送数据数目置零
        self.data_num_received = 0
        self.lineEdit.setText(str(self.data_num_received))
        self.data_num_sended = 0
        self.lineEdit_2.setText(str(self.data_num_sended))
        self.formGroupBox1.setTitle("串口状态（已关闭）")
        self.configfile.close()
    #关闭窗口回调
    def closeEvent(self,QCloseEvent):
        if self.encrypt_thread.isRunning():
            self.encrypt_thread.exit(21)
        if self.decrypt_thread.isRunning():
            self.decrypt_thread.exit(22)
        self.port_close()

    def add_crc_to_send(self):
        input_s = self.s3__send_text.toPlainText()
        if input_s != "":
            # 非空字符串
            if self.hex_send.isChecked():
                # hex发送
                input_s = input_s.strip()
                send_list = []
                while input_s != '':
                    try:
                        num = int(input_s[0:2], 16)
                    except ValueError:
                        QMessageBox.critical(self, 'wrong data', '请输入十六进制数据，以空格分开!')
                        return None
                    input_s = input_s[2:].strip()
                    send_list.append(num)
                crc_result = crc16(send_list,len(send_list))
                send_list.append(crc_result & 0xff)
                send_list.append((crc_result >> 8) & 0xff)
                self.s3__send_text.clear()
                max_len = len(send_list)
                for i in range(0,max_len):
                    if send_list[i] > 0x0f:        
                        temp = hex(send_list[i])
                        self.s3__send_text.insertPlainText(temp[2:])
                    else:
                        temp = hex(send_list[i])
                        self.s3__send_text.insertPlainText('0')
                        self.s3__send_text.insertPlainText(temp[2:])
                    if i < max_len-1:
                        self.s3__send_text.insertPlainText(' ')
            else:
                QMessageBox.critical(self, 'worning', 'hex 模式才能校验crc')  

        else:
            QMessageBox.critical(self, 'worning', '发送区为空无!')  
    # 发送数据
    def data_send(self):
        if self.ser.isOpen():
            input_s = self.s3__send_text.toPlainText()
            if input_s != "":
                # 非空字符串
                if self.hex_send.isChecked():
                    # hex发送
                    input_s = input_s.strip()
                    send_list = []
                    while input_s != '':
                        try:
                            num = int(input_s[0:2], 16)
                        except ValueError:
                            QMessageBox.critical(self, 'wrong data', '请输入十六进制数据，以空格分开!')
                            return None
                        input_s = input_s[2:].strip()
                        send_list.append(num)
                    input_s = bytes(send_list)
                else:
                    # ascii发送
                    input_s = (input_s + '\r\n').encode('utf-8')

                num = self.ser.write(input_s)
                self.data_num_sended += num
                self.lineEdit_2.setText(str(self.data_num_sended))
        else:
            pass
    #发送红外球升级准备
    def send_infrared_update_ready(self):
        if self.ser.isOpen():
            send_list = [0xfe,0x0e,0x01,0xf3,0x00]
            crcresult = crc16(send_list,3)
            send_list[3] = (crcresult & 0xff)
            send_list[4] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #发送颜色球升级准备
    def send_color_update_ready(self):
        if self.ser.isOpen():
            send_list = [0xfd,0x0e,0x01,0xf3,0x00]
            crcresult = crc16(send_list,3)
            send_list[3] = (crcresult & 0xff)
            send_list[4] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #发送触碰球升级准备
    def send_touch_update_ready(self):
        if self.ser.isOpen():
            send_list = [0xfa,0x0e,0x01,0xf3,0x00]
            crcresult = crc16(send_list,3)
            send_list[3] = (crcresult & 0xff)
            send_list[4] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #发送驱动球升级准备
    def send_driver_update_ready(self):
        if self.ser.isOpen():
            send_list = [0xfc,0x0e,0x01,0xf3,0x00]
            crcresult = crc16(send_list,3)
            send_list[3] = (crcresult & 0xff)
            send_list[4] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #发送水平球升级准备
    def send_hsrv_update_ready(self):
        if self.ser.isOpen():
            send_list = [0xf9,0x0e,0x01,0xf3,0x00]
            crcresult = crc16(send_list,3)
            send_list[3] = (crcresult & 0xff)
            send_list[4] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #发送摇摆球升级准备
    def send_vsrv_update_ready(self):
        if self.ser.isOpen():
            send_list = [0xf8,0x0e,0x01,0xf3,0x00]
            crcresult = crc16(send_list,3)
            send_list[3] = (crcresult & 0xff)
            send_list[4] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #发送超声波球升级准备
    def send_ultrasonic_update_ready(self):
        if self.ser.isOpen():
            send_list = [0xf7,0x0e,0x01,0xf3,0x00]
            crcresult = crc16(send_list,3)
            send_list[3] = (crcresult & 0xff)
            send_list[4] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #发送摇杆球升级准备
    def send_rocker_update_ready(self):
        if self.ser.isOpen():
            send_list = [0xf6,0x0e,0x01,0xf3,0x00]
            crcresult = crc16(send_list,3)
            send_list[3] = (crcresult & 0xff)
            send_list[4] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #发送温度球升级准备
    def send_temperature_update_ready(self):
        if self.ser.isOpen():
            send_list = [0xf5,0x0e,0x01,0xf3,0x00]
            crcresult = crc16(send_list,3)
            send_list[3] = (crcresult & 0xff)
            send_list[4] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #发送声音球升级准备
    def send_voice_update_ready(self):
        if self.ser.isOpen():
            send_list = [0xf4,0x0e,0x01,0xf3,0x00]
            crcresult = crc16(send_list,3)
            send_list[3] = (crcresult & 0xff)
            send_list[4] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #发送P2P球升级准备
    def send_P2P_update_ready(self):
        if self.ser.isOpen():
            send_list = [0xf3,0x0e,0x01,0xf3,0x00]
            crcresult = crc16(send_list,3)
            send_list[3] = (crcresult & 0xff)
            send_list[4] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #发送led板球升级准备
    def send_led_board_update_ready(self):
        if self.ser.isOpen():
            send_list = [0xf2,0x0e,0x01,0xf3,0x00]
            crcresult = crc16(send_list,3)
            send_list[3] = (crcresult & 0xff)
            send_list[4] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #发送热释电球升级准备
    def send_pyroelectric_update_ready(self):
        if self.ser.isOpen():
            send_list = [0xf1,0x0e,0x01,0xf3,0x00]
            crcresult = crc16(send_list,3)
            send_list[3] = (crcresult & 0xff)
            send_list[4] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #发送主控球升级准备
    def send_main_update_ready(self):
        if self.ser.isOpen():
            send_list = [0xff,0x0e,0x00,0x00,0xf3,0x00]
            crcresult = crc16(send_list,4)
            send_list[4] = (crcresult & 0xff)
            send_list[5] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
########################################查询##################################################
    #发送红外球固件查询
    def send_infrared_firm_check_ready(self):
        if self.ser.isOpen():
            module = int(self.sel_check_module.currentText())
            send_list = [0xfe,0xee,module,0xf3,0x00]
            crcresult = crc16(send_list,3)
            send_list[3] = (crcresult & 0xff)
            send_list[4] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #发送颜色球固件查询
    def send_color_firm_check_ready(self):
        if self.ser.isOpen():
            module = int(self.sel_check_module.currentText())
            send_list = [0xfd,0xee,module,0xf3,0x00]
            crcresult = crc16(send_list,3)
            send_list[3] = (crcresult & 0xff)
            send_list[4] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #发送触碰球固件查询
    def send_touch_firm_check_ready(self):
        if self.ser.isOpen():
            module = int(self.sel_check_module.currentText())
            send_list = [0xfa,0xee,module,0xf3,0x00]
            crcresult = crc16(send_list,3)
            send_list[3] = (crcresult & 0xff)
            send_list[4] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #发送驱动球固件查询
    def send_driver_firm_check_ready(self):
        if self.ser.isOpen():
            module = int(self.sel_check_module.currentText())
            send_list = [0xfc,0xee,module,0xf3,0x00]
            crcresult = crc16(send_list,3)
            send_list[3] = (crcresult & 0xff)
            send_list[4] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #发送水平球固件查询
    def send_hsrv_firm_check_ready(self):
        if self.ser.isOpen():
            module = int(self.sel_check_module.currentText())
            send_list = [0xf9,0xee,module,0xf3,0x00]
            crcresult = crc16(send_list,3)
            send_list[3] = (crcresult & 0xff)
            send_list[4] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #发送摇摆球升固件查询
    def send_vsrv_firm_check_ready(self):
        if self.ser.isOpen():
            module = int(self.sel_check_module.currentText())
            send_list = [0xf8,0xee,module,0xf3,0x00]
            crcresult = crc16(send_list,3)
            send_list[3] = (crcresult & 0xff)
            send_list[4] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #发送超声波球固件查询
    def send_ultrasonic_firm_check_ready(self):
        if self.ser.isOpen():
            module = int(self.sel_check_module.currentText())
            send_list = [0xf7,0xee,module,0xf3,0x00]
            crcresult = crc16(send_list,3)
            send_list[3] = (crcresult & 0xff)
            send_list[4] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #发送摇杆球固件查询
    def send_rocker_firm_check_ready(self):
        if self.ser.isOpen():
            module = int(self.sel_check_module.currentText())
            send_list = [0xf6,0xee,module,0xf3,0x00]
            crcresult = crc16(send_list,3)
            send_list[3] = (crcresult & 0xff)
            send_list[4] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #发送温度球固件查询
    def send_temperature_firm_check_ready(self):
        if self.ser.isOpen():
            module = int(self.sel_check_module.currentText())
            send_list = [0xf5,0xee,module,0xf3,0x00]
            crcresult = crc16(send_list,3)
            send_list[3] = (crcresult & 0xff)
            send_list[4] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #发送声音球固件查询
    def send_voice_firm_check_ready(self):
        if self.ser.isOpen():
            module = int(self.sel_check_module.currentText())
            send_list = [0xf4,0xee,module,0xf3,0x00]
            crcresult = crc16(send_list,3)
            send_list[3] = (crcresult & 0xff)
            send_list[4] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #发送P2P球固件查询
    def send_P2P_firm_check_ready(self):
        if self.ser.isOpen():
            module = int(self.sel_check_module.currentText())
            send_list = [0xf3,0xee,module,0xf3,0x00]
            crcresult = crc16(send_list,3)
            send_list[3] = (crcresult & 0xff)
            send_list[4] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #发送led板球固件查询
    def send_led_board_firm_check_ready(self):
        if self.ser.isOpen():
            module = int(self.sel_check_module.currentText())
            send_list = [0xf2,0xee,module,0xf3,0x00]
            crcresult = crc16(send_list,3)
            send_list[3] = (crcresult & 0xff)
            send_list[4] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #发送热释电球固件查询
    def send_pyroelectric_firm_check_ready(self):
        if self.ser.isOpen():
            module = int(self.sel_check_module.currentText())
            send_list = [0xf1,0xee,module,0xf3,0x00]
            crcresult = crc16(send_list,3)
            send_list[3] = (crcresult & 0xff)
            send_list[4] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #发送主控球固件查询
    def send_main_firm_check_ready(self):
        if self.ser.isOpen():
            send_list = [0xff,0xee,0xf3,0x00]
            crcresult = crc16(send_list,2)
            send_list[2] = (crcresult & 0xff)
            send_list[3] = ((crcresult >> 8) & 0xff)
            input_s = bytes(send_list)
            self.ser.write(input_s)
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    #加密文件
    def encryption_firmware(self):
        if ('encryptfile' in self.serial_config_dict != None):
            self.encrypt_file_name = QFileDialog.getOpenFileName(self,"选取文件",self.serial_config_dict['encryptfile'],"All Files (*)")
        else:
            self.encrypt_file_name = QFileDialog.getOpenFileName(self,"选取文件","./","All Files (*)")
        if self.encrypt_file_name[0] == '':#未打开文件
            #print('取消加密')
            return

        self.serial_config_dict.update(encryptfile=self.encrypt_file_name[0])#打开文件后保存到配置文件中
        try:   
            self.configfile.close()
            os.remove('.config')#清除源文件
            self.configfile = open('.config','a+')
            self.json_str = json.dumps(self.serial_config_dict)
            self.configfile.write(self.json_str)#write to .config file
            self.configfile.flush()
        except:
            pass
        self.encrypt_thread.start()
        #QMessageBox.critical(self, 'wrong data', '这个功能还没做')
    #解密文件
    def decrypt_firmware(self):
        if ('encryptfile' in self.serial_config_dict != None):
            self.decrypt_file_name = QFileDialog.getOpenFileName(self,"选取文件",self.serial_config_dict['encryptfile'],"All Files (*)")
        else:
            self.decrypt_file_name = QFileDialog.getOpenFileName(self,"选取文件","./","All Files (*)")
        if self.decrypt_file_name[0] == '':
            #print('取消解密')
            return

        self.serial_config_dict.update(encryptfile=self.decrypt_file_name[0])
        try:  
            self.configfile.close()
            os.remove('.config')#清除源文件
            self.configfile = open('.config','a+')
            self.json_str = json.dumps(self.serial_config_dict)
            self.configfile.write(self.json_str)#write to .config file
            self.configfile.flush()
        except:
            pass
        self.decrypt_thread.start()
        #QMessageBox.critical(self, 'wrong data', '这个功能还没做')

    #发送固件
    def send_firmware_file(self):
        if self.ser.isOpen(): 
            #if self.serial_config_dict.get('firmware',default=None) != None:
            if ('firmware' in self.serial_config_dict != None):
                self.file_name = QFileDialog.getOpenFileName(self,"选取文件",self.serial_config_dict['firmware'],"All Files (*)")
            else:
                self.file_name = QFileDialog.getOpenFileName(self,"选取文件","./","All Files (*)")
            self.sector_len = int(self.dw_send_sector_editor.text())

            if self.file_name[0] == '' or self.sector_len == 0 :#未打开文件
                return
            self.serial_config_dict.update(firmware=self.file_name[0])
            try:  
                self.configfile.close()
                os.remove('.config')#清除源文件
                self.configfile = open('.config','a+')
                self.json_str = json.dumps(self.serial_config_dict)
                self.configfile.write(self.json_str)#write to .config file
                self.configfile.flush()
            except:
                pass
            self.rec_thread.start()
            
           # QMessageBox.critical(self, 'wrong data', '这个功能还没做')
        else:
            QMessageBox.critical(self, 'wrong data', '串口没有打开')
    
    def data_receive(self):
        try:
            num = self.ser.inWaiting()
        except:
            self.port_close()
            return None
        if num > 0:
            data = self.ser.read(num)
            num = len(data)
            send_firmware_ack_result = []
            send_firmware_ack_result.clear()
            for i in range(0, len(data)):
                send_firmware_ack_result.append(int(data[i]))
            if self.send_firmware_state == SEND_FIRMWARE_STATE_START :#发送起始帧状态
                if send_firmware_ack_result[2] == 0:
                    self.send_firmware_ack = SEND_FIRMWARE_ACK_OK
                elif send_firmware_ack_result[2] == 100:
                    self.send_firmware_ack = SEND_FIRMWARE_ACK_FAIL
                #print(send_firmware_ack_result,num,'\n')
            elif self.send_firmware_state == SEND_FIRMWARE_STATE_DATA :#发送数据帧状态
                if send_firmware_ack_result[2] == 0:
                    self.send_firmware_ack = SEND_FIRMWARE_ACK_OK
                elif send_firmware_ack_result[2] == 100:
                    self.send_firmware_ack = SEND_FIRMWARE_ACK_FAIL
                #print(send_firmware_ack_result,num,'\n')
            elif self.send_firmware_state == SEND_FIRMWARE_STATE_END :#发送结束帧状态
                if send_firmware_ack_result[2] == 0:
                    self.send_firmware_ack = SEND_FIRMWARE_ACK_OK
                elif send_firmware_ack_result[2] == 100:
                    self.send_firmware_ack = SEND_FIRMWARE_ACK_FAIL
                #print(send_firmware_ack_result,num,'\n')
            
            # hex显示
            if self.hex_receive.checkState():
                out_s = ''
                for i in range(0, len(data)):
                    out_s = out_s + '{:02X}'.format(data[i]) + ' '
                self.s2__receive_text.insertPlainText(out_s)
            else:
                # 串口接收到的字符串为b'123',要转化成unicode字符串才能输出到窗口中去
                self.s2__receive_text.insertPlainText(data.decode('iso-8859-1'))

            # 统计接收字符的数量
            self.data_num_received += num
            self.lineEdit.setText(str(self.data_num_received))
            # 获取到text光标
            textCursor = self.s2__receive_text.textCursor()
            # 滚动到底部
            textCursor.movePosition(textCursor.End)
            # 设置光标到text中去
            self.s2__receive_text.setTextCursor(textCursor)
        
        else:
            pass
    # 定时发送数据
    def data_send_timer(self):
        if self.timer_send_cb.isChecked():
            self.timer_send.start(int(self.lineEdit_3.text()))
            self.lineEdit_3.setEnabled(False)
        else:
            self.timer_send.stop()
            self.lineEdit_3.setEnabled(True)

    # 清除显示
    def send_data_clear(self):
        self.s3__send_text.setText("")

    def receive_data_clear(self):
        self.s2__receive_text.setText("")
    
    def log_text_clear(self):
        self.log_text.setText("")
    def signal_process(self,str):
        self.log_text.insertPlainText(str)
        textCursor = self.log_text.textCursor()
        textCursor.movePosition(textCursor.End)
        self.log_text.setTextCursor(textCursor)
    def encrypt_signal_process(self,str):
        self.log_text.insertPlainText(str)
        textCursor = self.log_text.textCursor()
        textCursor.movePosition(textCursor.End)
        self.log_text.setTextCursor(textCursor)
    def decrypt_signal_process(self,str):
        self.log_text.insertPlainText(str)
        textCursor = self.log_text.textCursor()
        textCursor.movePosition(textCursor.End)
        self.log_text.setTextCursor(textCursor)
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myshow = Pyqt5_Serial()
    myshow.show()
    sys.exit(app.exec_())
