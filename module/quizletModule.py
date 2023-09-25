import re
import time
import urllib
from typing import List, Any
from urllib.parse import urlparse
from module import user_handeling
from bs4 import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class quizlet_talker:
    def __init__(self, quizlet_website: str = None, browser: str = None):
        self.website = quizlet_website if quizlet_website else 'https://quizlet.com/latest'
        self.is_browser = False
        self._drive:webdriver = None
        self._browser = browser if browser else 'firefox'
    def _need_browser(self):
        if self.is_browser:
            return
        try:
            if self._browser == 'google':
                self._drive = webdriver.Chrome()
            elif self._browser == 'firefox':
                self._drive = webdriver.Firefox()
            elif self._browser == 'safari':
                self._drive = webdriver.Safari()
            self.is_browser = True
        except:
            self._drive = webdriver.Firefox()

    def set_link(self, new_link: str):
        self.website = new_link

    def go_to_quiz(self):
        """
        Go to the quizlet website
        :return:
        """
        self._need_browser()

        self._drive.get(self.website)

    def get_question_answer(self) -> dict:
        try:
            WebDriverWait(self._drive, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'SetPageTerm-content')))
            soup = BeautifulSoup(self._drive.page_source, 'html.parser')
            question_divs = soup.find_all('div', class_='SetPageTerm-content')
            question_dict = {}

            for question_div in question_divs:
                question_elem = question_div.find('a', class_='SetPageTerm-wordText')
                answer_elem = question_div.find('a', class_='SetPageTerm-definitionText')

                if question_elem and answer_elem:
                    question_text = question_elem.find('span', class_='TermText notranslate lang-en').text
                    answer_text = answer_elem.find('span', class_='TermText notranslate lang-en').text

                    question_dict[question_text] = answer_text

            return question_dict

        except Exception as e:
            print('An error occurred:', str(e))

    def quizlet_communication_question_answer(self) -> dict:
        self._need_browser()
        self.go_to_quiz()
        return self.get_question_answer()

    def close_quizlet_driver(self):
        self.is_browser = False
        self._drive.close()

if __name__ == '__main__':
    quiz = quizlet_talker(quizlet_website='https://quizlet.com/119231974/fortinet-nse-4-flash-cards/')
    quiz._need_browser()
    quiz.go_to_quiz()
    quiz.get_question_answer()