# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import time
from PyQt5 import QtCore, QtGui, QtWidgets
from qfluentwidgets import FluentIcon, RoundMenu
import requests
import secrets
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading
import rsa
import base64
import socket

def get_available_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    addr, port = sock.getsockname()
    sock.close()
    return port

# 定义全局变量
global_state = "stop"
data = None
server_IP = sys.argv[1]
server_port = sys.argv[2]
roomid = sys.argv[3]
base_url = f"http://{server_IP}:{server_port}/api/device/client"
DEBOUNCE_TIME = 2000
port_global = get_available_port()

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global global_state
        global data
        # 获取请求体的长度
        content_length = int(self.headers["Content-Length"])
        # 读取请求体数据
        post_data = self.rfile.read(content_length)
        # 将请求体数据从 bytes 转换为 JSON
        data = json.loads(
            rsa.decrypt(
                base64.urlsafe_b64decode(post_data),
                rsa.PrivateKey.load_pkcs1(open("private.pem", "rb").read()),
            ).decode()
        )
        print(data)
        # 打印接收到的数据（或进行其他处理）
        # print("Received POST request with data:", data)

        # 发送响应
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {"status": "success"}
        self.wfile.write(json.dumps(response).encode("utf-8"))

def run_server(
    server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=port_global
):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()



