# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayout = QtWidgets.QFormLayout(self.centralwidget)
        self.formLayout.setObjectName("formLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget.setObjectName("tabWidget")
        self.tabMain = QtWidgets.QWidget()
        self.tabMain.setObjectName("tabMain")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("imgs/overview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tabMain, icon, "")
        self.tabDevices = QtWidgets.QWidget()
        self.tabDevices.setObjectName("tabDevices")
        self.deviceScroll = QtWidgets.QScrollArea(self.tabDevices)
        self.deviceScroll.setGeometry(QtCore.QRect(0, 0, 751, 531))
        self.deviceScroll.setWidgetResizable(True)
        self.deviceScroll.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.deviceScroll.setObjectName("deviceScroll")
        self.scrollAreaWidgeDevice = QtWidgets.QWidget()
        self.scrollAreaWidgeDevice.setGeometry(QtCore.QRect(0, 0, 747, 527))
        self.scrollAreaWidgeDevice.setObjectName("scrollAreaWidgeDevice")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgeDevice)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.deviceHolderLayout = QtWidgets.QVBoxLayout()
        self.deviceHolderLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.deviceHolderLayout.setObjectName("deviceHolderLayout")
        self.verticalLayout_2.addLayout(self.deviceHolderLayout)
        self.deviceScroll.setWidget(self.scrollAreaWidgeDevice)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("imgs/device.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tabDevices, icon1, "")
        self.tabMachines = QtWidgets.QWidget()
        self.tabMachines.setObjectName("tabMachines")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tabMachines)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.machineHolder = QtWidgets.QVBoxLayout()
        self.machineHolder.setObjectName("machineHolder")
        self.machineControls = QtWidgets.QHBoxLayout()
        self.machineControls.setObjectName("machineControls")
        self.machineHolder.addLayout(self.machineControls)
        self.machineScroll = QtWidgets.QScrollArea(self.tabMachines)
        self.machineScroll.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.machineScroll.setWidgetResizable(True)
        self.machineScroll.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.machineScroll.setObjectName("machineScroll")
        self.scrollAreaWidgetMachine = QtWidgets.QWidget()
        self.scrollAreaWidgetMachine.setGeometry(QtCore.QRect(0, 0, 735, 501))
        self.scrollAreaWidgetMachine.setObjectName("scrollAreaWidgetMachine")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.scrollAreaWidgetMachine)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout.setContentsMargins(-1, 2, -1, 2)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.machineHolderLayout = QtWidgets.QVBoxLayout()
        self.machineHolderLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.machineHolderLayout.setObjectName("machineHolderLayout")
        self.horizontalLayout.addLayout(self.machineHolderLayout)
        self.machineScroll.setWidget(self.scrollAreaWidgetMachine)
        self.machineHolder.addWidget(self.machineScroll)
        self.verticalLayout_3.addLayout(self.machineHolder)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("imgs/state-machine.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tabMachines, icon2, "")
        self.tabLinks = QtWidgets.QWidget()
        self.tabLinks.setObjectName("tabLinks")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.tabLinks)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 731, 511))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.linkHolder = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.linkHolder.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.linkHolder.setContentsMargins(0, 0, 0, 0)
        self.linkHolder.setObjectName("linkHolder")
        self.linkControls = QtWidgets.QHBoxLayout()
        self.linkControls.setObjectName("linkControls")
        self.linkHolder.addLayout(self.linkControls)
        self.linkScroll = QtWidgets.QScrollArea(self.verticalLayoutWidget_2)
        self.linkScroll.setWidgetResizable(True)
        self.linkScroll.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.linkScroll.setObjectName("linkScroll")
        self.scrollAreaWidgetLinks = QtWidgets.QWidget()
        self.scrollAreaWidgetLinks.setGeometry(QtCore.QRect(0, 0, 725, 497))
        self.scrollAreaWidgetLinks.setObjectName("scrollAreaWidgetLinks")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetLinks)
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.linkHolderLayout = QtWidgets.QVBoxLayout()
        self.linkHolderLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.linkHolderLayout.setObjectName("linkHolderLayout")
        self.horizontalLayout_2.addLayout(self.linkHolderLayout)
        self.linkScroll.setWidget(self.scrollAreaWidgetLinks)
        self.linkHolder.addWidget(self.linkScroll)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("imgs/link.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tabLinks, icon3, "")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 30))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Lambent 4"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMain), _translate("MainWindow", "Overview"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDevices), _translate("MainWindow", "Devices"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMachines), _translate("MainWindow", "Machines"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabLinks), _translate("MainWindow", "Links"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
