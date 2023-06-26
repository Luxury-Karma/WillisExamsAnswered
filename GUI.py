import sys

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, \
    QTextEdit, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout


from module import WillisAnswered

Data = WillisAnswered.DataHandle()


class StartWidget(QWidget):
    switch_to_create_account_signal = pyqtSignal()
    switch_to_get_research_signal = pyqtSignal(str, int)

    def emit_switch_to_create_account_signal(self):
        self.switch_to_create_account_signal.emit()

    def search_data(self):
        word_search = self.word_input.text()
        try:
            amount = int(self.number_input.text())
        except Exception as e:
            print(f'Not a number setting default amount : {e}')
            amount = 100
        self.switch_to_get_research_signal.emit(word_search, amount)

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
        self.research_button.clicked.connect(self.search_data)

        self.create_database_button = QPushButton('Create Database', self)
        layout.addWidget(self.create_database_button)

        self.AccountCreationButton = QPushButton('Input Loggins Credential', self)  # Add the back button
        layout.addWidget(self.AccountCreationButton)
        self.AccountCreationButton.clicked.connect(
            self.emit_switch_to_create_account_signal)  # Connect back button to emit the signal


class CreateDataBaseWidget(QWidget):
    switch_back_signal = pyqtSignal()

    def start_research_button_clicked(self):
        file_password = self.input_data.toPlainText()
        Data.global_quiz_data_collecting(file_password)

    def __init__(self, parent):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.input_label = QLabel('Password Of the password File:', self)
        layout.addWidget(self.input_label)

        self.input_data = QLineEdit(self)
        self.input_data.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.input_data)

        self.start_research_button = QPushButton('START', self)
        layout.addWidget(self.start_research_button)
        self.start_research_button.clicked.connect(self.start_research_button_clicked)

        self.back_button = QPushButton('Back', self)
        layout.addWidget(self.back_button)
        self.back_button.clicked.connect(self.emit_switch_back_signal)

    def emit_switch_back_signal(self):
        self.switch_back_signal.emit()


class CreateAccountBaseWidget(QWidget):
    switch_back_signal = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.account_input_label = QLabel('Willis College account:', self)
        layout.addWidget(self.account_input_label)

        self.account_input_data = QLineEdit(self)
        layout.addWidget(self.account_input_data)

        self.account_password_input_label = QLabel('Willis College password :', self)
        layout.addWidget(self.account_password_input_label)

        self.account_password_input_data = QLineEdit(self)
        self.account_password_input_data.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.account_password_input_data)

        self.file_password_input_label = QLabel('password to encrypt the file :', self)
        layout.addWidget(self.file_password_input_label)

        self.file_password_input_data = QLineEdit(self)
        self.file_password_input_data.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.file_password_input_data)


        self.create_account_button = QPushButton('Send', self)
        layout.addWidget(self.create_account_button)
        self.create_account_button.clicked.connect(self.create_account)

        self.back_button = QPushButton('Back', self)
        layout.addWidget(self.back_button)
        self.back_button.clicked.connect(self.emit_switch_back_signal)

    def emit_switch_back_signal(self):
        self.switch_back_signal.emit()

    def create_account(self):
        user = self.account_input_data.text()
        password = self.account_password_input_data.text()
        filepassword = self.file_password_input_data.text()
        Data.willis_user_creation(user, password, filepassword)
        self.switch_back_signal.emit()


