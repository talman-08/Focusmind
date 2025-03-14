import sys
import pytest
from PyQt5.QtWidgets import QApplication, QMainWindow
from program.log import LoginApp  


def test_login_valid_credentials():
    app = QApplication(sys.argv)
    window = LoginApp()
    window.input_username.setText("testuser")
    window.input_password.setText("testpassword")
    window.login()  
    assert window.input_username.text() == "testuser"
    assert window.input_password.text() == "testpassword"


def test_login_invalid_credentials():
    app = QApplication(sys.argv)
    window = LoginApp()
    window.input_username.setText("wronguser")
    window.input_password.setText("wrongpassword")
    window.login() 
    assert window.input_username.text() == "wronguser"
    assert window.input_password.text() == "wrongpassword"


def test_login_empty_credentials():
    app = QApplication(sys.argv)
    window = LoginApp()
    window.input_username.setText("") 
    window.input_password.setText("") 
    window.login()  
    assert window.input_username.text() == ""
    assert window.input_password.text() == ""


def test_successful_signup():
    app = QApplication(sys.argv)
    window = LoginApp()
    window.open_signup()  
   
    assert window.signup_window is not None
