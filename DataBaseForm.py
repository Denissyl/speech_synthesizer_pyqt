# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_DataBaseForm.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!
import sqlite3
import sys

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DataBaseForm(object):
    def setupUi(self, DataBaseForm):
        DataBaseForm.setObjectName("DataBaseForm")
        DataBaseForm.resize(282, 673)
        self.verticalLayout = QtWidgets.QVBoxLayout(DataBaseForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(DataBaseForm)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.le_condition = QtWidgets.QLineEdit(DataBaseForm)
        self.le_condition.setObjectName("le_condition")
        self.verticalLayout.addWidget(self.le_condition)
        self.pb_select = QtWidgets.QPushButton(DataBaseForm)
        self.pb_select.setObjectName("pb_select")
        self.verticalLayout.addWidget(self.pb_select)
        self.pb_select_all = QtWidgets.QPushButton(DataBaseForm)
        self.pb_select_all.setObjectName("pb_select_all")
        self.verticalLayout.addWidget(self.pb_select_all)
        self.pb_delete = QtWidgets.QPushButton(DataBaseForm)
        self.pb_delete.setObjectName("pb_delete")
        self.verticalLayout.addWidget(self.pb_delete)
        self.tw_sounds = QtWidgets.QTableWidget(DataBaseForm)
        self.tw_sounds.setObjectName("tw_sounds")
        self.tw_sounds.setColumnCount(0)
        self.tw_sounds.setRowCount(0)
        self.verticalLayout.addWidget(self.tw_sounds)

        self.retranslateUi(DataBaseForm)
        QtCore.QMetaObject.connectSlotsByName(DataBaseForm)

    def retranslateUi(self, DataBaseForm):
        _translate = QtCore.QCoreApplication.translate
        DataBaseForm.setWindowTitle(_translate("DataBaseForm", "База данных"))
        self.label.setText(_translate("DataBaseForm", "Введите букву или слог"))
        self.pb_select.setText(_translate("DataBaseForm", "Вывести"))
        self.pb_select_all.setText(_translate("DataBaseForm", "Вывести всё"))
        self.pb_delete.setText(_translate("DataBaseForm", "Удалить"))
