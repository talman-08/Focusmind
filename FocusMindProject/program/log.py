import sys
import os
import sqlite3
import json
import hashlib

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QPushButton,
    QLabel, QLineEdit, QWidget, QVBoxLayout
)
from PyQt5.QtGui import QPalette, QColor, QIcon, QFont
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtCore import Qt, QSize


 
#         LOGIN WINDOW
 
class LoginApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Title and geometry (iPhone 13 Pro size style)
        self.setWindowTitle("Login System")
        self.setGeometry(100, 100, 390, 844)

        #color to window:
        pal = self.palette()
        pal.setColor(QPalette.Window, QColor(144, 238, 144))  # To light-Green (RGB: 144, 238, 144)
        self.setPalette(pal)
        
        # Creating unified layout-window
        layout = QVBoxLayout()

        # 🔹 Unique FocusMind Header with bold font size 28
        self.label_header = QLabel("FocusMind", self)
        self.label_header.setAlignment(Qt.AlignCenter)
        header_font = QFont()
        header_font.setPointSize(28)  # Increased size for clarity
        header_font.setBold(True)
        self.label_header.setFont(header_font)
        self.label_header.setStyleSheet("color: #333; padding: 10px;")
        layout.addWidget(self.label_header)

        # Email field
        self.label_email = QLabel("Email:", self)
        layout.addWidget(self.label_email)
        self.input_email = QLineEdit(self)
        layout.addWidget(self.input_email)

        # Password field
        self.label_password = QLabel("Password:", self)
        layout.addWidget(self.label_password)
        self.input_password = QLineEdit(self)
        self.input_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.input_password)

        # Login button
        self.button_login = QPushButton("Login", self)
        self.button_login.setStyleSheet("background-color: lightgreen;")
        self.button_login.clicked.connect(self.login)
        layout.addWidget(self.button_login)

        # Sign Up button
        self.button_signup = QPushButton("Sign Up", self)
        self.button_signup.setStyleSheet("background-color: lightgreen;")
        self.button_signup.clicked.connect(self.open_signup)
        layout.addWidget(self.button_signup)

        # Forgot Password button
        self.button_reset_password = QPushButton("Forgot Password?", self)
        self.button_reset_password.setStyleSheet("background-color: lightgreen;")
        self.button_reset_password.clicked.connect(self.open_password_reset)
        layout.addWidget(self.button_reset_password)

    

        # Set layout to container widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def login(self):
        email = self.input_email.text().strip()
        password = self.input_password.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Login Failed", "Please enter email and password.")
            return

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            conn.close()

            if row:
                stored_hash = row[0]
                input_hash = hashlib.sha256(password.encode()).hexdigest()
                if stored_hash == input_hash:
                    QMessageBox.information(self, "Login Success", "Welcome!")
                    # Open the unique emoji (FeelApp) page
                    self.feelings = FeelApp()
                    self.feelings.show()
                    self.close()  # Close the login window upon success
                else:
                    QMessageBox.warning(self, "Login Failed", "Incorrect password.")
            else:
                QMessageBox.warning(self, "Login Failed", "Email not found.")
        except Exception as ex:
            QMessageBox.warning(self, "Login Failed", "An error occurred: " + str(ex))

    def logout(self):
        # For the login screen, simply clear the fields and show an info message.
        self.input_email.clear()
        self.input_password.clear()
        QMessageBox.information(self, "Logged Out", "You are already at the login screen.")

    def open_signup(self):
        self.signup_window = SignupApp()
        self.signup_window.show()

    def open_password_reset(self):
        self.reset_window = PasswordResetApp()
        self.reset_window.show()


 
#      PASSWORD RESET WINDOW
 
class PasswordResetApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Reset Password")
        self.setGeometry(150, 150, 300, 200)

        pal = self.palette()
        pal.setColor(QPalette.Window, QColor(144, 238, 144))
        self.setPalette(pal)

        layout = QVBoxLayout()

        # Email field for reset
        self.label_email = QLabel("Email:", self)
        layout.addWidget(self.label_email)
        self.input_email = QLineEdit(self)
        layout.addWidget(self.input_email)

        # New Password field
        self.label_new_password = QLabel("New Password:", self)
        layout.addWidget(self.label_new_password)
        self.input_new_password = QLineEdit(self)
        self.input_new_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.input_new_password)

        # Reset Password button
        self.button_reset = QPushButton("Reset Password", self)
        self.button_reset.setStyleSheet("background-color: lightgreen;")
        self.button_reset.clicked.connect(self.reset_password)
        layout.addWidget(self.button_reset)

        # Logout button
        self.logout_button = QPushButton("Logout", self)
        self.logout_button.setStyleSheet("background-color: red; color: white;")
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def reset_password(self):
        email = self.input_email.text().strip()
        new_pass = self.input_new_password.text().strip()

        if not email or not new_pass:
            QMessageBox.warning(self, "Reset Failed", "Please enter email and new password.")
            return

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            hashed_pass = hashlib.sha256(new_pass.encode()).hexdigest()
            cursor.execute("UPDATE users SET password=? WHERE email=?", (hashed_pass, email))
            if cursor.rowcount == 0:
                QMessageBox.warning(self, "Reset Failed", "Email not found.")
            else:
                conn.commit()
                QMessageBox.information(self, "Password Reset", "Your password has been updated.")
                self.close()
        except Exception as err:
            QMessageBox.warning(self, "Reset Failed", "An error occurred: " + str(err))
        finally:
            conn.close()

    def logout(self):
        self.close()
        self.login_window = LoginApp()
        self.login_window.show()


