# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'demo_1.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1000, 700)
        self.formGroupBox = QtWidgets.QGroupBox(Form)
        self.formGroupBox.setGeometry(QtCore.QRect(20, 20, 167, 301))
        self.formGroupBox.setObjectName("formGroupBox")
        self.formLayout = QtWidgets.QFormLayout(self.formGroupBox)
        self.formLayout.setContentsMargins(10, 10, 10, 10)
        self.formLayout.setSpacing(10)
        self.formLayout.setObjectName("formLayout")
        self.s1__lb_1 = QtWidgets.QLabel(self.formGroupBox)
        self.s1__lb_1.setObjectName("s1__lb_1")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.s1__lb_1)
        self.s1__box_1 = QtWidgets.QPushButton(self.formGroupBox)
        self.s1__box_1.setAutoRepeatInterval(100)
        self.s1__box_1.setDefault(True)
        self.s1__box_1.setObjectName("s1__box_1")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.s1__box_1)
        self.s1__lb_2 = QtWidgets.QLabel(self.formGroupBox)
        self.s1__lb_2.setObjectName("s1__lb_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.s1__lb_2)
        self.s1__box_2 = QtWidgets.QComboBox(self.formGroupBox)
        self.s1__box_2.setObjectName("s1__box_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.s1__box_2)
        self.s1__lb_3 = QtWidgets.QLabel(self.formGroupBox)
        self.s1__lb_3.setObjectName("s1__lb_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.s1__lb_3)
        self.s1__box_3 = QtWidgets.QComboBox(self.formGroupBox)
        self.s1__box_3.setObjectName("s1__box_3")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.s1__box_3)
        self.s1__lb_4 = QtWidgets.QLabel(self.formGroupBox)
        self.s1__lb_4.setObjectName("s1__lb_4")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.s1__lb_4)
        self.s1__box_4 = QtWidgets.QComboBox(self.formGroupBox)
        self.s1__box_4.setObjectName("s1__box_4")
        self.s1__box_4.addItem("")
        self.s1__box_4.addItem("")
        self.s1__box_4.addItem("")
        self.s1__box_4.addItem("")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.s1__box_4)
        self.s1__lb_5 = QtWidgets.QLabel(self.formGroupBox)
        self.s1__lb_5.setObjectName("s1__lb_5")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.s1__lb_5)
        self.s1__box_5 = QtWidgets.QComboBox(self.formGroupBox)
        self.s1__box_5.setObjectName("s1__box_5")
        self.s1__box_5.addItem("")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.s1__box_5)
        self.open_button = QtWidgets.QPushButton(self.formGroupBox)
        self.open_button.setObjectName("open_button")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.SpanningRole, self.open_button)
        self.close_button = QtWidgets.QPushButton(self.formGroupBox)
        self.close_button.setObjectName("close_button")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.close_button)
        self.s1__lb_6 = QtWidgets.QLabel(self.formGroupBox)
        self.s1__lb_6.setObjectName("s1__lb_6")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.s1__lb_6)
        self.s1__box_6 = QtWidgets.QComboBox(self.formGroupBox)
        self.s1__box_6.setObjectName("s1__box_6")
        self.s1__box_6.addItem("")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.s1__box_6)
        self.state_label = QtWidgets.QLabel(self.formGroupBox)
        self.state_label.setText("")
        self.state_label.setTextFormat(QtCore.Qt.AutoText)
        self.state_label.setScaledContents(True)
        self.state_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.state_label.setObjectName("state_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.state_label)
        self.verticalGroupBox = QtWidgets.QGroupBox(Form)
        self.verticalGroupBox.setGeometry(QtCore.QRect(210, 20, 401, 241))
        self.verticalGroupBox.setObjectName("verticalGroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalGroupBox)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.s2__receive_text = QtWidgets.QTextBrowser(self.verticalGroupBox)
        self.s2__receive_text.setObjectName("s2__receive_text")
        self.verticalLayout.addWidget(self.s2__receive_text)
        self.verticalGroupBox_2 = QtWidgets.QGroupBox(Form)
        self.verticalGroupBox_2.setGeometry(QtCore.QRect(210, 280, 401, 101))
        self.verticalGroupBox_2.setObjectName("verticalGroupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalGroupBox_2)
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.s3__send_text = QtWidgets.QTextEdit(self.verticalGroupBox_2)
        self.s3__send_text.setObjectName("s3__send_text")
        self.verticalLayout_2.addWidget(self.s3__send_text)
        self.s3__send_button = QtWidgets.QPushButton(Form)
        self.s3__send_button.setGeometry(QtCore.QRect(620, 310, 61, 31))
        self.s3__send_button.setObjectName("s3__send_button")
        self.s3__clear_button = QtWidgets.QPushButton(Form)
        self.s3__clear_button.setGeometry(QtCore.QRect(620, 350, 61, 31))
        self.s3__clear_button.setObjectName("s3__clear_button")
        self.formGroupBox1 = QtWidgets.QGroupBox(Form)
        self.formGroupBox1.setGeometry(QtCore.QRect(20, 340, 171, 101))
        self.formGroupBox1.setObjectName("formGroupBox1")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formGroupBox1)
        self.formLayout_2.setContentsMargins(10, 10, 10, 10)
        self.formLayout_2.setSpacing(10)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label = QtWidgets.QLabel(self.formGroupBox1)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(self.formGroupBox1)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(self.formGroupBox1)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.formGroupBox1)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.hex_send = QtWidgets.QCheckBox(Form)
        self.hex_send.setGeometry(QtCore.QRect(620, 280, 71, 16))
        self.hex_send.setObjectName("hex_send")
        self.hex_receive = QtWidgets.QCheckBox(Form)
        self.hex_receive.setGeometry(QtCore.QRect(620, 40, 71, 16))
        self.hex_receive.setObjectName("hex_receive")
        self.hex_receive.setChecked(True)#默认HEX接收
        self.s2__clear_button = QtWidgets.QPushButton(Form)
        self.s2__clear_button.setGeometry(QtCore.QRect(620, 80, 61, 31))
        self.s2__clear_button.setObjectName("s2__clear_button")
        self.timer_send_cb = QtWidgets.QCheckBox(Form)
        self.timer_send_cb.setGeometry(QtCore.QRect(260, 390, 71, 16))
        self.timer_send_cb.setObjectName("timer_send_cb")
        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(350, 390, 61, 20))
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.dw = QtWidgets.QLabel(Form)
        self.dw.setGeometry(QtCore.QRect(420, 390, 54, 20))
        self.dw.setObjectName("dw")

        self.add_crc_button = QtWidgets.QPushButton(Form)
        self.add_crc_button.setGeometry(QtCore.QRect(500, 385, 64, 30))
        self.add_crc_button.setObjectName("s3__send_button")
        #function box
        self.verticalGroupBox_func = QtWidgets.QGroupBox(Form)
        self.verticalGroupBox_func.setGeometry(QtCore.QRect(700, 20, 280, 660))
        self.verticalGroupBox_func.setObjectName("verticalGroupBox_func")
        
        #function button
        #self.verticalGroupBox_func.setSpacing(10)
        self.infrared_update_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#红外球
        self.infrared_update_button.setGeometry(10,20,80,30)
        #self.infrared_update_button.move(10,20)
        self.color_update_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#颜色球
        self.color_update_button.setGeometry(10,60,80,30)
        self.touch_update_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#触碰球
        self.touch_update_button.setGeometry(10,100,80,30)
        self.driver_update_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#驱动球
        self.driver_update_button.setGeometry(10,140,80,30)
        self.hsrv_update_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#水平球
        self.hsrv_update_button.setGeometry(10,180,80,30)
        self.vsrv_update_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#摇摆球
        self.vsrv_update_button.setGeometry(10,220,80,30)
        self.ultrasonic_update_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#超声波球
        self.ultrasonic_update_button.setGeometry(10,260,80,30)
        self.rocker_update_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#摇杆球
        self.rocker_update_button.setGeometry(10,300,80,30)
        self.temperature_update_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#温度球
        self.temperature_update_button.setGeometry(10,340,80,30)
        self.voice_update_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#声音球
        self.voice_update_button.setGeometry(10,380,80,30)
        self.p2p_update_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#P2P球
        self.p2p_update_button.setGeometry(10,420,80,30)
        self.led_board_update_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#LED球
        self.led_board_update_button.setGeometry(10,460,80,30)
        self.pyroelectric_update_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#热释电球
        self.pyroelectric_update_button.setGeometry(10,500,80,30)
        self.main_update_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#主控球
        self.main_update_button.setGeometry(10,540,80,30)
        self.infrared_firm_check_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#红外球
        self.infrared_firm_check_button.setGeometry(100,20,100,30)
        self.color_firm_check_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#颜色球
        self.color_firm_check_button.setGeometry(100,60,100,30)
        self.touch_firm_check_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#触碰球
        self.touch_firm_check_button.setGeometry(100,100,100,30)
        self.driver_firm_check_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#驱动球
        self.driver_firm_check_button.setGeometry(100,140,100,30)
        self.hsrv_firm_check_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#水平球
        self.hsrv_firm_check_button.setGeometry(100,180,100,30)
        self.vsrv_firm_check_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#摇摆球
        self.vsrv_firm_check_button.setGeometry(100,220,100,30)
        self.ultrasonic_firm_check_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#超声波球
        self.ultrasonic_firm_check_button.setGeometry(100,260,100,30)
        self.rocker_firm_check_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#摇杆球
        self.rocker_firm_check_button.setGeometry(100,300,100,30)
        self.temperature_firm_check_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#温度球
        self.temperature_firm_check_button.setGeometry(100,340,100,30)
        self.voice_firm_check_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#声音球
        self.voice_firm_check_button.setGeometry(100,380,100,30)
        self.p2p_firm_check_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#P2P球
        self.p2p_firm_check_button.setGeometry(100,420,100,30)
        self.led_board_firm_check_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#LED球
        self.led_board_firm_check_button.setGeometry(100,460,100,30)
        self.pyroelectric_firm_check_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#热释电球
        self.pyroelectric_firm_check_button.setGeometry(100,500,100,30)
        self.main_firm_check_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#主控球
        self.main_firm_check_button.setGeometry(100,540,100,30)

        self.dw_send_sector_editor = QtWidgets.QLineEdit(self.verticalGroupBox_func)
        self.dw_send_sector_editor.move(105,580)
        self.dw_send_sector = QtWidgets.QLabel(self.verticalGroupBox_func)#发送分段大小设置
        self.dw_send_sector.move(10,585)
        self.encryption_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#加密文件
        self.encryption_button.move(10,620)
        self.decrypt_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#解密文件
        self.decrypt_button.move(100,620)
        self.sel_file_button = QtWidgets.QPushButton(self.verticalGroupBox_func)#选择文件
        self.sel_file_button.move(190,620)

        self.sel_check_module = QtWidgets.QComboBox(self.verticalGroupBox_func)
        self.sel_check_module.setObjectName("sel_check_module")
        self.sel_check_module.addItem("")
        self.sel_check_module.addItem("")
        self.sel_check_module.addItem("")
        self.sel_check_module.addItem("")
        self.sel_check_module.addItem("")
        self.sel_check_module.addItem("")
        self.sel_check_module.addItem("")
        self.sel_check_module.addItem("")
        self.sel_check_module.addItem("")
        self.sel_check_module.addItem("")
        self.sel_check_module.addItem("")
        self.sel_check_module.addItem("")
        self.sel_check_module.addItem("")
        self.sel_check_module.addItem("")
        self.sel_check_module.addItem("")
        self.sel_check_module.setGeometry(210,20,60,30)
        #log box
        self.verticalGroupBox_log = QtWidgets.QGroupBox(Form)
        self.verticalGroupBox_log.setGeometry(QtCore.QRect(210, 420, 401, 260))
        self.verticalGroupBox_log.setObjectName("verticalGroupBox_log")
        self.log_text = QtWidgets.QTextBrowser(self.verticalGroupBox_log)
        self.log_text.move(10,20)
        self.log_text.resize(381,230)
        self.log_text.setObjectName("log_text")
        self.log_clear_button = QtWidgets.QPushButton(Form)
        self.log_clear_button.setGeometry(QtCore.QRect(620, 440, 61, 31))
        self.log_clear_button.setObjectName("log_clear_button")

        self.verticalGroupBox_func.raise_()
        self.verticalGroupBox.raise_()
        self.verticalGroupBox_2.raise_()
        self.formGroupBox.raise_()
        self.s3__send_button.raise_()
        self.add_crc_button.raise_()
        self.s3__clear_button.raise_()
        self.formGroupBox.raise_()
        self.hex_send.raise_()
        self.hex_receive.raise_()
        self.s2__clear_button.raise_()
        self.log_clear_button.raise_()
        self.timer_send_cb.raise_()
        self.lineEdit_3.raise_()
        self.dw.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.formGroupBox.setTitle(_translate("Form", "串口设置"))
        self.s1__lb_1.setText(_translate("Form", "串口检测："))
        self.s1__box_1.setText(_translate("Form", "检测串口"))
        self.s1__lb_2.setText(_translate("Form", "串口选择："))
        self.s1__lb_3.setText(_translate("Form", "波特率："))

        self.s1__box_3.setItemText(0, _translate("Form", "115200"))
        self.s1__box_3.setItemText(1, _translate("Form", "2400"))
        self.s1__box_3.setItemText(2, _translate("Form", "4800"))
        self.s1__box_3.setItemText(3, _translate("Form", "9600"))
        self.s1__box_3.setItemText(4, _translate("Form", "14400"))
        self.s1__box_3.setItemText(5, _translate("Form", "19200"))
        self.s1__box_3.setItemText(6, _translate("Form", "38400"))
        self.s1__box_3.setItemText(7, _translate("Form", "57600"))
        self.s1__box_3.setItemText(8, _translate("Form", "76800"))
        self.s1__box_3.setItemText(9, _translate("Form", "12800"))
        self.s1__box_3.setItemText(10, _translate("Form", "230400"))
        self.s1__box_3.setItemText(11, _translate("Form", "460800"))
        self.s1__lb_4.setText(_translate("Form", "数据位："))
        self.s1__box_4.setItemText(0, _translate("Form", "8"))
        self.s1__box_4.setItemText(1, _translate("Form", "7"))
        self.s1__box_4.setItemText(2, _translate("Form", "6"))
        self.s1__box_4.setItemText(3, _translate("Form", "5"))
        self.s1__lb_5.setText(_translate("Form", "校验位："))
        self.s1__box_5.setItemText(0, _translate("Form", "N"))
        self.open_button.setText(_translate("Form", "打开串口"))
        self.close_button.setText(_translate("Form", "关闭串口"))
        self.s1__lb_6.setText(_translate("Form", "停止位："))
        self.s1__box_6.setItemText(0, _translate("Form", "1"))
        self.verticalGroupBox.setTitle(_translate("Form", "接受区"))
        self.verticalGroupBox_2.setTitle(_translate("Form", "发送区"))
        #function
        self.verticalGroupBox_func.setTitle(_translate("Form", "附加功能区"))
        self.infrared_update_button.setText(_translate("Form", "红外球升级"))#红外球
        self.color_update_button.setText(_translate("Form", "颜色球升级"))#颜色球
        self.touch_update_button.setText(_translate("Form", "触碰球升级"))#触碰球
        self.driver_update_button.setText(_translate("Form", "驱动球升级"))#驱动球
        self.hsrv_update_button.setText(_translate("Form", "水平球升级"))#水平球
        self.vsrv_update_button.setText(_translate("Form", "摇摆球升级"))#摇摆球
        self.ultrasonic_update_button.setText(_translate("Form", "超声波升级"))#超声波球
        self.rocker_update_button.setText(_translate("Form", "摇杆球升级"))#摇杆球
        self.temperature_update_button.setText(_translate("Form", "温度球升级"))#温度球
        self.voice_update_button.setText(_translate("Form", "声音球升级"))#声音球
        self.p2p_update_button.setText(_translate("Form", "P2P球升级"))#P2P球
        self.led_board_update_button.setText(_translate("Form", "LED球升级"))#LED球
        self.pyroelectric_update_button.setText(_translate("Form", "热释电升级"))#热释电球
        self.main_update_button.setText(_translate("Form", "主控球升级"))#主控球

        self.infrared_firm_check_button.setText(_translate("Form", "红外球固件查询"))#红外球
        self.color_firm_check_button.setText(_translate("Form", "颜色球固件查询"))#颜色球
        self.touch_firm_check_button.setText(_translate("Form", "触碰球固件查询"))#触碰球
        self.driver_firm_check_button.setText(_translate("Form", "驱动球固件查询"))#驱动球
        self.hsrv_firm_check_button.setText(_translate("Form", "水平球固件查询"))#水平球
        self.vsrv_firm_check_button.setText(_translate("Form", "摇摆球固件查询"))#摇摆球
        self.ultrasonic_firm_check_button.setText(_translate("Form", "超声波固件查询"))#超声波球
        self.rocker_firm_check_button.setText(_translate("Form", "摇杆球固件查询"))#摇杆球
        self.temperature_firm_check_button.setText(_translate("Form", "温度球固件查询"))#温度球
        self.voice_firm_check_button.setText(_translate("Form", "声音球固件查询"))#声音球
        self.p2p_firm_check_button.setText(_translate("Form", "P2P球固件查询"))#P2P球
        self.led_board_firm_check_button.setText(_translate("Form", "LED球固件查询"))#LED球
        self.pyroelectric_firm_check_button.setText(_translate("Form", "热释电固件查询"))#热释电球
        self.main_firm_check_button.setText(_translate("Form", "主控球固件查询"))#主控球

        self.dw_send_sector.setText(_translate("Form", "分段发送字节数:"))#主控球
        self.dw_send_sector_editor.setText(_translate("Form", "1024"))
        self.encryption_button.setText(_translate("Form", "加密文件"))#加密
        self.decrypt_button.setText(_translate("Form", "解密文件"))#解密
        self.sel_file_button.setText(_translate("Form", "发送固件"))#发送文件
        self.sel_check_module.setItemText(0, _translate("Form", "1"))
        self.sel_check_module.setItemText(1, _translate("Form", "2"))
        self.sel_check_module.setItemText(2, _translate("Form", "3"))
        self.sel_check_module.setItemText(3, _translate("Form", "4"))
        self.sel_check_module.setItemText(4, _translate("Form", "5"))
        self.sel_check_module.setItemText(5, _translate("Form", "6"))
        self.sel_check_module.setItemText(6, _translate("Form", "7"))
        self.sel_check_module.setItemText(7, _translate("Form", "8"))
        self.sel_check_module.setItemText(8, _translate("Form", "9"))
        self.sel_check_module.setItemText(9, _translate("Form", "10"))
        self.sel_check_module.setItemText(10, _translate("Form", "11"))
        self.sel_check_module.setItemText(11, _translate("Form", "12"))
        self.sel_check_module.setItemText(12, _translate("Form", "13"))
        self.sel_check_module.setItemText(13, _translate("Form", "14"))
        self.sel_check_module.setItemText(14, _translate("Form", "15"))
        #log
        self.verticalGroupBox_log.setTitle(_translate("Form", "LOG区"))

        self.s3__send_text.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">123456</p></body></html>"))
        self.s3__send_button.setText(_translate("Form", "发送"))
        self.s3__clear_button.setText(_translate("Form", "清除"))
        self.formGroupBox1.setTitle(_translate("Form", "串口状态"))
        self.label.setText(_translate("Form", "已接收："))
        self.label_2.setText(_translate("Form", "已发送："))
        self.hex_send.setText(_translate("Form", "Hex发送"))
        self.hex_receive.setText(_translate("Form", "Hex接收"))
        self.s2__clear_button.setText(_translate("Form", "清除"))
        self.log_clear_button.setText(_translate("Form", "清除"))
        self.timer_send_cb.setText(_translate("Form", "定时发送"))
        self.lineEdit_3.setText(_translate("Form", "1000"))
        self.dw.setText(_translate("Form", "ms/次"))
        self.add_crc_button.setText(_translate("Form", "添加crc"))

