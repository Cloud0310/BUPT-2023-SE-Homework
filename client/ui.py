# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets
from qfluentwidgets import FluentIcon, RoundMenu


class ui_Form(object):
    def __init__(self):
        super().__init__()

        self.menu = RoundMenu(parent=self)
        self.action_up = QtWidgets.QAction(FluentIcon.UP.icon(), "Up")
        self.action_down = QtWidgets.QAction(FluentIcon.DOWN.icon(), "Down")

        self.menu.addAction(self.action_up)
        self.menu.addAction(self.action_down)

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
        self.PushButton.clicked.connect(self.toggleMode)
        self.ToolButton.clicked.connect(self.increaseTemperature)
        self.ToolButton_2.clicked.connect(self.decreaseTemperature)
        self.SwitchButton.checkedChanged.connect(self.toggleSweep)
        self.action_up.triggered.connect(self.action_up_triggered)
        self.action_down.triggered.connect(self.action_down_triggered)

    def action_up_triggered(self):
        # 这里添加点击 'Up' 时的逻辑
        if self.speed == "强风":
            self.speed = "强风"
        elif self.speed == "中风":
            self.speed = "强风"
        else:
            self.speed = "中风"
        self.updateSpeedLabel()

    def action_down_triggered(self):
        # 这里添加点击 'Down' 时的逻辑
        if self.speed == "强风":
            self.speed = "中风"
        elif self.speed == "中风":
            self.speed = "弱风"
        else:
            self.speed = "弱风"
        self.updateSpeedLabel()

    def increaseTemperature(self):
        self.temperature += 1  # 增加温度
        self.updateTemperatureLabel()

    def decreaseTemperature(self):
        self.temperature -= 1  # 减少温度
        self.updateTemperatureLabel()

    def updateSpeedLabel(self):
        self.SubtitleLabel_2.setText(f"风速：{self.speed}")

    def updateTemperatureLabel(self):
        if self.temperature < 16:
            self.temperature = 16
        if self.temperature > 30:
            self.temperature = 30
        # 更新 SubtitleLabel 显示温度
        self.SubtitleLabel.setText(f"温度：{self.temperature}°C")

    def updateTime(self):
        # 更新 TimePicker 的时间为当前时间
        currentDateTime = QtCore.QDateTime.currentDateTime()
        self.TimePicker.setTime(currentDateTime.time())

    def toggleMode(self):
        if self.current_mode == "cold":
            self.current_mode = "hot"
        else:
            self.current_mode = "cold"
        self.SubtitleLabel_3.setText(f"模式：{self.current_mode}")

    def toggleSweep(self):
        if self.sweep == "on":
            self.sweep = "off"
        else:
            self.sweep = "on"
        self.SubtitleLabel_4.setText(f"扫风：{self.sweep}")

    def retranslateUi(self, Form):
        self.temperature = 25
        self.speed = "中风"
        self.current_mode = "cold"
        self.sweep = "on"
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
)
import resource_rc