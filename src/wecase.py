#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- Linux Sina Weibo Client
# Since 4th,Feb,2013
# This is a TEST version
# Wait for ...
# Copyright: GPL v3 or later.

# Well, Let's go!


import sys
import urllib
import httplib
from weibo import APIClient
from PyQt4 import QtCore, QtGui
from LoginWindow_ui import Ui_frm_Login
from MainWindow_ui import Ui_frm_MainWindow
from SettingWindow_ui import Ui_SettingWindow
# NewpostWindow still uses Ui_MainWindow as its name.
# someone should fix it
from NewpostWindow_ui import Ui_MainWindow

APP_KEY = "1011524190"
APP_SECRET = "1898b3f668368b9f4a6f7ac8ed4a918f"
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
OAUTH2_PARAMETER = {'client_id':       APP_KEY,
                    'response_type':   'code',
                    'redirect_uri':    CALLBACK_URL,
                    'action':          'submit',
                    'userId':          '',  # username
                    'passwd':          '',  # password
                    'isLoginSina':     0,
                    'from':            '',
                    'regCallback':     '',
                    'state':           '',
                    'ticket':          '',
                    'withOfficalFlag': 0}


class LoginWindow(QtGui.QWidget, Ui_frm_Login):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setupMyUi()
        self.setupSignals()

    def setupSignals(self):
        self.pushButton_log.clicked.connect(self.login)

    def setupMyUi(self):
        self.txt_Password.setEchoMode(QtGui.QLineEdit.Password)

    def login(self):
        username = self.cmb_Users.currentText()
        password = self.txt_Password.text()

        client = self.authorize(username, password)

        if client:
            wecase_main.client = client
            wecase_main.status()
            wecase_main.show()
            self.close()
        else:
            QtGui.QMessageBox.critical(None, "Authorize Failed!",
                                       "Check your account and password!")

    def authorize(self, username, password):
        # TODO: This method is very messy, maybe do some cleanup?

        client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET,
                           redirect_uri=CALLBACK_URL)

        # Step 1: Get the authorize url from Sina
        authorize_url = client.get_authorize_url()

        # Step 2: Send the authorize info to Sina and get the authorize_code
        # TODO: Rewrite them with urllib/urllib2
        oauth2 = OAUTH2_PARAMETER
        oauth2['userId'] = username
        oauth2['passwd'] = password
        postdata = urllib.urlencode(oauth2)

        conn = httplib.HTTPSConnection('api.weibo.com')
        conn.request('POST', '/oauth2/authorize', postdata,
                     {'Referer':       authorize_url,
                      'Content-Type': 'application/x-www-form-urlencoded'})

        res = conn.getresponse()

        location = res.getheader('location')

        if not location:
            return None

        authorize_code = location.split('=')[1]
        conn.close()

        # Step 3: Put the authorize information into SDK
        r = client.request_access_token(authorize_code)
        access_token = r.access_token
        expires_in = r.expires_in

        client.set_access_token(access_token, expires_in)

        return client


class WeCaseWindow(QtGui.QMainWindow, Ui_frm_MainWindow):
    client = None

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setupMyUi()
        self.setupSignals()
        self.setupModels()

    def setupMyUi(self):
        self.listView.setWordWrap(True)

    def setupSignals(self):
        self.action_Exit.triggered.connect(self.close)
        self.action_Settings.triggered.connect(self.settings_show)
        self.action_Log_out.triggered.connect(self.logout)
        self.action_Refresh.triggered.connect(self.status)

        self.pushButton_settings.clicked.connect(self.settings_show)
        self.pushButton_refresh.clicked.connect(self.status)
        self.pushButton_new.clicked.connect(self.new_tweet)

    def setupModels(self):
        # Test only
        self.timeline = QtGui.QStringListModel(self)
        self.listView.setModel(self.timeline)

    def status(self):
        # Test only
        self.timeline_string = []

        statuses = self.client.statuses.user_timeline.get().statuses
        for status in statuses:
            self.timeline_string.append("%s\nText: %s\n" %
                                        (status['created_at'],
                                         status['text']))

        self.timeline_StringList = QtCore.QStringList(self.timeline_string)
        self.timeline.setStringList(self.timeline_StringList)

    def settings_show(self):
        wecase_settings.show()

    def logout(self):
        wecase_login.show()
        self.close()

    def new_tweet(self):
        wecase_new.show()


class WeSettingsWindow(QtGui.QMainWindow, Ui_SettingWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)


class NewpostWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    wecase_login = LoginWindow()
    wecase_main = WeCaseWindow()
    wecase_settings = WeSettingsWindow()
    wecase_new = NewpostWindow()

    wecase_login.show()
    sys.exit(app.exec_())
