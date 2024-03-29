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


class WILLHANDLE:
    def __init__(self, WILLIS_WEB_SITE=None, QUIZ_DETECTION_REGEX=None, driv: webdriver = None, browser: str = None):
        self.__QUIZ_DETECTION_REGEX = QUIZ_DETECTION_REGEX if QUIZ_DETECTION_REGEX else r'^https:\/\/students\.willisonline\.ca\/mod\/quiz\/.*$'
        self.__WILLIS_WEB_SITE = WILLIS_WEB_SITE if WILLIS_WEB_SITE else "https://willisonline.ca/login"
        self._driv: webdriver = driv
        self._got_connection_to_willis: bool = False
        browser = browser if browser else user_handeling.get_user_setting()
        self._browser = browser if browser else 'firefox'

    def _needDriver(self):
        if self._driv:
            pass
        else:
            try:
                if self._browser == 'google':
                    self._driv = webdriver.Chrome()
                elif self._browser == 'firefox':
                    self._driv = webdriver.Firefox()
                elif self._browser == 'safari':
                    self._driv = webdriver.Safari()
            except:
                self._driv = webdriver.Firefox()

    # region connect to the website
    def __microsoft_connection(self, username: str, password: str) -> None:
        """
        Connnect with the Microsoft connection
        :param username: Microsoft Email
        :param password: Microsoft email's password
        :return: None
        """
        try:
            WebDriverWait(self._driv, 10).until(EC.presence_of_element_located((By.NAME, 'loginfmt')))
            input_field = self._driv.find_element(By.NAME, 'loginfmt')
            input_field.send_keys(username)
            input_field.send_keys(Keys.ENTER)

            WebDriverWait(self._driv, 15).until(EC.visibility_of_element_located((By.NAME, 'passwd')))
            input_field = self._driv.find_element(By.NAME, 'passwd')
            input_field.send_keys(password)

            click_specific_btn(self._driv, 'id="idSIButton9"', 'input')

            WebDriverWait(self._driv, 15).until(EC.element_to_be_clickable((By.ID, 'idBtn_Back')))
            self._driv.find_element(By.ID, 'idBtn_Back').click()

        except Exception as e:
            print("An error occurred: ", e)

    def __willis_college_connection(self, willis_username: str, willis_password: str) -> None:
        """
        Connect to willis college homepage
        :param willis_username: The Willis student email address to connect
        :param willis_password: The willis student email's password to connect
        :return: None
        """
        self._driv.get(self.__WILLIS_WEB_SITE)

        try:
            WebDriverWait(self._driv, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'img[alt="Sign in with Microsoft"]'))
            )
        except Exception as e:
            print("An error occurred: ", e)
        else:
            link = WebDriverWait(self._driv, 10).until(
                EC.presence_of_element_located((By.XPATH, '//img[@alt="Sign in with Microsoft"]/..'))
            )
            link.click()
            self.__microsoft_connection(willis_username, willis_password)

    def __willis_to_moodle(self) -> str:
        """
        Pass from the willis website to the willis moodle
        :return: the current URL
        """
        try:
            #time.sleep(5)

            WebDriverWait(self._driv, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Moodle')))
            time.sleep(2)
            self._driv.find_element(By.LINK_TEXT, 'Moodle').click()
            time.sleep(2)
            self._driv.switch_to.window(self._driv.window_handles[-1])
            self._got_connection_to_willis = True
            return self._driv.current_url
        except Exception as e:
            print("An error occurred: ", e)

    def __get_timeline_urls(self) -> list[Any]:
        """
        Try to get all the time line urls
        :return:
        """
        try:
            divs = self._driv.find_elements(By.XPATH,
                                            '//div[@class="list-group-item timeline-event-list-item flex-column pt-2 pb-0 border-0 px-2" and @data-region="event-list-item"]')
            return [div.find_element(By.TAG_NAME, 'a').get_attribute('href') for div in divs]
        except:
            return []

    # endregion

    # region get quiz data

    def _get_question_dict(self) -> dict:
        """
        Get all the question from the webpage and the answer. Ensure that there is an answers
        :return: dictionary of all the question and answer
        """
        soup = BeautifulSoup(self._driv.page_source, 'html.parser')
        question_divs = soup.find_all('div', class_='que')
        questions_dict = {}
        for question_div in question_divs:
            question_id = question_div['id']
            question_text = question_div.find('div', class_='qtext').text.strip()

            answer_divs = question_div.find_all('div', class_='answer')
            answer_text = []
            for answer_div in answer_divs:
                answer_text.append(answer_div.get_text())
            if answer_text:  # Ensure there is an answer. It is useless to keep them if we do not have the answer
                questions_dict[question_id] = {
                    'question_text': question_text,
                    'answers': answer_text
                }
        return questions_dict

    def _get_all_quiz_specific_courses(self, course_link: str, username: str, password: str) -> list[str]:
        """
        Go inside a course, find all the quiz link
        :param course_link: The URL where the course is
        :param username: willis username
        :param password: willise password
        :return: all of quiz's url from the course
        """
        if not self._got_connection_to_willis:  # Ensure a connections with moodle have been made
            self._willis_moodle_connection(username, password)
        self._open_specific_url(course_link)
        return self._get_all_quiz_url_in_webpage()

    def _get_question_answer_dict(self, course_type: str = '') -> dict:
        """
        Open in a review URL, find all the question and there answer
        :param course_type: The type of the course (the name)
        :return: Dictionary of the question and answer
        """
        soup = BeautifulSoup(self._driv.page_source, 'html.parser')
        try:  # Try to find if there is a way to have all on one page
            fullpage = soup.find('div', class_='card-body p-3').find('a', text='Show all questions on one page').get(
                'href')
            self._open_specific_url(fullpage)
            soup = BeautifulSoup(self._driv.page_source, 'html.parser')
        except Exception as e:
            print(f'there was a problem on having everything on one page error : {e}')
            try:
                soup.find('div', class_='drawer-toggler').click()
                soup = BeautifulSoup(self._driv.page_source, 'html.parser')
                fullpage = soup.find('div', class_='card-body p-3').find('a',
                                                                         text='Show all questions on one page').get(
                    'href')
                self._open_specific_url(fullpage)
                soup = BeautifulSoup(self._driv.page_source, 'html.parser')
            except Exception as e:
                print(f'There is no button {e}')
        question_divs = soup.find_all('div', class_='que')
        questions_dict = {}
        for question_div in question_divs:
            try:
                question_text = question_div.find('div', class_='qtext').text.strip()

                answer_divs = question_div.find_all('div', class_='rightanswer')
                answer_text = []
                for answer_div in answer_divs:
                    answer_text.append(answer_div.get_text())
                if answer_text:  # Ensure there is an answer. Do not keep empty data
                    questions_dict[question_text] = {
                        'cours': course_type,
                        'answer': answer_text
                    }
            except Exception as e:
                print(f'Error {e}')
        return questions_dict

    def _get_quiz_from_timeline(self, username, password) -> dict:
        """
        Get all the quiz from the timeline (quiz of the day)
        :param username: email to go to willis college
        :param password: password to go to willis college
        :return: Dictionary of all the quizs question and answers
        """
        self.__willis_college_connection(username, password)
        self.__willis_to_moodle()
        urls = self.__get_timeline_urls()
        for url in urls:
            if re.fullmatch(self.__QUIZ_DETECTION_REGEX, url):
                self._driv.get(url)
                break

        click_specific_btn(self._driv, 'class="btn btn-primary"', 'button')

        self._driv.switch_to.window(self._driv.window_handles[-1])

        WebDriverWait(self._driv, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'que')))

        return self._get_question_answer_dict()

    def _get_quiz_review(self) -> str:
        """
        When you are in a quiz URL find the button for the review and send the URL of the quiz
        :return: url
        """
        link = ''
        try:
            WebDriverWait(self._driv, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'table-responsive')))
            soup = BeautifulSoup(self._driv.page_source, 'html.parser')
            link = soup.find('div', class_='table-responsive').find('a').get(
                'href')  # Should give the link to the review
        except Exception as e:
            print(f'Can\'t find a link exception : {e}')
        return link

    def _get_all_course(self) -> list[str]:
        """
        Get all the course from the correct URL
        :return: a list of the course links
        """
        WebDriverWait(self._driv, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#page-container-1 > div > div')))
        soup = BeautifulSoup(self._driv.page_source, 'html.parser')
        course_div = soup.find_all('div', class_='card dashboard-card')
        allurl: list[str] = []
        for div in course_div:
            anchor = div.find('a')
            if anchor:
                allurl.append(anchor.get('href'))
        return allurl

    def _ensure_index_is_open(self) -> None:
        """
        When entering a course ensure that the index is open for further work on the page
        :return: None
        """
        WebDriverWait(self._driv, 10).until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'sr-only')))

        button = self._driv.find_element(By.CSS_SELECTOR, '.drawer-toggler.drawer-left-toggle.open-nav.d-print-none')

        if 'open' in button.get_attribute('class'):
            try:
                button.click()
            except Exception as e:
                print(f'page allready open {e}')
                button_element = self._driv.find_element(By.CSS_SELECTOR,
                                                         '#theme_boost-drawers-courseindex > div.drawerheader > button')
                button_element.click()
                time.sleep(1)
                button.click()
        else:
            pass

    def _get_all_quiz_url_in_webpage(self) -> list[str]:
        """
        find all the URL inside the webpage that have the word quiz
        :return: all the quiz URL from this web
        """
        try:
            WebDriverWait(self._driv, 10).until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'drawer drawer-left show d-print-none')))  # Should ensure that the index is open
        except Exception as e:
            print(f'find the class for the index as error : {e}')
        self._ensure_index_is_open()  # Ensure the index of the course is open
        WebDriverWait(self._driv, 10).until(EC.presence_of_element_located(
            (By.ID, 'theme_boost-drawers-courseindex')))  # Should ensure that the index is open
        soup = BeautifulSoup(self._driv.page_source, 'html.parser')
        # TODO: NEED TO UPDATE THE CRAPE OUT OF THIS. I need it to correctly get the index. Go in it get every link and compare it to the REGEX to see if the link would work
        course_data = soup.find_all('div',
                                    class_='drawer drawer-left d-print-none show')  # find the section with all the homework

        quizURL = []
        for div in course_data:

            divisions = div.find_all('a', class_='courseindex-link text-truncate')
            for d in divisions:
                print(d)
                href = d.get('href')
                if re.match(self.__QUIZ_DETECTION_REGEX, href):
                    quizURL.append(href)

        return quizURL  # All the links for that webpage of quizs

    def _willis_moodle_connection(self, username: str, password: str) -> None:
        """
        Easy way to connect to moodle.
        :param username: email to willis college
        :param password: password of the email
        :return: None
        """
        self._needDriver()
        self.__willis_college_connection(username, password)
        self.__willis_to_moodle()

    def _open_specific_url(self, url: str) -> None:
        """
        Open a specific URL from the same driver
        :param url: The path to open
        :return: None
        """
        self._needDriver()
        self._driv.get(url)
        WebDriverWait(self._driv, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    # endregion

    # region apply webpage data
    def _write_underneath_question_text(self, qa_text: str):
        """
        Writes answers from the provided string underneath each 'qtext' div on the current webpage.
        The text of the 'qtext' div is used as a key to get the corresponding answer from the string.
        :param qa_text: A string containing questions and answers in the format "Question: ... Answer: ..."
        """
        # Split the text into question-answer pairs
        qa_pairs = re.findall(r"(?ms)(Question:.*?(?:Answer:|Answers:).*?)(?=Question:|$)", qa_text)

        # Find all 'qtext' divs on the page
        qtext_divs = self._driv.find_elements(By.CLASS_NAME, 'qtext')

        # For each 'qtext' div
        for i, qtext_div in enumerate(qtext_divs):
            # Get the question text
            question = qtext_div.get_attribute('textContent').strip()

            # Find the corresponding answer in the QA pairs
            answer = None
            for qa_pair in qa_pairs:
                if question in qa_pair:
                    answer = re.split("Answer:|Answers:", qa_pair, 1)[1].strip()
                    break

            # If an answer was found, write it directly under the 'qtext' div
            if answer:
                # Create a link to Google search with the question
                search_query = urllib.parse.quote(question)
                google_search_link = f"https://www.google.com/search?q={search_query}"
                answer_with_link = f"{answer} <a href='{google_search_link}' target='_blank'>[Search on Google]</a>"

                script = """
                    var p = document.createElement('p');
                    p.innerHTML = arguments[0];
                    p.style.color = 'green';
                    arguments[1].parentNode.insertBefore(p, arguments[1].nextSibling);
                """
                self._driv.execute_script(script, answer_with_link, qtext_div)
    # endregion


def click_specific_btn(driver, attr_btn: str, tag_btn: str):
    try:
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"{tag_btn}[{attr_btn}]")))
        button.click()
    except Exception as e:
        print("Button not found.", e)
