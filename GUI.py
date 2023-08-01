import sys

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, \
     QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QRadioButton,QFileDialog


from module import WillisAnswered

Data = WillisAnswered.DataHandle()

#region user config
def user_creation_widget():
    """
    The widget that the user will use to input is connection and the password for the file
    :return:
    """
    pass

#endregion


#region setting

def user_setting_widget():
    """
    The menu to decide the option to add data inside the database
    :return:
    """
    pass

#endregion


#region add questions

def add_question_menu_widget():
    """
    The menu to decide how to send data to the program
    :return:
    """
    pass

def add_review_quiz_widget():
    """
    The menu to send the program at a specific link to get the questions and answer
    :return:
    """
    pass

def add_course_quiz_widget():
    """
    The menu for a user to send at a course webpage to get all the quizs
    :return: 
    """
    pass

def add_manual_question_widget():
    """
    The menu to manualy add a question to the database
    :return:
    """
    pass

def create_data_base_widget():
    """
    The initial launch. Should go in the willis college website and read all it can see to get quizs
    :return:
    """
    pass

#endregion


#region get question

def get_question_answer_widget():
    """
    The menu for the user to research data in the database
    :return:
    """
    pass

#endregion


    # endregion

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    #window =
    #window.show()
    sys.exit(app.exec())
