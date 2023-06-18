import re
import json
import time

from module import WILLHANDLE
from module import user_handeling as user
import os


def regexCreator(searchedWords):
    regStr = '|'.join(searchedWords)
    return f'(?:{regStr})'


def openJsonData(pathToData: open) -> dict:
    jsonDic ={}
    try :
        jsonDic = json.load(pathToData)
    except Exception as e:
        print(f'{e} error in file')
    return jsonDic

def userInput(prompt :str) -> list[str]:
    inp = input(prompt)
    inp = inp.lower().split()  # force it to split at each space to have individual word
    return inp

def findAllMatchingQuestion(r:str, jdata: dict) -> list[[str,int]]:
    questionList:list[list[str,int]] = []
    for question in jdata.keys():
        # Detect similar wording
        if re.search(r, question.lower()):
            questionList.append([question, len(re.findall(r, question.lower()))])
    questionList.sort(key=lambda x: x[1], reverse=True)  # sort from the highest match amount
    return questionList

# TODO: ensureit get correctly the data
def addQuestionToDictionary(urlOfQuiz: str, driv: WILLHANDLE.WILLHANDLE, QAFilePath: str)   :
    """
    Update the Question list for you with a simple link
    :return: None
    """
    driv.open_specific_url(urlOfQuiz)  # go to the open quiz page
    # add the data to the file

    with open(QAFilePath, 'r') as QAData:
        existingdata = json.load(QAData)
        newData = driv.get_question_answer_dict()
        try:
            existingdata.update(newData)
        except Exception as e:
            print(f'The dictionary was empty {e}')

    with open(QAFilePath, 'w') as NewQAData:
        json.dump(existingdata, NewQAData, indent=4)


def needAccessToWebsite(user_profile_path: str, keys_path: str, userSection : str) -> WILLHANDLE.WILLHANDLE:
    """
    Open the willis website and connect
    :return: a driver at the connection page of willis
    """
    d = WILLHANDLE.WILLHANDLE()
    time.sleep(3)
    with open(user_profile_path, 'r') as profiler:

        profiler = profiler.read()
        password = input('Enter the password for the file')
        key, salt = user.load_key_and_salt_from_file(keys_path)
        profiler = user.decrypt_data(profiler, password, key, salt)
        profiler = json.loads(profiler)
        d.willis_moodle_connection(profiler[userSection]['username'], profiler[userSection]['password'])

    return d


def willis_user_creation(path_to_data, path_to_key: str):
    if not user.data_detection(path_to_data):
        username: str = input('Enter the willis email exemple : \'bob.ross@students.williscollege.com\': ')
        password: str = input('Enter you\'re willis email password: ')
        fPassword: str = input('Enter the file password')
        user.create_data_file(path_to_data, username, password, fPassword, path_to_key)



def main():
    path_to_user_data: str = '.\\userFile\\profile.json'
    path_key: str = '.\\userFile\\decryption.txt'
    willisAnswerFile = '.\\userFile\\willisAnswer.json'
    course_Section_url: str = 'https://students.willisonline.ca/my/courses.php'
    if not os.path.isfile('profile.json'):
        willis_user_creation(path_to_user_data, path_key)
    if not os.path.isfile(willisAnswerFile):  # When we do not have the file of answer
        with open(willisAnswerFile, 'w') as f:
            json.dump({}, f, indent=4)
            print('file created')
    driver: WILLHANDLE.WILLHANDLE = needAccessToWebsite(path_to_user_data, path_key, 'Willis_College_user')
    driver.open_specific_url(course_Section_url)
    course_url = driver.get_all_course()


    for course in course_url:
        driver.open_specific_url(course)  # should put on the URL of the website
        quizs_url = driver.get_all_quiz_url_in_webpage()  # should find all the quizs URL
        for quiz in quizs_url:
            driver.open_specific_url(quiz)
            quiz_link = driver.get_quiz_review()
            if quiz_link != '':
                addQuestionToDictionary(quiz_link, driver, willisAnswerFile)
            else:
                print('There is no link for the review')





    r = regexCreator(userInput('word search: '))
    jdata = {}  # initialisation
    try:
        with open(path_to_user_data,'r') as data:
            uspassword = input('enter the password for the user file')
            ukey, usalt = user.load_key_and_salt_from_file(path_key)
            user.decrypt_data(path_to_user_data, uspassword, ukey, usalt)
            jdata = openJsonData('.\\data.json')
    except Exception as e:
        print(f'There was an error with the file error : {e}')
    questionList: list[[str,int]] = findAllMatchingQuestion(r, jdata)
    for question in questionList:
        print(f'{question[0]} the answer is : {jdata[question[0]]["answer"]}, from the course : {jdata[question[0]]["cours"]}')


if __name__ == '__main__':
    main()



