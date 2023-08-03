import sys

from PyQt5.QtCore import pyqtSignal, Qt, pyqtBoundSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, \
    QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QRadioButton, QFileDialog, QHBoxLayout
import PyQt5.QtWidgets

from module import WillisAnswered

Data = WillisAnswered.DataHandle()  # The object use to interact with the program

#region General Graphical Function
__app = QApplication(sys.argv)
__window = QWidget()
__window.show()
def basic_side_layout(set_up_list:list[list]) -> QVBoxLayout:
    layout: QVBoxLayout = QVBoxLayout()
    for e in set_up_list:
        temp_layout = QHBoxLayout()
        temp_layout.addWidget(e[1])
        temp_layout.addWidget(e[0])
        layout.addLayout(temp_layout)
    return layout

def moving_widget(moving_widget:str) -> None:
    global __window

    moving_widget = moving_widget.lower()

    __window.setWindowTitle('Willis College Student Database')

    if moving_widget == 'database':
        __window.setLayout(add_question_menu_widget())
    elif moving_widget == 'setting':
        __window.setLayout(setting_menu_widget())
    elif moving_widget == 'main':
        __window.setLayout(mainMenue())
    elif moving_widget == 'getquestion':
        __window.setLayout(get_question_answer_widget())
    elif moving_widget == 'usersetting':
        __window.setLayout(user_setting_widget())
    elif moving_widget == 'usercreation':
        __window.setLayout(user_creation_widget())
    else:
        print('ERROR: The button do not bring anywhere')
    __window.update()


#endregion




#region setting

def setting_menu_widget() -> QVBoxLayout:
    layout: QVBoxLayout = QVBoxLayout()
    return layout

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

    # Give functionalities


    #Visual setup
    layout.addWidget(save_button)
    layout.addWidget(back_button)
    return layout


#endregion


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

    add_send_button = QPushButton('Send')
    side_layout = [[add_question_line,add_question_text],[add_answer_line,add_answer_text],
                   [add_course_line,add_course_text]]
    layout.addLayout(basic_side_layout(side_layout))

    layout.addWidget(add_send_button)

    return layout


#endregion


#region get question

def get_question_answer_widget(amount_of_return: int = 100) -> QVBoxLayout:
    """
    The menu for the user to research data in the database
    :return:
    """
    test = ['Question', 'Answer', 'Course']

    # Creating board
    layout: QVBoxLayout = QVBoxLayout()
    Hlayout: QHBoxLayout = QHBoxLayout()
    add_research_text = QLabel()
    add_research_text.setText('Enter your research: ')
    add_research_line = QLineEdit()
    add_research_line.setPlaceholderText('Cisco switch data')
    add_back_button = QPushButton('Back')


    grid_layout = QTableWidget()
    grid_layout.setRowCount(amount_of_return)
    grid_layout.setColumnCount(3)
    grid_layout.setHorizontalHeaderLabels(test)

    layout.addLayout(basic_side_layout([[add_research_line,add_research_text]]))
    layout.addWidget(grid_layout)





    return layout

#endregion


#region Main menu
def mainMenue():
    layout: QVBoxLayout = QVBoxLayout()

    add_information_text =QLabel()
    add_information_text.setText('Keep in mind: \nTo use database functions you need to add your credential in the setting menu')
    add_research_button = QPushButton('Research')
    add_addQuestion_button = QPushButton('Add to database')
    add_setting_button = QPushButton('Setting')

    add_research_button.clicked.connect(lambda: moving_widget('getquestion'))
    add_addQuestion_button.clicked.connect(lambda: moving_widget('database'))
    add_setting_button.clicked.connect(lambda: moving_widget('setting'))


    layout.addWidget(add_information_text)
    layout.addWidget(add_research_button)
    layout.addWidget(add_addQuestion_button)
    layout.addWidget(add_setting_button)

    return layout
#end region

    # endregion

if __name__ == '__main__':
    moving_widget('main')
    sys.exit(__app.exec())
