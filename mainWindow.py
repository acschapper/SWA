# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindowWithGrid.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.actionPan = QAction("Pan", MainWindow)
        self.actionPan.setShortcut("Ctrl+1")
        self.actionPan.setCheckable(True)

        self.actionQuit = QAction("Quit", MainWindow)
        self.actionQuit.setShortcut(QKeySequence.Quit)

        self.actionZoomIn = QAction("Zoom In", MainWindow)
        self.actionZoomIn.setShortcut(QKeySequence.ZoomIn)

        self.actionZoomOut = QAction("Zoom Out", MainWindow)
        self.actionZoomOut.setShortcut(QKeySequence.ZoomOut)

        self.actionEdit = QAction("Edit Mode", MainWindow)
        self.actionEdit.setShortcut("Ctrl+2")
        self.actionEdit.setCheckable(True)

        self.actionAddFlowPath = QAction("Add FlowPath", MainWindow)
        self.actionAddFlowPath.setShortcut("Ctrl+A")
        self.actionAddFlowPath.setCheckable(True)

        self.actionEditFlowPath = QAction("Edit FlowPath", MainWindow)
        self.actionEditFlowPath.setShortcut("Ctrl+E")
        self.actionEditFlowPath.setCheckable(True)

        self.actionDeleteFlowPath = QAction("Delete FlowPath", MainWindow)
        self.actionDeleteFlowPath.setShortcut("Ctrl+D")
        self.actionDeleteFlowPath.setCheckable(True)

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(986, 620)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.QgsMapCanvas = QgsMapCanvas(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.QgsMapCanvas.sizePolicy().hasHeightForWidth())
        self.QgsMapCanvas.setSizePolicy(sizePolicy)
        self.QgsMapCanvas.setObjectName("QgsMapCanvas")
        self.gridLayout_2.addWidget(self.QgsMapCanvas, 0, 2, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.Export = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Export.sizePolicy().hasHeightForWidth())
        self.Export.setSizePolicy(sizePolicy)
        self.Export.setMinimumSize(QtCore.QSize(140, 0))
        self.Export.setObjectName("Export")
        self.horizontalLayout.addWidget(self.Export)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout_2.addLayout(self.horizontalLayout, 3, 2, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setText("Zoom In")
        self.toolButton.setDefaultAction(self.actionZoomIn)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout_2.addWidget(self.toolButton)

        self.toolButton_4 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_4.setText("Zoom Out")
        self.toolButton_4.setDefaultAction(self.actionZoomOut)
        self.toolButton_4.setObjectName("toolButton_4")
        self.horizontalLayout_2.addWidget(self.toolButton_4)

        self.toolButton_3 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_3.setText("Pan")
        self.toolButton_3.setDefaultAction(self.actionPan)
        self.toolButton_3.setObjectName("toolButton_3")
        self.horizontalLayout_2.addWidget(self.toolButton_3)

        self.toolButton_2 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_2.setText("Edit")
        self.toolButton_2.setDefaultAction(self.actionEdit)
        self.toolButton_2.setObjectName("toolButton_2")
        self.horizontalLayout_2.addWidget(self.toolButton_2)

        self.toolButton_5 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_5.setText("Add FlowPath")
        self.toolButton_5.setDefaultAction(self.actionAddFlowPath)
        self.toolButton_5.setObjectName("toolButton_5")
        self.horizontalLayout_2.addWidget(self.toolButton_5)

        self.toolButton_6 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_6.setText("Edit FlowPath")
        self.toolButton_6.setDefaultAction(self.actionEditFlowPath)
        self.toolButton_6.setObjectName("toolButton_6")
        self.horizontalLayout_2.addWidget(self.toolButton_6)

        self.toolButton_7 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_7.setText("Delete FlowPath")
        self.toolButton_7.setDefaultAction(self.actionDeleteFlowPath)
        self.toolButton_7.setObjectName("toolButton_7")
        self.horizontalLayout_2.addWidget(self.toolButton_7)

        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 2, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem4 = QtWidgets.QSpacerItem(20, 200, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.verticalLayout_2.addItem(spacerItem4)
        spacerItem5 = QtWidgets.QSpacerItem(20, 150, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout_2.addItem(spacerItem5)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_2)
        self.gridLayout_3.addLayout(self.verticalLayout_4, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 986, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad_File = QtWidgets.QAction(MainWindow)
        self.actionLoad_File.setObjectName("actionLoad_File")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionPrint = QtWidgets.QAction(MainWindow)
        self.actionPrint.setObjectName("actionPrint")
        self.actionAddLayer = QtWidgets.QAction(MainWindow)
        self.actionAddLayer.setObjectName("actionAddLayer")
        self.menuFile.addAction(self.actionAddLayer)
        self.menuFile.addAction(self.actionLoad_File)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addAction(self.actionPrint)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Export.setText(_translate("MainWindow", "Export"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionLoad_File.setText(_translate("MainWindow", "Load New File"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_as.setText(_translate("MainWindow", "Save as"))
        self.actionPrint.setText(_translate("MainWindow", "Print"))
        self.actionAddLayer.setText(_translate("MainWindow", "Add Layer"))

from qgis.gui import QgsMapCanvas