import sys 
import pyrebase
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton, QLabel, QLineEdit, QWidget, QVBoxLayout
from PyQt5.QtGui import QPalette, QColor
import os
import sqlite3
from PyQt5 import uic
from PyQt5.QtCore import *

from PyQt5.QtWidgets import * #QApplication, QMainWindow, QMessageBox, QPushButton, QLabel, QLineEdit, QWidget, QVBoxLayout
from PyQt5.QtGui import * #QPalette, QColor


# Firebase configuration
firebase_config = { 
      "apiKey": "AIzaSyAW2QHXrcXseMXaxa7Jet662FSCumMveTI",
  "authDomain": "focus-71f5f.firebaseapp.com",
  "databaseURL": "https://focus-71f5f-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "focus-71f5f",
  "storageBucket": "focus-71f5f.firebasestorage.app",
  "messagingSenderId": "596802463261",
  "appId": "1:596802463261:web:cbc1c7e10b2b17168a88f4",
  "measurementId": "G-3VGLMKD90G"
}


firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

class LoginApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Login System")
        self.setGeometry(100, 100, 300, 200)

        palette = self.palette()

        palette.setColor(QPalette.Window, QColor(0,128,0))
        self.setPalette(palette)
        layout = QVBoxLayout()

        self.label_email = QLabel("Email:")
        layout.addWidget(self.label_email)
        self.input_email = QLineEdit(self)
        layout.addWidget(self.input_email)

        self.label_password = QLabel("Password:")
        layout.addWidget(self.label_password)
        self.input_password = QLineEdit(self)
        self.input_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.input_password)

        self.button_login = QPushButton("Login", self)
        self.button_login.setStyleSheet("background-color: lightgreen;")
        self.button_login.clicked.connect(self.login)
        layout.addWidget(self.button_login)

        self.button_signup = QPushButton("Sign Up", self)
        self.button_signup.setStyleSheet("background-color: lightgreen;")
        self.button_signup.clicked.connect(self.signup)
        layout.addWidget(self.button_signup)

        self.button_reset_password = QPushButton("Forgot Password?", self)
        self.button_reset_password.setStyleSheet("background-color: lightgreen;")
        self.button_reset_password.clicked.connect(self.reset_password)
        layout.addWidget(self.button_reset_password)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def login(self):
        username = self.input_username.text()
        password = self.input_password.text()

        db = firebase.database()
        user_data = db.child("users").child(username).get().val()

        if user_data:
            email = user_data['email']  # Retrieve email from username
            try:
                auth.sign_in_with_email_and_password(email, password)
                QMessageBox.information(self, "Login Success", "Welcome!")
            except:
                QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
        else:
            QMessageBox.warning(self, "Login Failed", "Username not found.")

    def signup(self):
        username = self.input_email.text() # username/email 
        password = self.input_password.text()
        email = self.input_email.text()

        try:
            user = auth.create_user_with_email_and_password(email, password)
            uid = user['localId']

            # Store username in Firebase Realtime Database
            db = firebase.database()
            db.child("users").child(username).set({"email": email, "uid": uid})

            QMessageBox.information(self, "Sign Up Success", "Account created successfully!")
        except:
            QMessageBox.warning(self, "Sign Up Failed", "Could not create account.")

    


     



    def reset_password(self):
        email = self.input_email.text()
        try:
            auth.send_password_reset_email(email)
            QMessageBox.information(self, "Reset Email Sent", "Check your email for reset link.")
        except:
            QMessageBox.warning(self, "Error", "Could not send reset email.")

            #Feelings page (Emojies) will be open here
            self.feelings = FeelApp()
            self.feelings.show()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")


    def open_signup(self):
        self.signup_window = SignupApp()
        self.signup_window.show()

    def open_password_reset(self):
        self.reset_window = PasswordResetApp()
        self.reset_window.show()


class PasswordResetApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Reset Password")
        self.setGeometry(150, 150, 300, 200)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(144, 238, 144))
        self.setPalette(palette)

        layout = QVBoxLayout()
        
        self.label_username = QLabel("Username:")
        layout.addWidget(self.label_username)
        self.input_username = QLineEdit(self)
        layout.addWidget(self.input_username)
        
        self.label_new_password = QLabel("New Password:")
        layout.addWidget(self.label_new_password)
        self.input_new_password = QLineEdit(self)
        self.input_new_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.input_new_password)
        
        self.button_reset = QPushButton("Reset Password", self)
        self.button_reset.setStyleSheet("background-color: lightgreen;")
        self.button_reset.clicked.connect(self.reset_password)
        layout.addWidget(self.button_reset)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def reset_password(self):
        username = self.input_username.text()
        new_password = self.input_new_password.text()

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password=? WHERE username=?", (new_password, username))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Password Reset", "Your password has been updated.")
        self.close()


class SignupApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Sign Up")
        self.setGeometry(150, 150, 300, 200)

        layout = QVBoxLayout()

        self.label_username = QLabel("Username:")
        layout.addWidget(self.label_username)
        self.input_username = QLineEdit(self)
        layout.addWidget(self.input_username)

        self.label_password = QLabel("Password:")
        layout.addWidget(self.label_password)
        self.input_password = QLineEdit(self)
        self.input_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.input_password)

        self.label_email = QLabel("Email:")
        layout.addWidget(self.label_email)
        self.input_email = QLineEdit(self)
        layout.addWidget(self.input_email)

        self.label_full_name = QLabel("Full Name:")
        layout.addWidget(self.label_full_name)
        self.input_full_name = QLineEdit(self)
        layout.addWidget(self.input_full_name)

        self.button_signup = QPushButton("Sign Up", self)
        self.button_signup.clicked.connect(self.signup)
        layout.addWidget(self.button_signup)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def signup(self):
        username = self.input_username.text()
        password = self.input_password.text()
        email = self.input_email.text()
        full_name = self.input_full_name.text()

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, email, full_name) VALUES (?, ?, ?, ?)", (username, password, email, full_name))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Sign Up", "User registered successfully!")
        self.close()


def test_password_reset():
    app = QApplication(sys.argv)
    reset_app = PasswordResetApp()
    reset_app.input_username.setText("testuser")
    reset_app.input_new_password.setText("newpassword123")
    reset_app.reset_password()
    print("Password reset test completed.")


class FeelApp(QMainWindow):
        
    def __init__(self):
        super().__init__()

        # Direct path to feelings.ui file inside the program.
        ui_file = os.path.join(os.path.dirname(__file__), "feelings.ui")
        
        # Ensure the UI file exists before loading
        if not os.path.exists(ui_file):
            QMessageBox.critical(self, "Error", f"UI file not found: {ui_file}")
            sys.exit(1)

        print(f"Loading UI from: {ui_file}")  # Debugging print statement
        uic.loadUi(ui_file, self)

    


        # Initialize UI and set up style
        #self.initUI()
        self.create_database()

        self.setStyleSheet("""
    
            QMainWindow {
                background-color: #D8BFD8; /* Light gray background */
                background-repeat: repeat;
                background-position: center;
            }
        
            QPushButton {
                background: none; /* Removes background */
                border: none; /* Removes border */
            }

            QPushButton::icon {
                width: 126px; /* Adjust icon size */
                height: 126px;
            }

            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333; /* Dark gray text */
                text-align: center;
            }
        """)

        # Connect emoji buttons to their functions
        self.setup_connections()

        # Define exercises for each emotion
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

    def setup_connections(self):
        """Connect buttons to the corresponding functions."""
        try:
            # Set emojis as icons for buttons using os.path.join to form the correct path
            self.btnHappy.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "images", "happy.png")))
            self.btnNeutral.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "images", "neutral.png")))
            self.btnSad.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "images", "sad.png")))
            self.btnRelaxed.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "images", "relaxed.png")))
            self.btnAnxious.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "images", "anxious.png")))
            self.btnStressed.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "images", "stressed.png")))

            # Optionally set the icon size
            self.btnHappy.setIconSize(QSize(126, 126))
            self.btnNeutral.setIconSize(QSize(126, 126))
            self.btnSad.setIconSize(QSize(126, 126))
            self.btnRelaxed.setIconSize(QSize(126, 126))
            self.btnAnxious.setIconSize(QSize(126, 126))
            self.btnStressed.setIconSize(QSize(126, 126))

            # Connect buttons to the respective methods
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
        """Switch to the exercise page and display the corresponding exercise."""
        self.textEdit.setText(self.exercises.get(emotion, "Please select an emotion."))
        self.stackedWidget.setCurrentIndex(1)  # Switch to exercise page

    def go_back(self):
        """Go back to the emotion selection page."""
        self.stackedWidget.setCurrentIndex(0)

    #def open_feelings(self):
        #self.feelings_window = FeelApp()
        #self.feelings_window.show()


    # connect interface to database...
    def create_database(self):
        """Create the database for FeelApp if necessary."""
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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginApp()
    window.show()
    sys.exit(app.exec_())
