from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLineEdit, QTableWidget, \
    QTableWidgetItem, QStackedWidget


class ResearchDatabase(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.init_ui()

    def init_ui(self):
        # Add your UI elements here
        self.layout = QVBoxLayout(self)

        self.input_line = QLineEdit(self)
        self.layout.addWidget(self.input_line)

        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)

        self.send_button = QPushButton('Send', self)
        self.layout.addWidget(self.send_button)

        self.back_button = QPushButton('Back', self)
        self.layout.addWidget(self.back_button)
        self.back_button.clicked.connect(self.main_window.show_main_menu)

        self.setLayout(self.layout)


class AddQuestion(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.init_ui()

    def init_ui(self):
        # Add your UI elements here
        self.layout = QVBoxLayout(self)

        self.manual_question_button = QPushButton('Manual Question', self)
        self.layout.addWidget(self.manual_question_button)

        self.review_button = QPushButton('Review', self)
        self.layout.addWidget(self.review_button)

        self.add_course_review_button = QPushButton('Add Course Review', self)
        self.layout.addWidget(self.add_course_review_button)

        self.generate_database_button = QPushButton('Generate Database', self)
        self.layout.addWidget(self.generate_database_button)

        self.back_button = QPushButton('Back', self)
        self.layout.addWidget(self.back_button)
        self.back_button.clicked.connect(self.main_window.show_main_menu)

        self.setLayout(self.layout)


class Settings(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.init_ui()

    def init_ui(self):
        # Add your UI elements here
        self.layout = QVBoxLayout(self)

        self.settings_button = QPushButton('Setting', self)
        self.layout.addWidget(self.settings_button)

        self.user_config_button = QPushButton('User Config', self)
        self.layout.addWidget(self.user_config_button)

        self.back_button = QPushButton('Back', self)
        self.layout.addWidget(self.back_button)
        self.back_button.clicked.connect(self.main_window.show_main_menu)

        self.setLayout(self.layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stacked_widget = QStackedWidget()

        self.research_database = ResearchDatabase(self)
        self.add_question = AddQuestion(self)
        self.settings = Settings(self)

        self.stacked_widget.addWidget(self.research_database)
        self.stacked_widget.addWidget(self.add_question)
        self.stacked_widget.addWidget(self.settings)

        self.init_ui()

    def init_ui(self):
        # Add your UI elements here
        self.layout = QVBoxLayout(self)

        self.research_database_button = QPushButton('Research Database', self)
        self.add_question_button = QPushButton('Add Question', self)
        self.settings_button = QPushButton('Settings', self)


        self.layout.addWidget(self.research_database_button)
        self.layout.addWidget(self.add_question_button)
        self.layout.addWidget(self.settings_button)

        self.research_database_button.clicked.connect(self.show_research_database)
        self.add_question_button.clicked.connect(self.show_add_question)
        self.settings_button.clicked.connect(self.show_settings)

        self.main_menu = QWidget()
        self.main_menu.setLayout(self.layout)
        self.stacked_widget.addWidget(self.main_menu)

        self.setCentralWidget(self.stacked_widget)
        self.show_main_menu()

    def show_research_database(self):
        self.stacked_widget.setCurrentWidget(self.research_database)

    def show_add_question(self):
        self.stacked_widget.setCurrentWidget(self.add_question)

    def show_settings(self):
        self.stacked_widget.setCurrentWidget(self.settings)

    def show_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