class ResearchWidget(QWidget):
    switch_back_signal = pyqtSignal()

    def emit_switch_back_signal(self):
        self.switch_back_signal.emit()

    def __init__(self, parent, words: str, amount: int):
        super().__init__(parent)
        self.words = words
        self.amount = amount
        self.Answer = []
        self.Answer = Data.getQuestionFromPrompt(self.words)

        self.researchWord_label = QLabel(f'Regex search: {Data.regex}', self)

        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(['Question', 'Answer'])
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.setTextElideMode(Qt.ElideNone)  # Disable text elision
        self.table_widget.setWordWrap(True)  # Enable text wrapping for the cells

        layout = QVBoxLayout(self)
        self.back_button = QPushButton('Back', self)
        layout.addWidget(self.back_button)
        self.back_button.clicked.connect(self.emit_switch_back_signal)

        self.new_search_line_edit = QLineEdit(self)  # Add the line edit
        layout.addWidget(self.new_search_line_edit)

        self.new_search_button = QPushButton('New Search', self)  # Add the button
        layout.addWidget(self.new_search_button)

        layout.addWidget(self.researchWord_label)
        layout.addWidget(self.table_widget)

        # Connect the button click and line edit returnPressed signal to a new slot
        self.new_search_button.clicked.connect(self.start_new_search)
        self.new_search_line_edit.returnPressed.connect(self.start_new_search)

        self.populate_table()  # Populate the table with data

    def start_new_search(self):
        # Slot to start a new search
        self.words = self.new_search_line_edit.text()
        self.Answer = Data.getQuestionFromPrompt(self.words)
        self.researchWord_label.setText(f'Regex search: {Data.regex}')
        self.populate_table()

    def populate_table(self):
        valid_rows = [(question, _) for question, _ in self.Answer if
                      Data.find_answer_by_question(question)['answer'] and 'No Data' not in
                      Data.find_answer_by_question(question)['answer']]
        row_count = self.amount  # Set the row count to the specified amount
        self.table_widget.setRowCount(row_count)
        active_answer = 0
        row_number = 0  # Track the current row number
        for row, (question, _) in enumerate(valid_rows):
            if active_answer >= self.amount:
                break
            question_item = QTableWidgetItem(question)
            answer = Data.find_answer_by_question(question)['answer']
            strAnswer: str = ''
            for e in answer:
                e = e.replace("\n", " ")
                strAnswer = strAnswer + f'{e}\n'
            question_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            answer_item = QTableWidgetItem(strAnswer)
            answer_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table_widget.setItem(row_number, 0, question_item)
            self.table_widget.setItem(row_number, 1, answer_item)
            active_answer += 1
            row_number += 1  # Increment the row number
        self.table_widget.resizeRowsToContents()  # Adjust row heights to fit content

    def resizeEvent(self, event):
        super().resizeEvent(event)

        table_width = self.width()
        column_0_width = table_width // 2
        self.table_widget.setColumnWidth(0, column_0_width)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Willis Student Question Answer Database')
        self.setGeometry(100, 100, 300, 300)

        self.init_start_widget()

    def init_start_widget(self):
        self.start_widget = StartWidget(self)

        # Connect signals from start widget
        self.start_widget.create_database_button.clicked.connect(self.switch_to_create_widget)
        self.start_widget.switch_to_get_research_signal.connect(self.switch_to_research_widget)
        self.start_widget.switch_to_create_account_signal.connect(self.switch_to_user_creation)

        self.setCentralWidget(self.start_widget)

    def init_create_database_widget(self):
        self.create_database_widget = CreateDataBaseWidget(self)

        # Connect back signals from other widgets
        self.create_database_widget.switch_back_signal.connect(self.switch_to_start_widget)

        self.setCentralWidget(self.create_database_widget)

    def init_create_account_widget(self):
        self.create_account_widget = CreateAccountBaseWidget(self)

        # Connect back signals from other widgets
        self.create_account_widget.switch_back_signal.connect(self.switch_to_start_widget)

        self.setCentralWidget(self.create_account_widget)

    def switch_to_create_widget(self):
        self.init_create_database_widget()

    def switch_to_start_widget(self):
        self.init_start_widget()
        self.resize(300, 300)  # Restore original window size

    def switch_to_research_widget(self, words_search: str, question_amount: int):
        self.research_widget = ResearchWidget(self, words_search, question_amount)
        self.research_widget.switch_back_signal.connect(self.switch_to_start_widget)  # Connect back signal
        self.resize(800, 600)
        self.setCentralWidget(self.research_widget)

    def switch_to_user_creation(self):
        self.init_create_account_widget()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
