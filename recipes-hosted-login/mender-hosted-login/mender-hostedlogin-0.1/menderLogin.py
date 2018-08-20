import sys
import requests
import re
import os
import json

from PyQt5 import QtCore, QtGui, QtWidgets
from menderLoginGUI import Ui_MainWindow

"""
This is the main GUI login application for logging in to Hosted Mender
and fetching the tenant token.
NOTE: This is the editable GUI-file, while menderLoginGUI.py is generated
      by Qt-creator.
"""

class LogInWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    # Base url: can also be set in gui textfield "server_addr"
    url_base = "https://hosted.mender.io"
    def __init__(self, parent=None):
        super(LogInWindow, self).__init__(parent)

        # Setup window to fixed size without frame and always on top
        self.setupUi(self)
        self.__expand_window__()
        self.setWindowFlags(QtCore.Qt.Window |
                            QtCore.Qt.CustomizeWindowHint |
                            QtCore.Qt.WindowStaysOnTopHint)

        # Move window to center of the screen
        qtRectangle = self.frameGeometry()
        screenCenter = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(screenCenter)
        self.move(qtRectangle.topLeft())

        # Setup button event functions
        self.logInBtn.setDisabled(True)
        self.logInBtn.setShortcut("Return")
        self.quitBtn.clicked.connect(self._quit_clicked)
        self.logInBtn.clicked.connect(self._logIn_clicked)
        self.serverCheckBox.clicked.connect(self._server_checked)
        self.showPwd.clicked.connect(self._show_pwd)

        # Setup line edit event functions
        self.usr.textChanged.connect(self._txt_change)
        self.pwd.textChanged.connect(self._txt_change)
        self.server_addr.editingFinished.connect(self._domain_changed)

    def __expand_window__(self):
        # Expand widget to cover the whole screen and move items relatively
        #    - looks prettier on sato
        frameRes = self.frameGeometry()
        screenRes = QtWidgets.QDesktopWidget().screenGeometry().size()
        self.setFixedSize(screenRes)
        frameBig = self.frameGeometry()
        frameDiff2 = (frameBig.size() - frameRes.size())/2
        # Move all items accordingly
        boxGeometry = self.usr.geometry()
        self.usr.move(boxGeometry.x() + frameDiff2.width(), \
                      boxGeometry.y() + frameDiff2.height())
        boxGeometry = self.pwd.geometry()
        self.pwd.move(boxGeometry.x() + frameDiff2.width(), \
                      boxGeometry.y() + frameDiff2.height())
        boxGeometry = self.label.geometry()
        self.label.move(boxGeometry.x() + frameDiff2.width(), \
                      boxGeometry.y() + frameDiff2.height())
        boxGeometry = self.logInBtn.geometry()
        self.logInBtn.move(boxGeometry.x() + frameDiff2.width(), \
                      boxGeometry.y() + frameDiff2.height())
        boxGeometry = self.quitBtn.geometry()
        self.quitBtn.move(boxGeometry.x() + frameDiff2.width(), \
                      boxGeometry.y() + frameDiff2.height())
        boxGeometry = self.showPwd.geometry()
        self.showPwd.move(boxGeometry.x() + frameDiff2.width(), \
                      boxGeometry.y() + frameDiff2.height())
        boxGeometry = self.server_addr.geometry()
        self.server_addr.move(boxGeometry.x() + frameDiff2.width(), \
                      boxGeometry.y() + frameDiff2.height())
        boxGeometry = self.serverCheckBox.geometry()
        self.serverCheckBox.move(boxGeometry.x() + frameDiff2.width(), \
                      boxGeometry.y() + frameDiff2.height())
        boxGeometry = self.domain_label.geometry()
        self.domain_label.move(boxGeometry.x() + frameDiff2.width(), \
                      boxGeometry.y() + frameDiff2.height())


    def _txt_change(self):
        # check if user has entered a valid user name (e-mail)
        # and the password is longer than 5 characters. And
        # enable/disable log in button accordingly
        res = re.search(".+@.+\..+", self.usr.text())
        if res == None:
            self.logInBtn.setDisabled(True)
        elif len(self.pwd.text()) > 5:
            self.logInBtn.setDisabled(False)

    def _quit_clicked(self):
        # Open dialog (sure you want to leave)
        _exit = QtWidgets.QMessageBox.question(self, "Exit",
                                               "Are you sure you want to exit?",
                                               QtWidgets.QMessageBox.Yes |
                                               QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if (_exit == QtWidgets.QMessageBox.Yes):
            QtCore.QCoreApplication.instance().quit()

    def _do_login(self, username, password):
        # Attempt login using username/password from respective line edits
        url = self.url_base + "/api/management/v1/useradm/auth/login"
        try:
            r = requests.post(url,
                              auth=requests.auth.HTTPBasicAuth(username, password))
        except (requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema,
                requests.exceptions.MissingSchema):
            # Print error and show error dialog for invalid URL
            print(sys.exc_info()[0])
            QtWidgets.QMessageBox.warning(self, "Invalid URL",
                                          "Invalid URL: %s" % self.url_base)
            return None
        except requests.exceptions.SSLError:
            # Show error dialog for SSL-cert error
            QtWidgets.QMessageBox.warning(self, "SSL error",
                                          "Could not POST to: %s" % url)
            return None
        except requests.exceptions.Timeout:
            QtWidgets.QMessageBox.warning(self, "Connection timeout",
                                          "Connection timed out")
            return None
        except:
            # Unexpected error
            print(sys.exc_info()[0])
            QtWidgets.QMessageBox.warning(self, "Unexpected Error",
                                          "Could not POST to: %s" % url)
            return None
        return r

    def _logIn_clicked(self):
        # Curl for tenant token
        # Dialog with status (success / failure (invalid credential etc))
        usrName = self.usr.text()
        usrPwd  = self.pwd.text()
        r = self._do_login(usrName, usrPwd)
        if r == None:
            return
        elif (r.status_code == 401):
            # Unauthorized: wrong username or password
            msg = QtWidgets.QMessageBox.warning(self, "Log in failed",
                                                "Log in failed: Wrong user name or password")
            return
        elif (r.status_code != 200):
            # Unexpected status code
            msg = QtWidgets.QMessageBox.warning(self, "Log in failed",
                                                "Error: Bad statuscode: %d" %
                                                r.status_code)
            return

        # Get tenant token from Hosted Mender
        header = {"Authorization": "Bearer " + str(r.text)}
        url = self.url_base + "/api/management/v1/tenantadm/user/tenant"
        try:
            r = requests.get(url, headers=header)
        except (requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema,
                requests.exceptions.MissingSchema):
            # Invalid URL / Invalid schema (missing https://)
            QtWidgets.QMessageBox.warning(self, "Invalid URL",
                                          "Invalid URL: %s" % self.url_base)
            return
        except:
            QtWidgets.QMessageBox.warning(self, "Unexpected Error",
                                          "Could not GET from: %s" % url)
            return
        f = None
        f_tmp = None
        p_tmp = None
        data = {}

        # open mender.conf and add/rewrite tenant token
        if os.path.exists("/etc/mender/mender.conf"):
            try:
                # Load conf into dict
                f = open("/etc/mender/mender.conf", "r")
                data = json.load(f)

                # Add TenantToken entry
                data["TenantToken"] = r.json()["tenant_token"]
                # Ensure that URL is set correctly
                data["ServerURL"] = self.url_base
                # Write temporary conf
                f_tmp = open("/tmp/mender.conf.tmp", "w+")
                # Rewrite mender.conf
                json.dump(data, f_tmp, indent=2, sort_keys=True)

                # Also write the tenant token to a persistent file
                # this will be restored into mender.conf by the mender.service
                # launch script.
                p_tmp = open("/data/mender/hosted-mender-settings.dat", "w")
                p_tmp.write(data["TenantToken"])
                p_tmp.write("\n")
                p_tmp.write(data["ServerURL"])
                p_tmp.write("\n")
            except:
                QtWidgets.QMessageBox.warning(self, "I/O Error",
                                              "Could not write token to /etc/mender.conf")
                print("Hosted Mender tenant token:\n%s" % data["TenantToken"])
                return
            finally:
                if f != None:
                    f.close()
                if f_tmp != None:
                    f_tmp.close()
                if p_tmp != None:
                    p_tmp.close()

        else: # not os.path.exists()
            # (Should not occur)
            os.makedirs("/etc/mender")
            try:
                f = open("/tmp/mender.conf.tmp", "w")
                # Create a new configuration holding the tenant token
                data = {"TenantToken": r.json()["tenant_token"], \
                        "ServerURL": self.url_base}
                # Rewrite mender.conf
                json.dump(data, f, indent=2)
            except:
                print("Hosted Mender tenant token:\n%s" % data["TenantToken"])
                QtWidgets.QMessageBox.warning(self, "I/O Error",
                                              "Could not write token to /etc/mender.conf")
                return
            finally:
                if f != None:
                    f.close()

        # This is a bit hacky; maybe there's a better solution (TODO)
        os.system("sudo mv /tmp/mender.conf.tmp /etc/mender/mender.conf")
        os.system("sudo mv /etc/xdg/autostart/mender-hostedlogin.desktop " + \
                          "/etc/mender/login/mender-hostedlogin.desktop")
        # Token successfully written to /etc/mender.conf
        QtWidgets.QMessageBox.information(self, "Success",
                                          "Successfully stored your Hosted Mender token")
        QtCore.QCoreApplication.instance().quit()

    def _domain_changed(self):
        # text entered in domain name: change self.url_base
        if self.server_addr.text() == "":
            self.url_base = "https://hosted.mender.io"
        else:
            # prepend "https://" if user doesn't
            if self.server_addr.text().startswith("https://"):
                self.url_base = self.server_addr.text()
            else:
                self.server_addr.setText("https://" + self.server_addr.text())
                self.url_base = self.server_addr.text()

    def _server_checked(self):
        # checkBox callback: toggle textfield editable
        if self.serverCheckBox.isChecked():
            self.server_addr.setReadOnly(False)
            self.server_addr.setFrame(True)
        else:
            self.server_addr.setReadOnly(True)
            self.server_addr.setFrame(False)
            self.server_addr.setText("")
            self._domain_changed()

    def _show_pwd(self):
        # check box showPwd callback: toggle hidden/normal echo mode
        if self.showPwd.isChecked():
            self.pwd.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.pwd.setEchoMode(QtWidgets.QLineEdit.Password)




if __name__ == "__main__":
    if os.getcwd() != "/etc/mender/login":
        # Make sure we're in the correct directory
        if not os.path.exists("/etc/mender/login"):
            os.makedirs("/etc/mender/login")
        os.chdir("/etc/mender/login")
    # Start Qt widget
    app = QtWidgets.QApplication(sys.argv)
    # Create log in window
    win = LogInWindow()
    # Display window
    win.show()
    # Execute widget application threads
    app.exec_()
