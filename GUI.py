import sys

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, \
    QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QRadioButton, QFileDialog, QHBoxLayout

from module import WillisAnswered

Data = WillisAnswered.DataHandle()  # The object use to interact with the program

#region General Graphical Function

def basic_side_layout(set_up_list:list[list]) -> QVBoxLayout:
    layout: QVBoxLayout = QVBoxLayout()
    for e in set_up_list:
        temp_layout = QHBoxLayout()
        temp_layout.addWidget(e[1])
        temp_layout.addWidget(e[0])
        layout.addLayout(temp_layout)
    return layout

#endregion


#region user config
def user_creation_widget() -> QVBoxLayout:
    """
    The widget that the user will use to input is connection and the password for the file
    :return:
    """
    layout: QVBoxLayout = QVBoxLayout()
    # Variables
    user_line = QLineEdit()
    user_password_line = QLineEdit()
    user_file_password = QLineEdit()
    user_line.setPlaceholderText('Jhon.Smith@students.williscollege.com')
    user_password_line.setPlaceholderText('Pa55W.rd')
    user_file_password.setPlaceholderText('Pa55W.rd')
    user_line_text = QLabel()
    user_password_text = QLabel()
    user_file_text = QLabel()
    user_line_text.setText('Enter Willis email: ')
    user_password_text.setText('Enter Willis email\'s password: ')
    user_file_text.setText('This file password: ')
    save_button = QPushButton()
    save_button.setText('Save')
    back_button = QPushButton()
    back_button.setText('Back')
    # How to set them up
    set_up_list = [[user_line,user_line_text], [user_password_line,user_password_text],
                   [user_file_password,user_file_text]]
    # set them up
    layout.addLayout(basic_side_layout(set_up_list))

    layout.addWidget(save_button)
    layout.addWidget(back_button)
    return layout



#endregion


#region setting

def user_setting_widget() -> QVBoxLayout:
    """
    The menu to decide the option to add data inside the database
    :return:
    """
    layout: QVBoxLayout = QVBoxLayout()
    save_button = QPushButton('Save')
    back_button = QPushButton('Back')
    radio_text = QLabel()
    radio_text.setText('Choose the browser to use: ')
    google_radio_button = QRadioButton('Google')
    firefox_radio_button = QRadioButton('Firefox')
    safari_radio_button = QRadioButton('Safari')
    edge_radio_button = QRadioButton('Edge')
    layout.addWidget(radio_text)
    layout.addWidget(google_radio_button)
    layout.addWidget(firefox_radio_button)
    layout.addWidget(safari_radio_button)
    layout.addWidget(edge_radio_button)
    layout.addWidget(save_button)
    layout.addWidget(back_button)
    return layout

#endregion


#region add questions

def add_question_menu_widget() -> QVBoxLayout:
    """
    The menu to decide how to send data to the program
    :return:
    """
    layout: QVBoxLayout = QVBoxLayout()
    add_back_button = QPushButton('Back')
    add_quiz_button = QPushButton('Add a quiz review')
    add_question_button = QPushButton('Add manual question')
    add_course_button = QPushButton('Add course reviews')
    create_data_base_button = QPushButton('Create Database')
    layout.addWidget(add_quiz_button)
    layout.addWidget(add_question_button)
    layout.addWidget(add_course_button)
    layout.addWidget(create_data_base_button)
    layout.addWidget(add_back_button)

    return layout

def add_review_quiz_widget(label:str, placeHolder:str, typeSearch: str) -> QVBoxLayout:
    """
    Menue built for any link to get info to
    :return: The layout of the page
    """
    layout: QVBoxLayout = QVBoxLayout()
    add_url_text = QLabel()
    add_url_text.setText(f'{label}')
    add_url = QLineEdit()
    add_url.setPlaceholderText(f'{placeHolder}')
    add_send_button = QPushButton('Send')
    hlayout = QHBoxLayout()
    hlayout.addWidget(add_url_text)
    hlayout.addWidget(add_url)
    layout.addLayout(hlayout)
    layout.addWidget(add_send_button)
    return layout

def add_course_quiz_widget() -> QVBoxLayout:
    """
    The menu for a user to send at a course webpage to get all the quizs
    :return: 
    """
    layout: QVBoxLayout = QVBoxLayout()

    return layout

def add_manual_question_widget() -> QVBoxLayout:
    """
    The menu to manualy add a question to the database
    :return:
    """
    layout: QVBoxLayout = QVBoxLayout()

    add_question_text = QLabel()
    add_question_text.setText('Enter question to create: ')

    add_question_line = QLineEdit()
    add_question_line.setPlaceholderText('What is a cisco machine?')

    add_answer_text = QLabel()
    add_answer_text.setText('Enter the answer to the question: ')

    add_answer_line = QLineEdit()
    add_answer_line.setPlaceholderText('It is a network machine')

    add_course_text = QLabel()
    add_course_text.setText('Which course it is link to: ')

    add_course_line = QLineEdit()
    add_course_line.setPlaceholderText('CCNA')

    side_layout = [[add_question_line,add_question_text],[add_answer_line,add_answer_text],
                   [add_course_line,add_course_text]]
    layout.addLayout(basic_side_layout(side_layout))

    return layout

def create_data_base_widget() -> QVBoxLayout:
    """
    The initial launch. Should go in the willis college website and read all it can see to get quizs
    :return:
    """
    layout: QVBoxLayout = QVBoxLayout()
    return layout

#endregion


#region get question

def get_question_answer_widget() -> QVBoxLayout:
    """
    The menu for the user to research data in the database
    :return:
    """
    layout: QVBoxLayout = QVBoxLayout()
    return layout

#endregion


    # endregion

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('Willis College Student Database')
    window.setLayout(add_manual_question_widget())
    window.show()
    sys.exit(app.exec())
