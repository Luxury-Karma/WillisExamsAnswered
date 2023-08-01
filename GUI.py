import sys

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, \
    QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QRadioButton, QFileDialog, QHBoxLayout

from module import WillisAnswered

Data = WillisAnswered.DataHandle()  # The object use to interact with the program

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

    for e in set_up_list:
        temp_layout = QHBoxLayout()
        temp_layout.addWidget(e[1])
        temp_layout.addWidget(e[0])
        layout.addLayout(temp_layout)
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
    add_quiz_button = QPushButton('Add a quiz review')
    add_question_button = QPushButton('Add manual question')
    

    return layout

def add_review_quiz_widget() -> QVBoxLayout:
    """
    The menu to send the program at a specific link to get the questions and answer
    :return:
    """
    layout: QVBoxLayout = QVBoxLayout()
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
    window.setLayout(user_creation_widget())
    window.show()
    sys.exit(app.exec())
