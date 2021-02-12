# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'user_password_dlg.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(235, 170)
        Dialog.setMinimumSize(QtCore.QSize(235, 170))
        Dialog.setMaximumSize(QtCore.QSize(235, 170))
        self.lblLoginName = QtWidgets.QLabel(Dialog)
        self.lblLoginName.setGeometry(QtCore.QRect(16, 32, 81, 20))
        self.lblLoginName.setObjectName("lblLoginName")
        self.lblPassword = QtWidgets.QLabel(Dialog)
        self.lblPassword.setGeometry(QtCore.QRect(30, 73, 62, 19))
        self.lblPassword.setObjectName("lblPassword")
        self.edtLoginName = QtWidgets.QLineEdit(Dialog)
        self.edtLoginName.setGeometry(QtCore.QRect(100, 30, 113, 29))
        self.edtLoginName.setObjectName("edtLoginName")
        self.edtPassword = QtWidgets.QLineEdit(Dialog)
        self.edtPassword.setGeometry(QtCore.QRect(100, 70, 113, 29))
        self.edtPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.edtPassword.setObjectName("edtPassword")
        self.btnConfirm = QtWidgets.QDialogButtonBox(Dialog)
        self.btnConfirm.setEnabled(True)
        self.btnConfirm.setGeometry(QtCore.QRect(30, 120, 176, 29))
        self.btnConfirm.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.btnConfirm.setObjectName("btnConfirm")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Enter Name and Password"))
        self.lblLoginName.setText(_translate("Dialog", "Login Name"))
        self.lblPassword.setText(_translate("Dialog", "Password"))

