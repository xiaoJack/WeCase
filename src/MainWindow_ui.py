# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/MainWindow.ui'
#
# Created: Sat Mar 30 19:26:45 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_frm_MainWindow(object):
    def setupUi(self, frm_MainWindow):
        frm_MainWindow.setObjectName(_fromUtf8("frm_MainWindow"))
        frm_MainWindow.resize(295, 637)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/IMG/img/WeCase.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frm_MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(frm_MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.homeView = QtDeclarative.QDeclarativeView(self.tab)
        self.homeView.setObjectName(_fromUtf8("homeView"))
        self.verticalLayout_2.addWidget(self.homeView)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.mentionsView = QtDeclarative.QDeclarativeView(self.tab_2)
        self.mentionsView.setObjectName(_fromUtf8("mentionsView"))
        self.verticalLayout_3.addWidget(self.mentionsView)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.commentsView = QtDeclarative.QDeclarativeView(self.tab_3)
        self.commentsView.setObjectName(_fromUtf8("commentsView"))
        self.verticalLayout_4.addWidget(self.commentsView)
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tab_4)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.myView = QtDeclarative.QDeclarativeView(self.tab_4)
        self.myView.setObjectName(_fromUtf8("myView"))
        self.verticalLayout_5.addWidget(self.myView)
        self.tabWidget.addTab(self.tab_4, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.widget = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(0, 30))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.pushButton_me = QtGui.QPushButton(self.widget)
        self.pushButton_me.setObjectName(_fromUtf8("pushButton_me"))
        self.gridLayout.addWidget(self.pushButton_me, 0, 3, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 4, 1, 1)
        self.pushButton_refresh = QtGui.QPushButton(self.widget)
        self.pushButton_refresh.setObjectName(_fromUtf8("pushButton_refresh"))
        self.gridLayout.addWidget(self.pushButton_refresh, 0, 1, 1, 1)
        self.pushButton_new = QtGui.QPushButton(self.widget)
        self.pushButton_new.setObjectName(_fromUtf8("pushButton_new"))
        self.gridLayout.addWidget(self.pushButton_new, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.widget)
        frm_MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(frm_MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 295, 22))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menubar.sizePolicy().hasHeightForWidth())
        self.menubar.setSizePolicy(sizePolicy)
        self.menubar.setMinimumSize(QtCore.QSize(0, 0))
        self.menubar.setDefaultUp(True)
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_WeCase = QtGui.QMenu(self.menubar)
        self.menu_WeCase.setObjectName(_fromUtf8("menu_WeCase"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuO_ptions = QtGui.QMenu(self.menubar)
        self.menuO_ptions.setObjectName(_fromUtf8("menuO_ptions"))
        frm_MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(frm_MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        frm_MainWindow.setStatusBar(self.statusbar)
        self.action_About = QtGui.QAction(frm_MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/IMG/img/where_s_my_weibo.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_About.setIcon(icon1)
        self.action_About.setObjectName(_fromUtf8("action_About"))
        self.action_Refresh = QtGui.QAction(frm_MainWindow)
        self.action_Refresh.setObjectName(_fromUtf8("action_Refresh"))
        self.action_Log_out = QtGui.QAction(frm_MainWindow)
        self.action_Log_out.setObjectName(_fromUtf8("action_Log_out"))
        self.action_Exit = QtGui.QAction(frm_MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/IMG/img/application-exit.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Exit.setIcon(icon2)
        self.action_Exit.setObjectName(_fromUtf8("action_Exit"))
        self.action_Settings = QtGui.QAction(frm_MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/IMG/img/preferences-other.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Settings.setIcon(icon3)
        self.action_Settings.setObjectName(_fromUtf8("action_Settings"))
        self.actionUpdate = QtGui.QAction(frm_MainWindow)
        self.actionUpdate.setObjectName(_fromUtf8("actionUpdate"))
        self.menu_WeCase.addAction(self.action_Refresh)
        self.menu_WeCase.addSeparator()
        self.menu_WeCase.addAction(self.action_Log_out)
        self.menu_WeCase.addAction(self.action_Exit)
        self.menuHelp.addAction(self.action_About)
        self.menuO_ptions.addAction(self.action_Settings)
        self.menuO_ptions.addAction(self.actionUpdate)
        self.menubar.addAction(self.menu_WeCase.menuAction())
        self.menubar.addAction(self.menuO_ptions.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(frm_MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.action_Exit, QtCore.SIGNAL(_fromUtf8("triggered()")), frm_MainWindow.close)
        QtCore.QObject.connect(self.action_About, QtCore.SIGNAL(_fromUtf8("triggered()")), frm_MainWindow.showAbout)
        QtCore.QObject.connect(self.action_Settings, QtCore.SIGNAL(_fromUtf8("triggered()")), frm_MainWindow.showSettings)
        QtCore.QObject.connect(self.action_Log_out, QtCore.SIGNAL(_fromUtf8("triggered()")), frm_MainWindow.logout)
        QtCore.QObject.connect(self.action_Refresh, QtCore.SIGNAL(_fromUtf8("triggered()")), frm_MainWindow.refresh)
        QtCore.QObject.connect(self.pushButton_refresh, QtCore.SIGNAL(_fromUtf8("clicked()")), frm_MainWindow.refresh)
        QtCore.QObject.connect(self.pushButton_new, QtCore.SIGNAL(_fromUtf8("clicked()")), frm_MainWindow.postTweet)
        QtCore.QObject.connect(frm_MainWindow, QtCore.SIGNAL(_fromUtf8("timelineLoaded(int)")), frm_MainWindow.moveToTop)
        QtCore.QObject.connect(frm_MainWindow, QtCore.SIGNAL(_fromUtf8("imageLoaded(QString)")), frm_MainWindow.setLoaded)
        QtCore.QObject.connect(frm_MainWindow, QtCore.SIGNAL(_fromUtf8("tabTextChanged(int,QString)")), frm_MainWindow.setTabText)
        QtCore.QMetaObject.connectSlotsByName(frm_MainWindow)

    def retranslateUi(self, frm_MainWindow):
        frm_MainWindow.setWindowTitle(_translate("frm_MainWindow", "WeCase", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("frm_MainWindow", "Weibo", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("frm_MainWindow", "@ME", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("frm_MainWindow", "Comments", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("frm_MainWindow", "My tweet", None))
        self.pushButton_me.setText(_translate("frm_MainWindow", "Me", None))
        self.pushButton_refresh.setText(_translate("frm_MainWindow", "Refresh", None))
        self.pushButton_new.setText(_translate("frm_MainWindow", "New Weibo", None))
        self.menu_WeCase.setTitle(_translate("frm_MainWindow", "&WeCase", None))
        self.menuHelp.setTitle(_translate("frm_MainWindow", "&Help", None))
        self.menuO_ptions.setTitle(_translate("frm_MainWindow", "&Options", None))
        self.action_About.setText(_translate("frm_MainWindow", "&About...", None))
        self.action_Refresh.setText(_translate("frm_MainWindow", "&Refresh", None))
        self.action_Log_out.setText(_translate("frm_MainWindow", "&Log out", None))
        self.action_Exit.setText(_translate("frm_MainWindow", "&Exit", None))
        self.action_Settings.setText(_translate("frm_MainWindow", "&Settings", None))
        self.actionUpdate.setText(_translate("frm_MainWindow", "&Update", None))

from PyQt4 import QtDeclarative
import wecase_rc
