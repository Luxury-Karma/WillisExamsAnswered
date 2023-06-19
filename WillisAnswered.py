import re
import json
import time

from module import WILLHANDLE
from module import user_handeling as user
import os


class DataHandle(WILLHANDLE.WILLHANDLE):

    def __init__(self, regex: str = None, jsonDic: dict = None, pathToData: str = None, pathToUser: str = None,
                 pathToKey: str = None, courseURL: str = None):
        super().__init__()
        self.DataPath = pathToData if pathToData else '.\\userFile\\willisAnswer.json'
        self.userPath = pathToUser if pathToUser else '.\\userFile\\profile.json'
        self.keyPath = pathToKey if pathToKey else '.\\userFile\\decryption.txt'
        self.regex = regex
        self.jsonDictionary = jsonDic if jsonDic else self.openJsonData()
        self.courseURL: str = courseURL if courseURL else 'https://students.willisonline.ca/my/courses.php'




    def regexCreator(self, searchedWords: list[str]) -> None:
        '''
        Apply the new regex search on the object
        :param searchedWords: The words to make a search
        :return: None
        '''
        regStr = '|'.join(searchedWords)
        self.regex = f'(?:{regStr})'

    def openJsonData(self) -> None:
        '''
        Open a Json Format File and return a dictionary
        :param pathToData:
        :return:None
        '''

        try :
            with open(self.DataPath, 'r') as file:
                data = json.load(file)
        except Exception as e:
            print(f'{e} error in file')
        return data

    def userInput(self, prompt :str) -> list[str]:
        """
        Get an input from the user and correctly format it
        :param prompt: What do we say to the user
        :return: the correctly formated list of string
        """
        inp = input(prompt)
        inp = inp.lower().split()  # force it to split at each space to have individual word
        return inp

    def findAllMatchingQuestion(self) -> list[[str, int]]:

        questionList:list[list[str, int]] = []
        for question in self.jsonDictionary.keys():
            # Detect similar wording
            if re.search(self.regex, question.lower()):
                questionList.append([question, len(re.findall(self.regex, question.lower()))])
        questionList.sort(key=lambda x: x[1], reverse=True)  # sort from the highest match amount
        return questionList

    # TODO: ensureit get correctly the data
    def addQuestionToDictionary(self, urlOfQuiz: str):
        """
        Update the Question list for you with a simple link
        :return: None
        """
        self.open_specific_url(urlOfQuiz)  # go to the open quiz page
        # add the data to the file

        with open(self.DataPath, 'r') as QAData:
            existingData = json.load(QAData)
            newData = self.get_question_answer_dict()
            try:
                existingData.update(newData)
            except Exception as e:
                print(f'The dictionary was empty {e}')

        with open(self.DataPath, 'w') as NewQAData:
            json.dump(existingData, NewQAData, indent=4)

    def needAccessToWebsite(self, userSection : str) -> None:
        """
        Open the willis website and connect
        :return: a driver at the connection page of willis
        """
        with open(self.userPath, 'r') as profiler:

            profiler = profiler.read()
            password = input('Enter the password for the file')
            key, salt = user.load_key_and_salt_from_file(self.keyPath)
            profiler = user.decrypt_data(profiler, password, key, salt)
            profiler = json.loads(profiler)
            self.willis_moodle_connection(profiler[userSection]['username'], profiler[userSection]['password'])

    def willis_user_creation(self, path_to_data):
        if not user.data_detection(path_to_data):
            username: str = input('Enter the willis email exemple : \'bob.ross@students.williscollege.com\': ')
            password: str = input('Enter you\'re willis email password: ')
            fPassword: str = input('Enter the file password')
            user.create_data_file(path_to_data, username, password, fPassword, self.keyPath)

    def getQuestionFromPrompt(self, search: list[str]):
        self.regexCreator(search)
        return self.findAllMatchingQuestion()

    def ensure_files_are_present(self):
        if not os.path.isfile(self.userPath):
            self.willis_user_creation(self.userPath)
            print(f'{self.userPath} created')
        if not os.path.isfile(self.DataPath):  # When we do not have the file of answer
            with open(self.DataPath, 'w') as f:
                json.dump({}, f, indent=4)
            print(f'{self.DataPath} created')

    def global_quiz_data_collecting(self):
        self.needAccessToWebsite('Willis_College_user')  # Open the moodle for the website

        self.open_specific_url(self.courseURL)  # Connect to all of the accessible courses
        course_url = self.get_all_course()  # get all the URL of the accessible courses

        for course in course_url:  # Pass trough all of the course URLS
            self.open_specific_url(course)  # Go the one of the course URL
            quizs_url = self.get_all_quiz_url_in_webpage()  # find all the quizs URL
            for quiz in quizs_url:  # Pass trough all of the quizs URLS
                self.open_specific_url(quiz)  # Open a quiz URL
                quiz_link = self.get_quiz_review()  # Open the review if it exist
                if quiz_link != '':  # If there is data write it to the json data
                    self.addQuestionToDictionary(quiz_link)  # Write the data in the json file
                else:
                    print('There is no link for the review')  # Mension there is no data\




