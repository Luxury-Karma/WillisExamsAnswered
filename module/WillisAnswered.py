import json
import os
import re
from module import WILLHANDLE
from module import user_handeling as user


class DataHandle(WILLHANDLE.WILLHANDLE):

    def __init__(self, regex: str = None, jsonDic: dict = None, pathToData: str = None, pathToUser: str = None,
                 pathToKey: str = None, courseURL: str = None, pathSetting: str = None):
        super().__init__()
        self.__pyPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        self.__user_dir = os.path.join(self.__pyPath, 'userFile')
        self._DataPath = pathToData if pathToData else os.path.join(self.__pyPath, 'userFile\\willisAnswer.json')
        self._userPath = pathToUser if pathToUser else os.path.join(self.__pyPath, 'userFile\\profile.json')
        self._keyPath = pathToKey if pathToKey else os.path.join(self.__pyPath, 'userFile\\decryption.txt')
        self._userSettingPath = pathSetting if pathSetting else os.path.join(self.__pyPath, 'userFile\\setting.json')
        self.regex = regex
        self._jsonDictionary = jsonDic if jsonDic else self.__open_json_data()
        self._courseURL: str = courseURL if courseURL else 'https://students.willisonline.ca/my/courses.php'
        self.__password_entered: str = ''

        self.__user_section = 'Willis_College_user'


    # region Regex Usage
    def __regex_creator(self, searchedWords: list[str]) -> None:
        """
        Apply the new regex search on the object
        :param searchedWords: The words to make a search
        :return: None
        """
        regex_string = '|'.join(searchedWords)
        self.regex = f'(?:{regex_string})'

    def __find_all_matching_question(self) -> list[[str, int]]:
        """
        Go in the data file. Try to find all of the question that match the actual regex of the object
        :return: all of the matching question with the amount of occurence
        """

        question_list: list[list[str, int]] = []
        for question in self._jsonDictionary.keys(): # Pass inside of all the question and look if it could be one
            # Detect similar wording
            match = re.findall(self.regex, question.lower())
            if match:
                unique_matches = len(set(match))  # Count unique matches
                total_matches = len(match)  # Count total matches
                question_list.append([question, (unique_matches, total_matches)])
        question_list.sort(key=lambda x: (x[1][0], x[1][1]), reverse=True)  # sort by unique matches, then total matches
        return question_list

    # endregion

    # region Files
    def __open_json_data(self) -> None:
        """
        Open a Json Format File and return a dictionary
        :return:None
        """
        self.__ensure_files_are_present()
        try:
            with open(self._DataPath, 'r') as file:
                data = json.load(file)
        except Exception as e:
            print(f'{e} error in file')
        return data


