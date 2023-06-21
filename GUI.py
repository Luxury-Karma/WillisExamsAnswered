import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QWidget, QVBoxLayout
from module import WillisAnswered

Data = WillisAnswered.DataHandle()

class StartWidget(QWidget):
    switch_to_create_account_signal = pyqtSignal()

    def emit_switch_to_create_account_signal(self):
        self.switch_to_create_account_signal.emit()

    def __init__(self, parent):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.word_label = QLabel('Word:', self)
        layout.addWidget(self.word_label)

        self.word_input = QLineEdit(self)
        layout.addWidget(self.word_input)

        self.number_label = QLabel('Number:', self)
        layout.addWidget(self.number_label)

        self.number_input = QLineEdit(self)
        layout.addWidget(self.number_input)

        self.research_button = QPushButton('Research', self)
        layout.addWidget(self.research_button)

        self.create_database_button = QPushButton('Create Database', self)
        layout.addWidget(self.create_database_button)

        self.Create_account_button = QPushButton('Create Account', self)
        layout.addWidget(self.Create_account_button)
        self.Create_account_button.clicked.connect(self.emit_switch_to_create_account_signal)

class CreateDataBaseWidget(QWidget):  # Create a new widget
    def start_research_button_clicked(self):
        file_password = self.input_data.toPlainText()
        Data.global_quiz_data_collecting(file_password)

    def __init__(self, parent):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.input_label = QLabel('Password Of the password File:', self)
        layout.addWidget(self.input_label)

        self.input_data = QTextEdit(self)
        layout.addWidget(self.input_data)

        self.start_research_button = QPushButton('START', self)
        layout.addWidget(self.start_research_button)
        self.start_research_button.clicked.connect(self.start_research_button_clicked)


        self.back_button = QPushButton('Back', self)
        layout.addWidget(self.back_button)





class CreateAccountBaseWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.account_input_label = QLabel('Willis College account:', self)  # Get the account
        layout.addWidget(self.account_input_label)

        self.account_input_data = QTextEdit(self)  # Get the username
        layout.addWidget(self.account_input_data)

        self.account_password_input_label = QLabel('Willis College password :', self)
        layout.addWidget(self.account_password_input_label)

        self.account_password_input_data = QTextEdit(self)  # Get the password
        layout.addWidget(self.account_password_input_data)

        self.file_password_input_label = QLabel('password to encrypt the file :', self)
        layout.addWidget(self.file_password_input_label)

        self.file_password_input_data = QTextEdit(self)  # Get the password
        layout.addWidget(self.file_password_input_data)

        self.create_account_button = QPushButton('Send', self)
        layout.addWidget(self.create_account_button)
        self.create_account_button.clicked.connect(self.create_account)

    def create_account(self):
        user = self.account_input_data.toPlainText()
        password = self.account_password_input_data.toPlainText()
        filepassword = self.file_password_input_data.toPlainText()
        Data.willis_user_creation(user, password, filepassword)





class ResearchWidget(QWidget):  # When we press the Research Button coming here
    def __init__(self, parent):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.researchWord_label = QLabel('Regex search:', self)
        layout.addWidget(self.researchWord_label)

        self.researchedWord_area = QTextEdit(self)
        layout.addWidget(self.researchedWord_area)

        self.back_button = QPushButton('Back', self)
        layout.addWidget(self.back_button)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Willis Student Question Answer Database')
        self.setGeometry(100, 100, 300, 300)

        self.start_widget = StartWidget(self)
        self.research_widget = ResearchWidget(self)
        self.create_database_widget = CreateDataBaseWidget(self)
        self.create_account_widget = CreateAccountBaseWidget(self)

        self.setCentralWidget(self.start_widget)

        self.start_widget.create_database_button.clicked.connect(self.switch_to_create_widget)
        self.create_database_widget.back_button.clicked.connect(self.switch_to_start_widget)
        self.start_widget.research_button.clicked.connect(self.switch_to_research_widget)
        self.research_widget.back_button.clicked.connect(self.switch_to_start_widget)
        self.start_widget.switch_to_create_account_signal.connect(self.switch_to_user_creation)

    def switch_to_create_widget(self):
        self.setCentralWidget(self.create_database_widget)

    def switch_to_start_widget(self):
        self.setCentralWidget(self.start_widget)

    def switch_to_research_widget(self):
        self.setCentralWidget(self.research_widget)

    def switch_to_user_creation(self):
        self.setCentralWidget(self.create_account_widget)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
