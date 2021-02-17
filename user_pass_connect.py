#!/usr/bin/python3
# coding: utf-8
# user_pass_connect.py
"""
set database connection secret parameters, user name and password authentication
"""
# 345678901234567890123456789012345678901234567890123456789012345678901234567890
__author__ = "Dr Adel"
__location__ = "Roushdy"
__date__ = "Feb 12, 2018 06:58 PM"

import sys
from PyQt5 import QtWidgets as qtw
import os.path
import json
import psycopg2
import ui_user_password_dlg
import ui_set_conn_dlg
import set_conn_1

# -------------------
RES_FILE = 'pg_connection.bin'
SIGNATURE = 'pg_sgnature_ver1'


class UserPasswordDlg(qtw.QDialog):
    """ user name - password Dialog

    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pass_ui = ui_user_password_dlg.Ui_Dialog()
        self.pass_ui.setupUi(self)
        # ------Signals------------------
        self.pass_ui.btnConfirm.accepted.connect(self.on_btn_confirm_ok)
        self.pass_ui.btnConfirm.rejected.connect(self.reject)
        self.open_data_connection()

    def on_btn_confirm_ok(self):
        pass

    def open_data_connection(self):
        pass


class PgConnectionArgs(qtw.QDialog):
    """ maintain database connection arguments
    Used by Admin to reset parameters and save encrypted file
    Structure (encrypted in set_con_1.py): version 'pg_sgnature_ver1' file nmae: 'pg_connection.bin'
    {'sign': self.signature, 'ip': self.ip, 'user': self.user, 'passw': self.passw, 'db': self.db}

    """

    def __init__(self, parent=None, resource=RES_FILE, sig=SIGNATURE):
        super().__init__(parent)
        self.setcon = ui_set_conn_dlg.Ui_Dialog()
        self.setcon.setupUi(self)
        # --------------------------------
        self.resource_file = resource
        self.signature = sig
        self.ip = ''
        self.user = ''
        self.passw = ''
        self.db = ''
        # ------------
        self.data = {}
        # ------------
        self.pg = None
        self.curs = None
        self.is_connected = False
        # ------------
        self.setcon.btnClose.clicked.connect(self.reject)
        self.setcon.btnConnect.clicked.connect(self.on_btn_connect)
        self.setcon.btnPasswordShow.clicked.connect(self.on_btn_passw_show)
        # --------------------------
        self.setcon.lblConnectedIcon.hide()

        # --------Start-------------
        msg = self.read_resource_bin(resource)
        print(msg)
        if msg == 'ok':
            self.build_vars_from_dic()
            self.build_widgets_from_vars()

    def on_btn_connect(self):
        self.build_vars_from_widgets()
        if not (self.signature and self.ip and self.user and self.passw and self.db):
            print('some data is missing !!!')
            return
        if self.curs:
            self.pg.close_connection()
        # now proceed
        self.pg = PgConnect(self.ip, self.db, self.user, self.passw)
        self.curs = self.pg.connect_to_db()
        if self.curs:
            print('successfully connected')
            self.is_connected = True
            self.setcon.lblNotConnectedIcon.hide()
            self.setcon.lblConnectedIcon.show()
            self.save()
        else:
            self.is_connected = False
            self.pg = None
            self.setcon.lblNotConnectedIcon.show()
            self.setcon.lblConnectedIcon.hide()

    def on_btn_passw_show(self):
        if self.setcon.linePassword.echoMode() == 2:        # Password
            self.setcon.linePassword.setEchoMode(0)         # Normal
        else:
            self.setcon.linePassword.setEchoMode(2)         # Password

    def save(self):
        self.build_dic_from_vars()
        # -----------------
        # encrypt string representation of data using repr()
        enc = set_conn_1.enc(repr(self.data))
        with open(self.resource_file, 'wb') as fp:
            # json.dump(enc, fp)
            fp.write(enc)

    def reset_data(self):
        self.ip = ''
        self.user = ''
        self.passw = ''
        self.db = ''

    def build_dic_from_vars(self):
        self.data = {'sign': self.signature, 'ip': self.ip, 'user': self.user, 'passw': self.passw, 'db': self.db}

    def build_vars_from_dic(self):
        self.signature = self.data['sign']
        self.ip = self.data['ip']
        self.user = self.data['user']
        self.passw = self.data['passw']
        self.db = self.data['db']

    def build_vars_from_widgets(self):
        self.ip = self.setcon.lineHost.text()
        self.user = self.setcon.lineUserName.text()
        self.passw = self.setcon.linePassword.text()
        self.db = self.setcon.lineDatabase.text()

    def build_widgets_from_vars(self):
        self.setcon.lineHost.setText(self.ip)
        self.setcon.lineUserName.setText(self.user)
        self.setcon.linePassword.setText(self.passw)
        self.setcon.lineDatabase.setText(self.db)

    def read_resource_bin(self, res_fil):
        if os.path.isfile(res_fil):
            try:
                with open(res_fil, 'rb') as fp:
                    data_bytes = fp.read(-1)      # read all
                # decode and convert result back to dictionary using eval
                dec = eval(set_conn_1.dec(data_bytes))
            except OSError:
                return 'OS Error'
            except TypeError:
                return 'Type Error'
        else:
            return 'no file exists'
        if not dec:
            return 'file empty'
        elif 'sign' not in dec:
            return 'not our format'
        elif dec['sign'] != self.signature:
            return 'old file version'
        else:
            self.data = dec
            return 'ok'

    def read_resource_json(self, res_fil):
        if os.path.isfile(res_fil):
            try:
                with open(res_fil, 'r') as fp:
                    data = json.load(fp)
            except OSError:
                data = {}
        else:
            return 'no file'
        if not data:
            return 'file empty'
        try:
            dec = set_conn_1.decode_all(data)
        except:
            return 'error in decoding'
        if 'sign' not in dec:
            return 'not our format'
        elif dec['sign'] != self.signature:
            return 'old file version'
        else:
            self.data = dec
            return 'ok'


class PgConnect:

    def __init__(self, host, db, user, passw):
        self.host = host
        self.db = db
        self.user = user
        self.passw = passw
        # -----------------
        self.myconn = None
        self.curs = None
        # This is an attempt to allow development of code with multiple paramstyles
        self.pmark = "%s"
        self.pg_error = (psycopg2.Error, psycopg2.ProgrammingError)

    def connect_to_db(self):
        try:
            self.myconn = psycopg2.connect(host=self.host, database=self.db, user=self.user, password=self.passw)
        except self.pg_error:
            print('error in connection')
            return None
        self.curs = self.myconn.cursor()
        return self.curs

    def close_connection(self):
        if self.myconn:
            self.myconn.close()
            self.myconn = None
            self.curs = None


class PgReadConnectBuld:
    """
    read database connection arguments
    Used by other users to make a connection to database
    Must have user authentication here.
    This module must be in C code (using cython) to cover the internal security.

    """

    def __init__(self, resource=RES_FILE, sig=SIGNATURE):
        # --------------------------------
        self.resource_file = resource
        self.signature = sig
        self.ip = ''
        self.user = ''
        self.passw = ''
        self.db = ''
        # ------------
        self.data = {}
        # ------------
        self.pg = None
        self.mycon = None
        self.curs = None
        self.is_connected = False
        # --------Start-------------
        msg = self.read_resource_bin(resource)
        print(msg)
        if msg == 'ok':
            self.build_vars_from_dic()
            self.connect()

    def connect(self):
        if self.curs:
            self.pg.close_connection()
        # now proceed
        self.pg = PgConnect(self.ip, self.db, self.user, self.passw)
        self.curs = self.pg.connect_to_db()
        self.mycon = self.pg.myconn
        if self.curs:
            self.is_connected = True
        else:
            self.is_connected = False
            self.pg = None

    def reset_data(self):
        self.ip = ''
        self.user = ''
        self.passw = ''
        self.db = ''

    def build_vars_from_dic(self):
        self.signature = self.data['sign']
        self.ip = self.data['ip']
        self.user = self.data['user']
        self.passw = self.data['passw']
        self.db = self.data['db']

    def read_resource_bin(self, res_fil):
        if os.path.isfile(res_fil):
            try:
                with open(res_fil, 'rb') as fp:
                    data_bytes = fp.read(-1)      # read all
                # decode and convert result back to dictionary using eval
                dec = eval(set_conn_1.dec(data_bytes))
            except OSError:
                return 'OS Error'
            except TypeError:
                return 'Type Error'
        else:
            return 'no file exists'
        if not dec:
            return 'file empty'
        elif 'sign' not in dec:
            return 'not our format'
        elif dec['sign'] != self.signature:
            return 'old file version'
        else:
            self.data = dec
            return 'ok'

    def gettblsindatabase(self):
        """

        :return: list of table names
        """
        sql = "select table_name from information_schema.tables where table_schema = 'public' order by table_name"
        self.curs.execute(sql)
        res = self.curs.fetchall()
        print(res)
        if len(res) > 0:
            return [element[0] for element in res]
        else:
            return None

    def buildtable(self, sql, pgtblnme):
        err = 'ok'
        try:
            print("Creating table ", pgtblnme)
            self.curs.execute(sql)
        except psycopg2.Error as e:
            err = "DB Error: ", e.pgerror
            print(err)
            return err
        self.mycon.commit()  # We'll try to continue even in the presence of errors
        return err


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    # myfont = QFont("AlMateen")
    # myfont = QFont("Noto Naskh Arabic UI", 10, QFont.Bold)
    # myfont = QFont("Sans")
    # myfont = QFont("Times New Roman")
    # myfont = QFont("FreeSans")
    # myfont = QFont("Arab")
    # myfont = QFont("AlArabiya")
    # app.setFont(myfont)
    # form = UserPasswordDlg(parent=None)
    form = PgConnectionArgs(parent=None)
    form.show()
    app.exec_()