class ui_Form(object):
    def __init__(self):
        super().__init__()

        self.menu = RoundMenu(parent=self)
        self.action_up = QtWidgets.QAction(FluentIcon.UP.icon(), "Up")
        self.action_down = QtWidgets.QAction(FluentIcon.DOWN.icon(), "Down")

        self.menu.addAction(self.action_up)
        self.menu.addAction(self.action_down)

        self.initial_temperature = 25
        self.current_temperature = 25
        self.temperature = 25
        self.speed = 2
        self.current_mode = "cold"
        self.sweep = "off"
        self.state = "stop"
        self.room_id = roomid 
        self.port = port_global
        self.temp_update_timer = QtCore.QTimer(self)
        self.temp_update_timer.setInterval(DEBOUNCE_TIME)
        self.temp_update_timer.timeout.connect(self.send_temperature_update)
        self.temp_update_timer.setSingleShot(True)  # 设置计时器为单次触发

        # 启动 HTTP 服务器线程
        threading.Thread(target=run_server, daemon=True).start()

        # 发送客户端上线请求
        self.client_online()

    def generate_unique_id(self):
        return secrets.token_hex(8)  # 生成 16 字符（8 字节）的十六进制字符串

    def get_available_port():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', 0))
        addr, port = sock.getsockname()
        sock.close()
        return port

    # def generate_rsa_key_pair(self):
    #     # 生成 RSA 密钥对
    #     private_key = rsa.generate_private_key(
    #         public_exponent=65537,
    #         key_size=4096,
    #     )
    #     public_key = private_key.public_key()

    #     return private_key, public_key

    def generate_signature(self, private_key, text):
        # 使用私钥生成签名
        signature = base64.urlsafe_b64encode(
            rsa.sign(text.encode(), private_key, "SHA-256")
        ).decode()
        return signature

    def client_online(self):
        port = self.port  # 示例端口号
        unique_id = self.generate_unique_id()  # 生成 unique_id
        private_key = rsa.PrivateKey.load_pkcs1(open("private.pem", "rb").read())
        signature = self.generate_signature(
            private_key, self.room_id + unique_id + str(port)
        )  # 生成 signature

        global base_url
        payload = {
            "room_id": self.room_id,
            "port": port,
            "unique_id": unique_id,
            "signature": signature,
        }
        response = requests.post(base_url, json=payload)
        if response.status_code == 204:
            print("Client Online successfully")
        else:
            print("Error:", response.status_code)
            exit(1)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(839, 410)
        self.PushButton = PushButton(Form)
        self.PushButton.setGeometry(QtCore.QRect(420, 290, 102, 32))
        self.PushButton.setObjectName("PushButton")
        self.SwitchButton = SwitchButton(Form)
        self.SwitchButton.setGeometry(QtCore.QRect(590, 300, 75, 22))
        self.SwitchButton.setObjectName("SwitchButton")
        self.ToolButton = ToolButton(Form)
        self.ToolButton.setGeometry(QtCore.QRect(230, 270, 38, 32))
        self.ToolButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.ToolButton.setAcceptDrops(False)
        self.ToolButton.setText("")
        self.ToolButton.setArrowType(QtCore.Qt.NoArrow)
        self.ToolButton.setObjectName("ToolButton")
        self.ToolButton.setIcon("./static/up.svg")
        self.ToolButton_2 = ToolButton(Form)
        self.ToolButton_2.setIcon("./static/down.svg")
        self.ToolButton_2.setGeometry(QtCore.QRect(230, 310, 38, 32))
        self.ToolButton_2.setObjectName("ToolButton_2")
        self.CaptionLabel = CaptionLabel(Form)
        self.CaptionLabel.setGeometry(QtCore.QRect(550, 300, 70, 16))
        self.CaptionLabel.setObjectName("CaptionLabel")
        self.CaptionLabel_2 = CaptionLabel(Form)
        self.CaptionLabel_2.setGeometry(QtCore.QRect(300, 300, 70, 16))
        self.CaptionLabel_2.setObjectName("CaptionLabel_2")
        self.CaptionLabel_3 = CaptionLabel(Form)
        self.CaptionLabel_3.setGeometry(QtCore.QRect(170, 300, 70, 16))
        self.CaptionLabel_3.setObjectName("CaptionLabel_3")
        self.CardWidget = CardWidget(Form)
        self.CardWidget.setGeometry(QtCore.QRect(120, 50, 591, 211))
        self.CardWidget.setObjectName("CardWidget")
        self.TimePicker = TimePicker(self.CardWidget)
        self.TimePicker.setGeometry(QtCore.QRect(340, 20, 240, 30))
        self.TimePicker.setObjectName("TimePicker")
        self.ZhDatePicker = ZhDatePicker(self.CardWidget)
        self.ZhDatePicker.setGeometry(QtCore.QRect(20, 20, 240, 30))
        self.ZhDatePicker.setObjectName("ZhDatePicker")
        self.SubtitleLabel = SubtitleLabel(self.CardWidget)
        self.SubtitleLabel.setGeometry(QtCore.QRect(80, 70, 119, 27))
        self.SubtitleLabel.setObjectName("SubtitleLabel")
        self.SubtitleLabel_2 = SubtitleLabel(self.CardWidget)
        self.SubtitleLabel_2.setGeometry(QtCore.QRect(80, 130, 119, 27))
        self.SubtitleLabel_2.setObjectName("SubtitleLabel_2")
        self.SubtitleLabel_3 = SubtitleLabel(self.CardWidget)
        self.SubtitleLabel_3.setGeometry(QtCore.QRect(360, 70, 119, 27))
        self.SubtitleLabel_3.setObjectName("SubtitleLabel_3")
        self.SubtitleLabel_4 = SubtitleLabel(self.CardWidget)
        self.SubtitleLabel_4.setGeometry(QtCore.QRect(360, 130, 119, 27))
        self.SubtitleLabel_4.setObjectName("SubtitleLabel_4")
        self.CaptionLabel_4 = CaptionLabel(Form)
        self.CaptionLabel_4.setGeometry(QtCore.QRect(710, 270, 111, 111))
        self.CaptionLabel_4.setStyleSheet("background:url(:/images/11.jpg)")
        self.CaptionLabel_4.setText("")
        self.CaptionLabel_4.setObjectName("CaptionLabel_4")
        self.CaptionLabel_5 = CaptionLabel(Form)
        self.CaptionLabel_5.setGeometry(QtCore.QRect(10, 270, 111, 111))
        self.CaptionLabel_5.setStyleSheet("background:url(:/images/22.jpg)")
        self.CaptionLabel_5.setText("")
        self.CaptionLabel_5.setObjectName("CaptionLabel_5")
        self.CaptionLabel_6 = CaptionLabel(Form)
        self.CaptionLabel_6.setGeometry(QtCore.QRect(300, 340, 141, 41))
        self.CaptionLabel_6.setStyleSheet('font: 15pt "华文彩云";')
        self.CaptionLabel_6.setObjectName("CaptionLabel_6")
        self.RadioButton = RadioButton(Form)
        self.RadioButton.setGeometry(QtCore.QRect(490, 350, 113, 24))
        self.RadioButton.setObjectName("RadioButton")
        self.TransparentDropDownToolButton = TransparentDropDownToolButton(Form)
        self.TransparentDropDownToolButton.setGeometry(QtCore.QRect(350, 290, 58, 30))
        self.TransparentDropDownToolButton.setObjectName(
            "TransparentDropDownToolButton"
        )
        self.TransparentDropDownToolButton.setIcon("./static/menu.svg")
        self.TransparentDropDownToolButton.setMenu(self.menu)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        currentDateTime = QtCore.QDateTime.currentDateTime()
        self.TimePicker.setTime(currentDateTime.time())
        self.ZhDatePicker.setDate(currentDateTime.date())
        self.timer = QtCore.QTimer(Form)
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(10000)  # 每10秒更新一次

        self.timer1 = QtCore.QTimer(Form)
        self.timer1.timeout.connect(self.updateTime1)
        self.timer1.start(2000)

        self.PushButton.clicked.connect(self.toggleMode)
        self.ToolButton.clicked.connect(self.increaseTemperature)
        self.ToolButton_2.clicked.connect(self.decreaseTemperature)
        self.SwitchButton.checkedChanged.connect(self.toggleSweep)
        self.action_up.triggered.connect(self.action_up_triggered)
        self.action_down.triggered.connect(self.action_down_triggered)
        self.RadioButton.clicked.connect(self.toggleState)

    def action_up_triggered(self):
        # 这里添加点击 'Up' 时的逻辑
        if self.speed == 3:
            self.speed = 3
        elif self.speed == 2:
            self.speed = 3
        else:
            self.speed = 2
        self.updateSpeedLabel()
        self.send_operation_request("wind_speed", str(self.speed))

    def action_down_triggered(self):
        # 这里添加点击 'Down' 时的逻辑
        if self.speed == 3:
            self.speed = 2
        elif self.speed == 2:
            self.speed = 1
        else:
            self.speed = 1
        self.updateSpeedLabel()
        self.send_operation_request("wind_speed", str(self.speed))

    def increaseTemperature(self):
        self.temperature += 1  # 增加温度
        self.updateTemperatureLabel()
        self.reset_temp_update_timer()

    def decreaseTemperature(self):
        self.temperature -= 1  # 减少温度
        self.updateTemperatureLabel()
        self.reset_temp_update_timer()

    def send_temperature_update(self):
        # 当计时器到达间隔时，发送更新请求
        # print("Sending temperature update:", self.temperature)
        self.send_operation_request("temperature", str(self.temperature))

    def reset_temp_update_timer(self):
        self.temp_update_timer.stop()
        self.temp_update_timer.start()

    def toggleMode(self):
        if self.current_mode == "cold":
            self.current_mode = "hot"
        else:
            self.current_mode = "cold"
        self.SubtitleLabel_3.setText(f"模式：{self.current_mode}")
        self.send_operation_request("mode", str(self.current_mode))

    def toggleSweep(self):
        if self.sweep == "on":
            self.sweep = "off"
        else:
            self.sweep = "on"
        self.SubtitleLabel_4.setText(f"扫风：{self.sweep}")
        if self.sweep == "on":
            self.send_operation_request("sweep", "True")
        else:
            self.send_operation_request("sweep", "False")

    def toggleState(self):
        global global_state
        if global_state == "stop":
            global_state = "start"
            self.send_operation_request("start", "sb")
        else:
            global_state = "stop"
            self.send_operation_request("stop", "sb")

    def send_operation_request(self, operation, data):
        unique_id = self.generate_unique_id()
        private_key = rsa.PrivateKey.load_pkcs1(open("private.pem", "rb").read())
        time_now = str(time.localtime())
        signature = self.generate_signature(
            private_key, operation + unique_id + data + time_now
        )
        global base_url
        url = base_url + "/" + self.room_id
        payload = {
            "operation": operation,
            "data": data,
            "time": time_now,
            "unique_id": unique_id,
            "signature": signature,
        }
        response = requests.post(url, json=payload)
        if response.status_code == 204:
            print("Operation Request successfully")
        else:
            print("Error:", response.status_code)

    def updateSpeedLabel(self):
        self.SubtitleLabel_2.setText(f"风速：{self.speed}")

    def updateTemperatureLabel(self):
        if self.temperature < 16:
            self.temperature = 16
        if self.temperature > 30:
            self.temperature = 30
        # 更新 SubtitleLabel 显示温度
        self.SubtitleLabel.setText(f"温度：{self.temperature}°C")

    def update_radio_button_state(self):
        if self.state == "start":
            self.RadioButton.setChecked(True)
        else:
            self.RadioButton.setChecked(False)

    def updateTime1(self):
        global global_state 
        global data
        # 更新全局变量
        global_state = (
            data["operation"]
            if data is not None and data["operation"] in ["start", "stop"]
            else global_state
        )
        # 接收服务端此时的state
        self.state = global_state
        self.update_radio_button_state()

    def updateTime(self):
        # 更新 TimePicker 的时间为当前时间
        currentDateTime = QtCore.QDateTime.currentDateTime()
        self.TimePicker.setTime(currentDateTime.time())
        
        # 回温函数
        if self.state == "start":
            if (
                self.current_mode == "cold"
                and self.current_temperature > self.temperature
            ):
                self.current_temperature -= 0.5
            elif (
                self.current_mode == "hot"
                and self.current_temperature < self.temperature
            ):
                self.current_temperature += 0.5
        else:
            # 当空调关闭时，回温至初始温度
            if self.current_temperature < self.initial_temperature:
                self.current_temperature = min(
                    self.current_temperature + 0.5, self.initial_temperature
                )
            elif self.current_temperature > self.initial_temperature:
                self.current_temperature = max(
                    self.current_temperature - 0.5, self.initial_temperature
                )

        # 更新温度显示
        self.CaptionLabel_6.setText(f"当前温度: {self.current_temperature}°")

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.PushButton.setText(_translate("Form", "模式切换"))
        self.CaptionLabel.setText(_translate("Form", "扫风"))
        self.CaptionLabel_2.setText(_translate("Form", "风速调节"))
        self.CaptionLabel_3.setText(_translate("Form", "温度调节"))
        self.SubtitleLabel.setText(_translate("Form", f"温度：{self.temperature}°C"))
        self.SubtitleLabel_2.setText(_translate("Form", f"风速：{self.speed}"))
        self.SubtitleLabel_3.setText(_translate("Form", f"模式：{self.current_mode}"))
        self.SubtitleLabel_4.setText(_translate("Form", f"扫风：{self.sweep}"))
        self.CaptionLabel_6.setText(
            _translate("Form", f"当前温度：{self.current_temperature}°C")
        )
        self.RadioButton.setText(_translate("Form", "开关"))


from qfluentwidgets import (
    CaptionLabel,
    CardWidget,
    PushButton,
    SubtitleLabel,
    SwitchButton,
    TimePicker,
    ToolButton,
    TransparentDropDownToolButton,
    ZhDatePicker,
    RadioButton,
)
import resource_rc
