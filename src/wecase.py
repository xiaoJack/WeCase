#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- Linux Sina Weibo Client
# Since 4th,Feb,2013
# This is a TEST version
# Wait for ...
# Copyright: GPL v3 or later.

# Well, Let's go!


import sys
import os
from datetime import datetime
from dateutil import parser as time_parser
import urllib.request
import urllib.parse
import urllib.error
import http.client
import shelve
import notify2 as pynotify
import threading
from WTimer import WTimer
from weibo import APIClient, APIError
from PyQt4 import QtCore, QtGui, QtDeclarative
from LoginWindow_ui import Ui_frm_Login
from MainWindow_ui import Ui_frm_MainWindow
from SettingWindow_ui import Ui_SettingWindow
from NewpostWindow_ui import Ui_NewPostWindow
from AboutWindow_ui import Ui_About_Dialog

APP_KEY = "1011524190"
APP_SECRET = "1898b3f668368b9f4a6f7ac8ed4a918f"
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
OAUTH2_PARAMETER = {'client_id': APP_KEY,
                    'response_type': 'code',
                    'redirect_uri': CALLBACK_URL,
                    'action': 'submit',
                    'userId': '',  # username
                    'passwd': '',  # password
                    'isLoginSina': 0,
                    'from': '',
                    'regCallback': '',
                    'state': '',
                    'ticket': '',
                    'withOfficalFlag': 0}
config_path = os.environ['HOME'] + '/.config/wecase/config_db'
cache_path = os.environ['HOME'] + '/.cache/wecase/'
myself_name = sys.argv[0].split('/')[-1]
myself_path = os.path.abspath(sys.argv[0]).replace(myself_name, "")


class TweetModel(QtCore.QAbstractListModel):
    def __init__(self, prototype, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.setRoleNames(prototype.roleNames())
        self.tweets = []

    def appendRow(self, item):
        self.insertRow(self.rowCount(), item)

    def clear(self):
        del self.tweets
        self.tweets = []

    def data(self, index, role):
        return self.tweets[index.row()].data(role)

    def insertRow(self, row, item):
        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        self.tweets.insert(row, item)
        self.endInsertRows()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.tweets)


class TweetItem(QtCore.QAbstractItemModel):
    typeRole = QtCore.Qt.UserRole + 1
    idRole = QtCore.Qt.UserRole + 2
    authorRole = QtCore.Qt.UserRole + 3
    avatarRole = QtCore.Qt.UserRole + 4
    contentRole = QtCore.Qt.UserRole + 5
    timeRole = QtCore.Qt.UserRole + 6
    originalIdRole = QtCore.Qt.UserRole + 7
    originalContentRole = QtCore.Qt.UserRole + 8
    originalAuthorRole = QtCore.Qt.UserRole + 9
    originalTimeRole = QtCore.Qt.UserRole + 10
    thumbnailPicRole = QtCore.Qt.UserRole + 11

    def __init__(self, type="", id="", author="", avatar="", content="",
                 time="", original_id="", original_content="",
                 original_author="", original_time="", thumbnail_pic="",
                 parent=None):
        QtCore.QAbstractItemModel.__init__(self, parent)

        self.type = type
        self.id = id
        self.author = author
        self.avatar = avatar
        self.content = content
        self.time = time
        self.original_id = original_id
        self.original_content = original_content
        self.original_author = original_author
        self.original_time = original_time
        self.thumbnail_pic = thumbnail_pic

    def sinceTimeString(self, createTime):
        create = time_parser.parse(createTime)
        create_utc = (create - create.utcoffset()).replace(tzinfo=None)
        now_utc = datetime.utcnow()

        # Always compare UTC time, do NOT compare LOCAL time.
        # See http://coolshell.cn/articles/5075.html for more details.
        passedSeconds = (now_utc - create_utc).seconds

        # datetime do not support nagetive numbers
        if now_utc < create_utc:
            return "Time travel!"
        if passedSeconds < 60:
            return "%.0f seconds ago" % (passedSeconds)
        if passedSeconds < 3600:
            return "%.0f minutes ago" % (passedSeconds / 60)
        if passedSeconds < 86400:
            return "%.0f hours ago" % (passedSeconds / 3600)

        return "%.0f days ago" % (passedSeconds / 86400)

    def roleNames(self):
        names = {}
        names[self.typeRole] = "type"
        names[self.idRole] = "id"
        names[self.authorRole] = "author"
        names[self.avatarRole] = "avatar"
        names[self.contentRole] = "content"
        names[self.timeRole] = "time"
        names[self.originalIdRole] = "original_id"
        names[self.originalContentRole] = "original_content"
        names[self.originalAuthorRole] = "original_author"
        names[self.originalTimeRole] = "original_time"
        names[self.thumbnailPicRole] = "thumbnail_pic"
        return names

    def data(self, role):
        if role == self.typeRole:
            return self.type
        elif role == self.idRole:
            return self.id
        elif role == self.authorRole:
            return self.author
        elif role == self.avatarRole:
            return self.avatar
        elif role == self.contentRole:
            return self.content
        elif role == self.timeRole:
            return self.sinceTimeString(self.time)
        elif role == self.originalIdRole:
            return self.original_id
        elif role == self.originalContentRole:
            return self.original_content
        elif role == self.originalAuthorRole:
            return self.original_author
        elif role == self.originalTimeRole:
            return self.original_time
        elif role == self.thumbnailPicRole:
            return self.thumbnail_pic
        else:
            return None


