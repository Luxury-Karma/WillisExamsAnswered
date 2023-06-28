import sys

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, \
    QTextEdit, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout


from module import WillisAnswered

Data = WillisAnswered.DataHandle()


class StartWidget(QWidget):
    switch_to_create_account_signal = pyqtSignal()
    switch_to_get_research_signal = pyqtSignal(str, int)
    switch_to_update_database_signal = pyqtSignal()  # new signal for update database

    def emit_switch_to_create_account_signal(self):
        self.switch_to_create_account_signal.emit()

    def emit_switch_to_update_database_signal(self):
        self.switch_to_update_database_signal.emit()  # new method to emit signal

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

        # Bring to the research page
        self.research_button = QPushButton('Research', self)
        layout.addWidget(self.research_button)
        self.research_button.clicked.connect(self.search_data)

        # Bring to the menu going trought all of willis college to collect data
        self.create_database_button = QPushButton('Create Database', self)
        layout.addWidget(self.create_database_button)

        # Bring to the other options to modify the data base
        self.update_database_button = QPushButton('Update Database', self)
        layout.addWidget(self.update_database_button)
        self.update_database_button.clicked.connect(self.emit_switch_to_update_database_signal)

        # Bring to create the account needed for the program to work
        self.AccountCreationButton = QPushButton('Input Loggins Credential', self)  # Add the back button
        layout.addWidget(self.AccountCreationButton)
        self.AccountCreationButton.clicked.connect(
            self.emit_switch_to_create_account_signal)  # Connect back button to emit the signal


class CreateDataBaseWidget(QWidget):
    switch_back_signal = pyqtSignal()

    def start_research_button_clicked(self):
        file_password = self.input_data.text()
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


class UpdateDatabaseWidget(QWidget):
    switch_back_signal = pyqtSignal()
    switch_to_manual_qa_signal = pyqtSignal()
    switch_to_json_file_signal = pyqtSignal()
    switch_to_review_link_signal = pyqtSignal()
    switch_to_course_link_signal = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create buttons for various update operations
        self.manual_qa_button = QPushButton('Manually give a question and answer', self)
        layout.addWidget(self.manual_qa_button)
        self.manual_qa_button.clicked.connect(self.switch_to_manual_qa_signal.emit)

        self.json_file_button = QPushButton('Give me a JSON file', self)
        layout.addWidget(self.json_file_button)
        self.json_file_button.clicked.connect(self.switch_to_json_file_signal.emit)

        self.review_link_button = QPushButton('Give me a link to a review', self)
        layout.addWidget(self.review_link_button)
        self.review_link_button.clicked.connect(self.switch_to_review_link_signal.emit)

        self.course_link_button = QPushButton('Give me a link to a course', self)
        layout.addWidget(self.course_link_button)
        self.course_link_button.clicked.connect(self.switch_to_course_link_signal.emit)

        # Create back button
        self.back_button = QPushButton('Back', self)
        layout.addWidget(self.back_button)
        self.back_button.clicked.connect(self.switch_back_signal.emit)


class ManualQAWidget(QWidget):
    switch_back_signal = pyqtSignal()

    def emit_switch_back_signal(self):
        self.switch_back_signal.emit()

    def send_data(self):
        self.answer_label.text()
        Data.manualy_add_question_answer(self.question_line.text(), self.answer_line.text(), self.course_type_line.text())

    def __init__(self, parent=None):
        super(ManualQAWidget, self).__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.url_label = QLabel('Enter the question : ', self)
        layout.addWidget(self.url_label)

        self.question_line = QLineEdit()
        layout.addWidget(self.question_line)

        self.answer_label = QLabel('Enter the answer : ', self)
        layout.addWidget(self.answer_label)  # Add the label to the layout
        self.answer_line = QLineEdit()
        layout.addWidget(self.answer_line)

        self.courtse_type_label = QLabel('Enter the course Type: ', self)
        layout.addWidget(self.courtse_type_label)  # Add the label to the layout
        self.course_type_line = QLineEdit()
        layout.addWidget(self.course_type_line)

        self.send_button = QPushButton('Send', self)
        layout.addWidget(self.send_button)
        self.send_button.clicked.connect(self.send_data)
        # Connect send button to some function

        self.back_button = QPushButton('Back', self)
        layout.addWidget(self.back_button)
        self.back_button.clicked.connect(self.emit_switch_back_signal)