# ================================
#         SIGN UP WINDOW
# ================================
class SignupApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Sign Up")
        self.setGeometry(150, 150, 300, 200)

        layout = QVBoxLayout()

        self.label_username = QLabel("Username:", self)
        layout.addWidget(self.label_username)
        self.input_username = QLineEdit(self)
        layout.addWidget(self.input_username)

        self.label_password = QLabel("Password:", self)
        layout.addWidget(self.label_password)
        self.input_password = QLineEdit(self)
        self.input_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.input_password)

        self.label_email = QLabel("Email:", self)
        layout.addWidget(self.label_email)
        self.input_email = QLineEdit(self)
        layout.addWidget(self.input_email)

        self.label_full_name = QLabel("Full Name:", self)
        layout.addWidget(self.label_full_name)
        self.input_full_name = QLineEdit(self)
        layout.addWidget(self.input_full_name)

        self.button_signup = QPushButton("Sign Up", self)
        self.button_signup.clicked.connect(self.signup)
        self.button_signup.setStyleSheet("background-color: lightgreen;")
        layout.addWidget(self.button_signup)

        # Logout button
        self.logout_button = QPushButton("Logout", self)
        self.logout_button.setStyleSheet("background-color: red; color: white;")
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def signup(self):
        uname = self.input_username.text().strip()
        email = self.input_email.text().strip()
        passwd = self.input_password.text().strip()
        fullname = self.input_full_name.text().strip()

        if not uname or not email or not passwd:
            QMessageBox.warning(self, "Sign Up Failed", "Username, email, and password cannot be empty.")
            return

        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    full_name TEXT
                )
            ''')
            cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (uname, email))
            if cursor.fetchone():
                QMessageBox.warning(self, "Sign Up Failed", "Username or email already registered.")
                conn.close()
                return

            hashed = hashlib.sha256(passwd.encode()).hexdigest()
            cursor.execute(
                "INSERT INTO users (username, email, password, full_name) VALUES (?, ?, ?, ?)",
                (uname, email, hashed, fullname)
            )
            conn.commit()
            QMessageBox.information(self, "Sign Up Success", "User registered successfully!")
            self.close()
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Sign Up Failed", "Could not create account: " + str(e))
        finally:
            conn.close()

    def logout(self):
        self.close()
        self.login_window = LoginApp()
        self.login_window.show()


# ================================
#         FEELINGS PAGE
# ================================
class FeelApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Unique direct path to feelings.ui inside the program directory.
        ui_file = os.path.join(os.path.dirname(__file__), "feelings.ui")
        if not os.path.exists(ui_file):
            QMessageBox.critical(self, "Error", f"UI file not found: {ui_file}")
            sys.exit(1)

        print(f"Loading UI from: {ui_file}")
        uic.loadUi(ui_file, self)

        self.create_database()

        # Unique styling for FeelApp
        self.setStyleSheet("""
            QMainWindow {
                background-color: #D8BFD8;
                background-repeat: repeat;
                background-position: center;
            }
            QPushButton {
                background: none;
                border: none;
            }
            QPushButton::icon {
                width: 126px;
                height: 126px;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
                text-align: center;
            }
        """)

        self.setup_connections()

        self.exercises = {
            "Happy": "Practice gratitude: Write down three things you are grateful for today.",
            "Neutral": "Take a mindful walk: Observe your surroundings and focus on your breathing.",
            "Sad": "Journaling: Write down your thoughts and emotions freely for 10 minutes.",
            "Relaxed": "Deep breathing: Inhale for 4 seconds, hold for 4, exhale for 4.",
            "Anxious": "Progressive muscle relaxation: Tense and relax each muscle group slowly.",
            "Stressed": "5-minute meditation: Close your eyes and focus on your breath."
        }

        # Start at the emotion selection page
        self.stackedWidget.setCurrentIndex(0)

        # Add a unique logout button positioned at the top-right
        self.logout_button = QPushButton("Logout", self)
        self.logout_button.setStyleSheet("background-color: red; color: white;")
        self.logout_button.setGeometry(self.width() - 90, 10, 80, 30)
        self.logout_button.clicked.connect(self.logout)

    def setup_connections(self):
        try:
            self.btnHappy.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "images", "happy.png")))
            self.btnNeutral.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "images", "neutral.png")))
            self.btnSad.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "images", "sad.png")))
            self.btnRelaxed.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "images", "relaxed.png")))
            self.btnAnxious.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "images", "anxious.png")))
            self.btnStressed.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "images", "stressed.png")))

            self.btnHappy.setIconSize(QSize(126, 126))
            self.btnNeutral.setIconSize(QSize(126, 126))
            self.btnSad.setIconSize(QSize(126, 126))
            self.btnRelaxed.setIconSize(QSize(126, 126))
            self.btnAnxious.setIconSize(QSize(126, 126))
            self.btnStressed.setIconSize(QSize(126, 126))

            self.btnHappy.clicked.connect(lambda: self.show_exercise("Happy"))
            self.btnNeutral.clicked.connect(lambda: self.show_exercise("Neutral"))
            self.btnSad.clicked.connect(lambda: self.show_exercise("Sad"))
            self.btnRelaxed.clicked.connect(lambda: self.show_exercise("Relaxed"))
            self.btnAnxious.clicked.connect(lambda: self.show_exercise("Anxious"))
            self.btnStressed.clicked.connect(lambda: self.show_exercise("Stressed"))
            self.pushButton.clicked.connect(self.go_back)  # Back button
        except AttributeError:
            QMessageBox.critical(self, "Error", "UI elements not found. Check the UI file.")

    def show_exercise(self, emotion):
        self.textEdit.setText(self.exercises.get(emotion, "Please select an emotion."))
        self.stackedWidget.setCurrentIndex(1)

    def go_back(self):
        self.stackedWidget.setCurrentIndex(0)

    def create_database(self):
        conn = sqlite3.connect("feelings.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feelings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                emotion TEXT NOT NULL,
                exercise TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def logout(self):
        self.close()
        self.login_window = LoginApp()
        self.login_window.show()


# ================================
#           MAIN
# ================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = LoginApp()
    main_window.show()
    sys.exit(app.exec_())