class LoginWindow(QtGui.QDialog, Ui_frm_Login):
    passwd = {}
    last_login = ""
    auto_login = False

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.loadConfig()
        self.setupUi(self)
        self.setupMyUi()

    def setupMyUi(self):
        self.show()
        self.txt_Password.setEchoMode(QtGui.QLineEdit.Password)
        self.cmb_Users.addItem(self.last_login)
        self.chk_AutoLogin.setChecked(self.auto_login)

        for username in list(self.passwd.keys()):
            if username == self.last_login:
                continue
            self.cmb_Users.addItem(username)

        if self.cmb_Users.currentText():
            self.setPassword(self.cmb_Users.currentText())

        if self.auto_login:
            self.login()

    def loadConfig(self):
        self.config = shelve.open(config_path, 'c')
        try:
            self.passwd = self.config['passwd']
            self.last_login = self.config['last_login']
            self.auto_login = self.config['auto_login']
        except KeyError:
            pass

    def saveConfig(self):
        self.config['passwd'] = self.passwd
        self.config['last_login'] = self.last_login
        self.config['auto_login'] = self.chk_AutoLogin.isChecked()

    def login(self):
        self.pushButton_log.setText("Login, waiting...")
        self.pushButton_log.setEnabled(False)
        app.processEvents()
        app.processEvents()

        client = self.ui_authorize()
        if client:
            if self.chk_Remember.isChecked():
                self.passwd[str(self.username)] = str(self.password)
                self.last_login = str(self.username)
                self.saveConfig()
            wecase_main.client = client
            wecase_main.get_uid()
            wecase_main.get_all_timeline()
            wecase_main.get_my_timeline()
            wecase_main.get_mentions_timeline()
            wecase_main.get_comment_to_me()
            wecase_main.show()
            self.close()
        else:
            QtGui.QMessageBox.critical(None, "Authorize Failed!",
                                       "Check your account and password!")
        self.pushButton_log.setText("GO!")
        self.pushButton_log.setEnabled(True)

    def ui_authorize(self):
        self.username = self.cmb_Users.currentText()
        self.password = self.txt_Password.text()
        client = self.authorize(self.username, self.password)

        if client:
            return client

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
        postdata = urllib.parse.urlencode(oauth2)

        conn = http.client.HTTPSConnection('api.weibo.com')
        conn.request('POST', '/oauth2/authorize', postdata,
                     {'Referer': authorize_url,
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

    def setPassword(self, username):
        self.txt_Password.setText(self.passwd[str(username)])

    def closeEvent(self, event):
        self.config.close()


class WeCaseWindow(QtGui.QMainWindow, Ui_frm_MainWindow):
    client = None
    uid = None
    timelineLoaded = QtCore.pyqtSignal(int)
    imageLoaded = QtCore.pyqtSignal(str)
    tabTextChanged = QtCore.pyqtSignal(int, str)

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.tweetViews = [self.homeView, self.mentionsView, self.commentsView,
                           self.myView]
        self.setupModels()
        self.setupMyUi()
        self.IMG_AVATAR = -2
        self.IMG_THUMB = -1
        self.TIMER_INTERVAL = 30  # TODO: Can be modify with settings window
        self.notify = Notify()
        self.timer = WTimer(self.TIMER_INTERVAL, self.show_notify)
        self.timer.start()

    def setupMyUi(self):
        for tweetView in self.tweetViews:
            tweetView.setResizeMode(tweetView.SizeRootObjectToView)
            tweetView.setSource(
                QtCore.QUrl.fromLocalFile(myself_path + "/ui/TweetList.qml"))
            tweetView.rootContext().setContextProperty("mainWindow", self)

    @QtCore.pyqtSlot()
    def load_more(self):
        if self.tabWidget.currentIndex() == 0:
            self.all_timeline_page += 1
            self.get_all_timeline(self.all_timeline_page)
        elif self.tabWidget.currentIndex() == 1:
            self.mentions_page += 1
            self.get_mentions_timeline(self.mentions_page)
        elif self.tabWidget.currentIndex() == 2:
            self.comment_to_me_page += 1
            self.get_comment_to_me(self.comment_to_me_page)
        elif self.tabWidget.currentIndex() == 3:
            self.my_timeline_page += 1
            self.get_my_timeline(self.my_timeline_page)

    def setupModels(self):
        self.all_timeline = TweetModel(TweetItem(), self)
        self.homeView.rootContext().setContextProperty("mymodel",
                                                       self.all_timeline)
        self.mentions = TweetModel(TweetItem(), self)
        self.mentionsView.rootContext().setContextProperty("mymodel",
                                                           self.mentions)
        self.comment_to_me = TweetModel(TweetItem(), self)
        self.commentsView.rootContext().setContextProperty("mymodel",
                                                           self.comment_to_me)
        self.my_timeline = TweetModel(TweetItem(), self)
        self.myView.rootContext().setContextProperty("mymodel",
                                                     self.my_timeline)

    def get_timeline(self, timeline, model, more=False):
        for count, item in enumerate(timeline):
            # tweet (default), comment or retweet?
            item_type = "tweet"

            # simple tweet or comment
            item_id = item['idstr']
            item_author = item['user']['name']
            item_author_avatar = item['user']['profile_image_url']
            item_content = item['text']
            item_content_time = item['created_at']

            # comment only
            try:
                item_comment_to_original_id = item['status']['idstr']
                item_type = "comment"
            except KeyError:
                # not a comment
                pass

            # original tweet (if retweeted)
            try:
                item_original_id = item['retweeted_status']['idstr']
                item_original_content = item['retweeted_status']['text']
                item_original_author = item['retweeted_status']['user']['name']
                item_original_time = item['retweeted_status']['created_at']
                item_type = "retweet"
            except KeyError:
                # not retweeted
                pass

            # thumb pic
            try:
                item_thumb_pic = None
                item_thumb_pic = item['thumbnail_pic']
            except KeyError:
                try:
                    item_thumb_pic = item['retweeted_status']['thumbnail_pic']
                except KeyError:
                    pass

            # tweet
            tweet = TweetItem(type=item_type, id=item_id, author=item_author,
                              avatar=item_author_avatar, content=item_content,
                              time=item_content_time)

            if item_type == "comment":
                # comment
                tweet = TweetItem(type=item_type, id=item_id,
                                  author=item_author,
                                  avatar=item_author_avatar,
                                  content=item_content, time=item_content_time,
                                  original_id=item_comment_to_original_id)

            if item_type == "retweet":
                # retweet
                tweet = TweetItem(type=item_type, id=item_id,
                                  author=item_author,
                                  avatar=item_author_avatar,
                                  content=item_content, time=item_content_time,
                                  original_id=item_original_id,
                                  original_content=item_original_content,
                                  original_author=item_original_author,
                                  original_time=item_original_time)

            if not item_thumb_pic is None:
                # thumb pic
                tweet.thumbnail_pic = item_thumb_pic

            model.appendRow(tweet)
        self.timelineLoaded.emit(more)

    def get_all_timeline(self, page=1, reset_remind=False, more=False):
        all_timelines = self.client.statuses.home_timeline.get(
            page=page).statuses
        threading.Thread(group=None, target=self.get_timeline,
                         args=(all_timelines, self.all_timeline, more)).start()
        self.all_timeline_page = page
        if reset_remind:
            self.tabWidget.setTabText(0, "Weibo")

    def get_my_timeline(self, page=1, reset_remind=False, more=False):
        my_timelines = self.client.statuses.user_timeline.get(
            page=page).statuses
        threading.Thread(group=None, target=self.get_timeline,
                         args=(my_timelines, self.my_timeline, more)).start()
        self.my_timeline_page = page

    def get_mentions_timeline(self, page=1, reset_remind=False, more=False):
        mentions_timelines = self.client.statuses.mentions.get(
            page=page).statuses
        threading.Thread(group=None, target=self.get_timeline,
                         args=(
                             mentions_timelines, self.mentions, more)).start()
        self.mentions_page = page
        if reset_remind:
            self.client.remind.set_count.post(type="mention_status")
            self.tabWidget.setTabText(1, "@ME")

    def get_comment_to_me(self, page=1, reset_remind=False, more=False):
        comments_to_me = self.client.comments.to_me.get(page=page).comments
        threading.Thread(group=None, target=self.get_timeline, args=(
            comments_to_me, self.comment_to_me, more)).start()
        self.comment_to_me_page = page
        if reset_remind:
            self.client.remind.set_count.post(type="cmt")
            self.tabWidget.setTabText(2, "Comments")

    def get_remind(self, uid):
        '''this function is used to get unread_count
        from Weibo API. uid is necessary.'''

        reminds = self.client.remind.unread_count.get(uid=uid)
        return reminds

    def get_uid(self):
        '''How can I get my uid? here it is'''
        try:
            self.uid = self.client.account.get_uid.get().uid
        except AttributeError:
            return None

    def show_notify(self):
        # This function is run in another thread by WTimer.
        # Do not modify UI directly. Send signal and react it in a slot only.
        # We use SIGNAL self.tabTextChanged and SLOT self.setTabText()
        # to display unread count

        # HACK: not login yet, pass notify checking
        if not self.isVisible():
            return

        reminds = self.get_remind(self.uid)
        msg = "You have:\n"
        num_msg = 0
        # TODO: we need settings window, to controll their displaying or not
        if reminds['status'] != 0:
            # Note: do NOT send notify here, or users will crazy.
            self.tabTextChanged.emit(0, "Weibo(%d)" % reminds['status'])

        if reminds['mention_status'] != 0:
            msg += "%d unread @ME\n" % reminds['mention_status']
            self.tabTextChanged.emit(1,
                                       "@Me(%d)" % reminds['mention_status'])
            num_msg += 1

        if reminds['cmt'] != 0:
            msg += "%d unread comment(s)\n" % reminds['cmt']
            self.tabTextChanged.emit(2, "Comments(%d)" % reminds['cmt'])
            num_msg += 1

        if num_msg != 0:
            #TODO: image can use our images in rcc
            self.notify.showMessage("WeCase", msg,
                                    image="notification-message-email")

    def setTabText(self, index, string):
        self.tabWidget.setTabText(index, string)

    def moveToTop(self, more):
        if more:
            self.get_current_tweetView().rootObject().positionViewAtBeginning()

    def setLoaded(self, tweetid):
        self.get_current_tweetView().rootObject().imageLoaded(tweetid)

    def showSettings(self):
        wecase_settings.show()

    def showAbout(self):
        wecase_about.show()

    def logout(self):
        wecase_login.show()
        self.close()

    def postTweet(self):
        wecase_new = NewpostWindow()
        wecase_new.client = self.client
        wecase_new.exec_()

    @QtCore.pyqtSlot(str)
    def comment(self, idstr):
        wecase_new = NewpostWindow(action="comment", id=int(idstr))
        wecase_new.client = self.client
        wecase_new.exec_()

    @QtCore.pyqtSlot(str, str)
    def repost(self, idstr, text):
        wecase_new = NewpostWindow(action="retweet", id=int(idstr), text=text)
        wecase_new.client = self.client
        wecase_new.exec_()

    @QtCore.pyqtSlot(str, result=int)
    def favorite(self, idstr):
        try:
            self.client.favorites.create.post(id=int(idstr))
            return True
        except:
            return False

    @QtCore.pyqtSlot(str, result=bool)
    def un_favorite(self, idstr):
        try:
            self.client.favorites.destroy.post(id=int(idstr))
            return True
        except:
            return False

    @QtCore.pyqtSlot(str, str)
    def reply(self, idstr, cidstr):
        wecase_new = NewpostWindow(action="reply", id=int(idstr),
                                   cid=int(cidstr))
        wecase_new.client = self.client
        wecase_new.exec_()

    @QtCore.pyqtSlot(str, str)
    def look_orignal_pic(self, thumbnail_pic, tweetid):
        threading.Thread(group=None, target=self.fetch_open_original_pic,
                         args=(thumbnail_pic, tweetid)).start()

    def fetch_open_original_pic(self, thumbnail_pic, tweetid):
        """Fetch and open original pic from thumbnail pic url.
           Pictures will stored in cache directory. If we already have a same
           name in cache directory, just open it. If we don't, then download it
           first."""
        # XXX: This function is NOT thread-safe!
        # Click a single picture for many time will download a image for many
        # times, and the picture may be overwrite, we will get a broken image.

        original_pic = thumbnail_pic.replace("thumbnail",
                                             "large")  # A simple trick ... ^_^
        localfile = cache_path + original_pic.split("/")[-1]
        if not os.path.exists(localfile):
            urllib.request.urlretrieve(original_pic, localfile)

        os.popen("xdg-open " + localfile)  # xdg-open is common?
        self.imageLoaded.emit(tweetid)

    def refresh(self):
        model = self.get_current_model()
        get_timeline = self.get_current_function()

        model.clear()
        get_timeline(page=1, reset_remind=True, more=True)

    def get_current_tweetView(self):
        tweetViews = {0: self.homeView, 1: self.mentionsView,
                      2: self.commentsView, 3: self.myView}
        return tweetViews[self.tabWidget.currentIndex()]

    def get_current_model(self):
        models = {0: self.all_timeline, 1: self.mentions,
                  2: self.comment_to_me,
                  3: self.my_timeline}
        return models[self.tabWidget.currentIndex()]

    def get_current_function(self):
        functions = {0: self.get_all_timeline, 1: self.get_mentions_timeline,
                     2: self.get_comment_to_me, 3: self.get_my_timeline}
        return functions[self.tabWidget.currentIndex()]


class WeSettingsWindow(QtGui.QDialog, Ui_SettingWindow):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)


class NewpostWindow(QtGui.QDialog, Ui_NewPostWindow):
    client = None
    image = None
    apiError = QtCore.pyqtSignal(str)
    sendSuccessful = QtCore.pyqtSignal()

    def __init__(self, parent=None, action="new", id=None, cid=None, text=""):
        QtGui.QDialog.__init__(self, parent)
        self.script = JavaScript(QtCore.QUrl.fromLocalFile(myself_path + "/ui/JavaScript.qml"))
        self.action = action
        self.id = id
        self.cid = cid
        self.setupUi(self)
        self.textEdit.setText(text)
        self.checkChars()
        self.notify = Notify(time=1)

    def setupMyUi(self):
        if self.action == "new":
            self.pushButton_send.clicked.connect(self.send_tweet)

    def send(self):
        if self.action == "new":
            threading.Thread(group=None, target=self.new).start()
        elif self.action == "retweet":
            threading.Thread(group=None, target=self.retweet).start()
        elif self.action == "comment":
            threading.Thread(group=None, target=self.comment).start()
        elif self.action == "reply":
            threading.Thread(group=None, target=self.reply).start()

    def retweet(self):
        text = str(self.textEdit.toPlainText())
        try:
            self.client.statuses.repost.post(id=int(self.id), status=text)
            self.notify.showMessage("WeCase", "Retweet Success!")
            self.sendSuccessful.emit()
        except APIError as e:
            self.apiError.emit(str(e))
            return

    def comment(self):
        text = str(self.textEdit.toPlainText())
        try:
            self.client.comments.create.post(id=int(self.id), comment=text)
            self.notify.showMessage("WeCase", "Comment Success!")
            self.sendSuccessful.emit()
        except APIError as e:
            self.apiError.emit(str(e))
            return

    def reply(self):
        text = str(self.textEdit.toPlainText())
        try:
            self.client.comments.reply.post(id=int(self.id), cid=int(self.cid),
                                            comment=text)
            self.notify.showMessage("WeCase", "Reply Success!")
            self.sendSuccessful.emit()
        except APIError as e:
            self.apiError.emit(str(e))
            return

    def new(self):
        text = str(self.textEdit.toPlainText())

        try:
            if self.image:
                self.client.statuses.upload.post(status=text,
                                                 pic=open(self.image, "rb"))
            else:
                self.client.statuses.update.post(status=text)

            self.notify.showMessage("WeCase", "Tweet Success!")
            self.sendSuccessful.emit()
        except APIError as e:
            self.apiError.emit(str(e))
            return

        self.image = None

    def addImage(self):
        ACCEPT_TYPE = "Images (*.png *.jpg *.bmp *.gif)"
        if self.image:
            self.image = None
            self.pushButton_picture.setText("Picture")
        else:
            self.image = QtGui.QFileDialog.getOpenFileName(self,
                                                           "Choose a image",
                                                           filter=ACCEPT_TYPE)
            self.pushButton_picture.setText("Remove the picture")

    def showError(self, e):
        if "Text too long" in e:
            QtGui.QMessageBox.warning(None, "Text too long!",
                                      "Please remove some text.")
        else:
            QtGui.QMessageBox.warning(None, "Unknown error!", e)

    def checkChars(self):
        '''Check textEdit's characters.
        If it larger than 140, Send Button will be disabled
        and label will show red chars.'''

        text = self.textEdit.toPlainText()
        numLens = 140 - self.script.fucking_getLength(text, 140)
        if numLens >= 0:
            self.label.setStyleSheet("color:black;")
            self.pushButton_send.setEnabled(True)
        else:
            self.label.setStyleSheet("color:red;")
            self.pushButton_send.setEnabled(False)
        self.label.setText(str(numLens))


class Notify():
    def __init__(self, appname="WeCase", time=5):
        pynotify.init(appname)
        self.timeout = time
        self.n = pynotify.Notification(appname)

    def showMessage(self, title, text, image=""):
        self.n.update(title, text, image)
        # TODO: user should be able to adjust the time by settings window
        self.n.set_timeout(self.timeout * 1000)
        self.n.show()


class AboutWindow(QtGui.QDialog, Ui_About_Dialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)


class JavaScript():
    def __init__(self, file):
        self.view = QtDeclarative.QDeclarativeView()
        self.view.setSource(file)

    def __getattr__(self, name):
        obj = eval("self.view.rootObject().%s" % name)
        return obj


if __name__ == "__main__":
    try:
        os.mkdir(config_path.replace("/config_db", ""))
    except OSError:
        pass

    try:
        os.mkdir(cache_path)
    except OSError:
        pass

    app = QtGui.QApplication(sys.argv)

    wecase_main = WeCaseWindow()
    wecase_login = LoginWindow()
    wecase_settings = WeSettingsWindow()
    wecase_about = AboutWindow()

    exit_status = app.exec_()

    # Cleanup code here.
    # stop notify thread
    wecase_main.timer.stopped = True

    sys.exit(exit_status)