# TODO: Update the saving
    def __add_question_to_dictionary(self, url_quiz: str):
        """
        Update the Question list for you with a simple link
        :return: None
        """
        self._open_specific_url(url_quiz)  # go to the open quiz page

        new_data = self._get_question_answer_dict()
        self.__add_data_to_json(new_data)



    def __add_data_to_json(self, new_data: dict):
        # Load existing data
        try:
            with open(self._DataPath, 'r') as QAData:
                existing_data = json.load(QAData)
        except FileNotFoundError:
            print(f'The file {self._DataPath} does not exist. Creating a new one.')
            existing_data = {}

        # If existing_data is not a dictionary, we initialize it
        if not isinstance(existing_data, dict):
            print(f'Existing data is not a dictionary, initializing a new one.')
            existing_data = {}

        # If new data key exists in existing data, print a warning
        intersecting_keys = set(existing_data.keys()).intersection(set(new_data.keys()))
        if intersecting_keys:
            print(f'Warning: New data keys {intersecting_keys} exist in existing data. They will be overwritten.')

        # Update the data
        existing_data.update(new_data)
        self._jsonDictionary = existing_data  # Update Object memory

        # Write the updated data back to file
        with open(self._DataPath, 'w') as NewQAData:
            json.dump(existing_data, NewQAData, indent=4)



    def willis_add_specific_quiz_review(self, link_of_review: str, file_password: str):

        """
        Add to the data dictionary a specific URL worth of data
        :param link_of_review: The exact URL of the review you want to add
        :param user_section: The name where the willis user is in the json file
        :param file_password : The password to unlock user file
        :return: Nothing
        """
        if not self._got_connection_to_willis:
            self.__handle_non_connection(file_password)

        self.__add_question_to_dictionary(link_of_review)

    def manualy_add_question_answer(self, question: str, answer: str, course_type: str) -> None:
        """
        Receive a question, answer, course type and add it to the dictionarry
        :return: None
        """
        #self._jsonDictionary is allready the full data of the file loaded
        newdata: dict = {  # Create the data of the dictionary
            'cours': course_type,
            'answer': answer
        }
        self._jsonDictionary[question] = newdata  # Add the new data inside of the existing loaded data

        with open(self._DataPath, 'w') as file:
            json.dump(self._jsonDictionary, file, indent=4)


    # TODO: add data verification
    def give_json_data(self, path_to_data: str) -> None:
        """
        Give a formatted json file and add it to the data
        careful in this version there is no data verification
        :param path_to_data: The path where the json file is
        :return: None
        """
        try:
            with open(path_to_data, 'r') as new_file:
                new_data = json.load(new_file)
                self._jsonDictionary.update(new_data)

            with open(self._DataPath, 'w') as file:
                json.dump(self._jsonDictionary, file, indent=4)

        except IOError as io_err:
            print(f"IOError: {io_err}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def willis_user_creation(self, username: str, password: str, file_password: str) -> None:
        """
        The creation of the file account for the connection
        :param username: The willis college user name exemple : Bob.Ross@Students.Williscollege.com
        :param password: The password for the account
        :param file_password: The password encrypting the file
        :return: None
        """

        user.create_data_file(self._userPath, username, password, file_password, self._keyPath)

    # region searching file

    def get_question_from_prompt(self, search: str) -> list:
        """
        Create the regex and get all matching question
        :param search: the words we want to research
        :return: list of all the question matching the regex created
        """
        self.__regex_creator(search.lower().split())
        return self.__find_all_matching_question()

    # endregion

    # region Website Handling

    def __need_access_to_website(self: str, password: str) -> None:
        """
        Open the willis website and connect
        :return: a driver at the connection page of willis
        """
        self.__password_entered = password
        with open(self._userPath, 'rb', ) as profiler:
            profiler = profiler.read()
            key, salt = user.load_key_and_salt_from_file(self._keyPath)
            profiler = user.decrypt_data(profiler, password, key, salt)
            profiler = json.loads(profiler)
            self._willis_moodle_connection(profiler[self.__user_section]['username'], profiler[self.__user_section]['password'])

    def __handle_non_connection(self, password: str) -> list[str]:

        with open(self._userPath, 'rb') as profiler:
            key, salt = user.load_key_and_salt_from_file(self._keyPath)
            profiler = json.loads(user.decrypt_data(profiler.read(), password, key, salt))
            self._willis_moodle_connection(profiler[self.__user_section]['username'], profiler[self.__user_section]['password'] )



    def willis_add_course_questions(self, course_link: str, file_password: str) -> None:

        """
        Get in a specific course URL, find all of the quizs and get the question and answer of each of them
        :param course_link: Exact link of the course
        :param user_section: section where the user is in the json file
        :return: None
        """
        username: str = ''
        password: str = ''
        if not self._got_connection_to_willis:
            self.__handle_non_connection(file_password)
        for e in self._get_all_quiz_specific_courses(course_link, username, password):
            self._open_specific_url(e)
            try:
                self._open_specific_url(self._get_quiz_review())
                new_data: dict = self._get_question_answer_dict('')
                self.__add_data_to_json(new_data)

            except Exception as e:
                print(f'No link {e}')



    # endregion

    def __ensure_files_are_present(self) -> None:
        """
        Protect the opening of the file if the files do not exist yet
        :return:
        """

        if not os.path.isdir(self.__user_dir):
            print(f'dir created : {self.__user_dir}')
            os.mkdir(self.__user_dir)
        if not os.path.isfile(self._userPath):
            print(f'{self._userPath} created')
        if not os.path.isfile(self._DataPath):  # When we do not have the file of answer
            with open(self._DataPath, 'w') as f:
                json.dump({}, f, indent=4)
            print(f'{self._DataPath} created')

    def global_quiz_data_collecting(self, password: str) -> None:
        """
        Go in each course you have on the willis web page and go in each quiz its find to get the data
        :param password: The password you gave to the encryption files
        :return: None
        """
        self.__need_access_to_website(password)  # Open the moodle for the website

        self._open_specific_url(self._courseURL)  # Connect to all of the accessible courses
        course_url = self._get_all_course()  # get all the URL of the accessible courses

        for course in course_url:  # Pass trough all of the course URLS
            self._open_specific_url(course)  # Go the one of the course URL
            quizs_url = self._get_all_quiz_url_in_webpage()  # find all the quizs URL
            for quiz in quizs_url:  # Pass trough all of the quizs URLS
                self._open_specific_url(quiz)  # Open a quiz URL
                quiz_link = self._get_quiz_review()  # Open the review if it exist
                if quiz_link != '':  # If there is data write it to the json data
                    self.__add_question_to_dictionary(quiz_link)  # Write the data in the json file
                else:
                    print('There is no link for the review')  # Mension there is no data\
        self._driv.close()
        self._got_connection_to_willis = False  # The driver is closed so there is no more connection

    def find_answer_by_question(self, question: str) -> dict:
        """
        Find the question and return the dictionary linked to it
        :param question: Question (name) in the json file
        :return: The dictionary linked to that name
        """
        return self._jsonDictionary[question]

    # endregion


    # region setting handeling

    def change_user_setting(self, setting: dict):
        with open(self._userSettingPath, 'w') as file:
            json.dump(setting, file)
        br = self.get_user_browser()
        self._browser = br

    def get_user_browser(self) -> str:
        """
        :return: The browser the user want to use. Default value at edge
        """
        try:
            with open(self._userSettingPath, 'r') as file:
                data = json.load(file)  # Open it as a dictionary
                return data['browser']
        except ValueError:
            return 'edge'  # There is an error by reading the file. default value return
    #end region