class JsonFileWidget(QWidget):
    switch_back_signal = pyqtSignal()

    def emit_switch_back_signal(self):
        self.switch_back_signal.emit()

    def __init__(self, parent=None):
        super(JsonFileWidget, self).__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.url_label = QLabel('Enter The path to the json : ', self)
        layout.addWidget(self.url_label)
        self.file_path_line = QLineEdit()
        layout.addWidget(self.file_path_line)

        self.send_button = QPushButton('Send', self)
        layout.addWidget(self.send_button)
        # Connect send button to some function

        self.back_button = QPushButton('Back', self)
        layout.addWidget(self.back_button)
        self.back_button.clicked.connect(self.emit_switch_back_signal)


class ReviewLinkWidget(QWidget):
    switch_back_signal = pyqtSignal()

    def emit_switch_back_signal(self):
        self.switch_back_signal.emit()

    def __init__(self, parent=None):
        super(ReviewLinkWidget, self).__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.url_label = QLabel('Enter the link to the review :', self)
        layout.addWidget(self.url_label)
        self.url_line = QLineEdit()
        layout.addWidget(self.url_line)

        self.send_button = QPushButton('Send', self)
        layout.addWidget(self.send_button)
        # Connect send button to some function

        self.back_button = QPushButton('Back', self)
        layout.addWidget(self.back_button)
        self.back_button.clicked.connect(self.emit_switch_back_signal)


class CourseLinkWidget(QWidget):
    switch_back_signal = pyqtSignal()

    def emit_switch_back_signal(self):
        self.switch_back_signal.emit()

    def __init__(self, parent=None):
        super(CourseLinkWidget, self).__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.url_label = QLabel('URL of the course: ', self)

        self.url_line = QLineEdit()
        layout.addWidget(self.url_line)

        self.send_button = QPushButton('Send', self)
        layout.addWidget(self.send_button)
        # Connect send button to some function

        self.back_button = QPushButton('Back', self)
        layout.addWidget(self.back_button)
        self.back_button.clicked.connect(self.emit_switch_back_signal)


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
        self.Answer = Data.get_question_from_prompt(self.words)

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
        self.Answer = Data.get_question_from_prompt(self.words)
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
        self.start_widget.switch_to_update_database_signal.connect(self.switch_to_update_database_widget)

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

    def init_manual_qa_widget(self):
        self.manual_qa_widget = ManualQAWidget(self)
        self.manual_qa_widget.switch_back_signal.connect(self.switch_to_update_database_widget)

    def init_json_file_widget(self):
        self.json_file_widget = JsonFileWidget(self)
        self.json_file_widget.switch_back_signal.connect(self.switch_to_update_database_widget)

    def init_review_link_widget(self):
        self.review_link_widget = ReviewLinkWidget(self)
        self.review_link_widget.switch_back_signal.connect(self.switch_to_update_database_widget)

    def init_course_link_widget(self):
        self.course_link_widget = CourseLinkWidget(self)
        self.course_link_widget.switch_back_signal.connect(self.switch_to_update_database_widget)

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

    def init_update_database_widget(self):
        self.update_database_widget = UpdateDatabaseWidget(self)

        # Connect back signal
        self.update_database_widget.switch_back_signal.connect(self.switch_to_start_widget)

        # Connect signals to switch to other widgets
        self.update_database_widget.switch_to_manual_qa_signal.connect(self.switch_to_manual_qa_widget)
        self.update_database_widget.switch_to_json_file_signal.connect(self.switch_to_json_file_widget)
        self.update_database_widget.switch_to_review_link_signal.connect(self.switch_to_review_link_widget)
        self.update_database_widget.switch_to_course_link_signal.connect(self.switch_to_course_link_widget)

        self.setCentralWidget(self.update_database_widget)

    def switch_to_update_database_widget(self):
        self.init_update_database_widget()

    def switch_to_manual_qa_widget(self):
        self.init_manual_qa_widget()
        self.setCentralWidget(self.manual_qa_widget)

    def switch_to_json_file_widget(self):
        self.init_json_file_widget()
        self.setCentralWidget(self.json_file_widget)

    def switch_to_review_link_widget(self):
        self.init_review_link_widget()
        self.setCentralWidget(self.review_link_widget)

    def switch_to_course_link_widget(self):
        self.init_course_link_widget()
        self.setCentralWidget(self.course_link_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
