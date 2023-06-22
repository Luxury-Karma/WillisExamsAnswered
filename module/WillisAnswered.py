import json
import os
import re

from module import WILLHANDLE
from module import user_handeling as user


class DataHandle(WILLHANDLE.WILLHANDLE):

    def __init__(self, regex: str = None, jsonDic: dict = None, pathToData: str = None, pathToUser: str = None,
                 pathToKey: str = None, courseURL: str = None):
        super().__init__()
        self.__pyPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        self._DataPath = pathToData if pathToData else os.path.join(self.__pyPath, 'userFile\\willisAnswer.json')
        self._userPath = pathToUser if pathToUser else os.path.join(self.__pyPath, 'userFile\\profile.json')
        self._keyPath = pathToKey if pathToKey else os.path.join(self.__pyPath, 'userFile\\decryption.txt')
        self.regex = regex
        self._jsonDictionary = jsonDic if jsonDic else self.__openJsonData()
        self._courseURL: str = courseURL if courseURL else 'https://students.willisonline.ca/my/courses.php'

    def __regexCreator(self, searchedWords: list[str]) -> None:
        '''
        Apply the new regex search on the object
        :param searchedWords: The words to make a search
        :return: None
        '''
        regStr = '|'.join(searchedWords)
        self.regex = f'(?:{regStr})'

    def __openJsonData(self) -> None:
        '''
        Open a Json Format File and return a dictionary
        :param pathToData:
        :return:None
        '''
        self.__ensure_files_are_present()
        try:
            with open(self._DataPath, 'r') as file:
                data = json.load(file)
        except Exception as e:
            print(f'{e} error in file')
        return data

    def __findAllMatchingQuestion(self) -> list[[str, int]]:

        questionList: list[list[str, int]] = []
        for question in self._jsonDictionary.keys():
            # Detect similar wording
            if re.search(self.regex, question.lower()):
                questionList.append([question, len(re.findall(self.regex, question.lower()))])
        questionList.sort(key=lambda x: x[1], reverse=True)  # sort from the highest match amount
        return questionList

    def __addQuestionToDictionary(self, urlOfQuiz: str):
        """
        Update the Question list for you with a simple link
        :return: None
        """
        self._open_specific_url(urlOfQuiz)  # go to the open quiz page
        # add the data to the file

        with open(self._DataPath, 'r') as QAData:
            existingData = json.load(QAData)
            newData = self._get_question_answer_dict()
            try:
                existingData.update(newData)
            except Exception as e:
                print(f'The dictionary was empty {e}')

        with open(self._DataPath, 'w') as NewQAData:
            json.dump(existingData, NewQAData, indent=4)

    def __needAccessToWebsite(self, userSection: str, password: str) -> None:
        """
        Open the willis website and connect
        :return: a driver at the connection page of willis
        """
        with open(self._userPath, 'rb', ) as profiler:
            profiler = profiler.read()
            key, salt = user.load_key_and_salt_from_file(self._keyPath)
            profiler = user.decrypt_data(profiler, password, key, salt)
            profiler = json.loads(profiler)
            self._willis_moodle_connection(profiler[userSection]['username'], profiler[userSection]['password'])

    def willis_user_creation(self, username: str, password: str, fpassword: str) -> None:
        """
        The creation of the file account for the connection
        :param username: The willis college user name exemple : Bob.Ross@Students.Williscollege.com
        :param password: The password for the account
        :param fpassword: The password encrypting the file
        :return: None
        """
        if not user.data_detection(self._userPath):
            user.create_data_file(self._userPath, username, password, fpassword, self._keyPath)

    def getQuestionFromPrompt(self, search: str):
        self.__regexCreator(search.lower().split())
        return self.__findAllMatchingQuestion()

    def __ensure_files_are_present(self):
        if not os.path.isfile(self._userPath):
            print(f'{self._userPath} created')
        if not os.path.isfile(self._DataPath):  # When we do not have the file of answer
            with open(self._DataPath, 'w') as f:
                json.dump({}, f, indent=4)
            print(f'{self._DataPath} created')

    def global_quiz_data_collecting(self, password: str):
        # TODO: Update to have a check up if the json is decrypted
        self.__needAccessToWebsite('Willis_College_user', password)  # Open the moodle for the website

        self._open_specific_url(self._courseURL)  # Connect to all of the accessible courses
        course_url = self._get_all_course()  # get all the URL of the accessible courses

        for course in course_url:  # Pass trough all of the course URLS
            self._open_specific_url(course)  # Go the one of the course URL
            quizs_url = self._get_all_quiz_url_in_webpage()  # find all the quizs URL
            for quiz in quizs_url:  # Pass trough all of the quizs URLS
                self._open_specific_url(quiz)  # Open a quiz URL
                quiz_link = self._get_quiz_review()  # Open the review if it exist
                if quiz_link != '':  # If there is data write it to the json data
                    self.__addQuestionToDictionary(quiz_link)  # Write the data in the json file
                else:
                    print('There is no link for the review')  # Mension there is no data\
        self._driv.close()

    def find_answer_by_question(self, question: str) -> dict:
        return self._jsonDictionary[question]
