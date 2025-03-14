import sys
import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication
from log import FeelApp  


class TestFeelApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the QApplication for testing."""
        cls.app = QApplication(sys.argv)

    def setUp(self):
        """This method will be run before each test."""
        self.feel_app = FeelApp() 
        self.feel_app.setup_connections()  

    def test_setup_connections(self):
        """Test if buttons are connected correctly."""
        self.feel_app.btnHappy.clicked = MagicMock()
        self.feel_app.btnNeutral.clicked = MagicMock()
        self.feel_app.btnSad.clicked = MagicMock()
        self.feel_app.btnRelaxed.clicked = MagicMock()
        self.feel_app.btnAnxious.clicked = MagicMock()
        self.feel_app.btnStressed.clicked = MagicMock()

        self.feel_app.setup_connections()
        self.feel_app.btnHappy.clicked.connect.assert_called_once()
        self.feel_app.btnNeutral.clicked.connect.assert_called_once()
        self.feel_app.btnSad.clicked.connect.assert_called_once()
        self.feel_app.btnRelaxed.clicked.connect.assert_called_once()
        self.feel_app.btnAnxious.clicked.connect.assert_called_once()
        self.feel_app.btnStressed.clicked.connect.assert_called_once()

    def test_show_exercise(self):
        """Test if the exercise for a given emotion is shown correctly."""
        emotion = "Happy"
        self.feel_app.show_exercise(emotion)
        expected_exercise = self.feel_app.exercises[emotion]
        self.assertEqual(self.feel_app.textEdit.toPlainText(), expected_exercise)

    def test_go_back(self):
        """Test if the 'go_back' method works properly by switching to the correct page."""
        self.feel_app.stackedWidget.setCurrentIndex(1)
        self.feel_app.go_back()
        self.assertEqual(self.feel_app.stackedWidget.currentIndex(), 0)
@patch('sqlite3.connect')
def test_create_database(self, mock_connect):
    """Test if the database is created successfully."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mock_connect.return_value = mock_conn

    self.feel_app.create_database()

    mock_cursor.execute.assert_any_call(
        "CREATE TABLE IF NOT EXISTS feelings ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "emotion TEXT NOT NULL, "
        "exercise TEXT NOT NULL)"
    )

    @patch('sqlite3.connect')
    def test_create_database(self, mock_connect):
        """Test if the database is created successfully."""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        self.feel_app.create_database()

        mock_conn.cursor.return_value.execute.assert_any_call(
            "CREATE TABLE IF NOT EXISTS feelings (" 
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "emotion TEXT NOT NULL, "
            "exercise TEXT NOT NULL)"
        )

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests are finished."""
        cls.app.quit() 


if __name__ == '__main__':
    unittest.main()
