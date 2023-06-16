import re
import json
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
        fulldata = existingdata.append(newData)
    with open(QAFilePath, 'w') as QAData:
        json.dump(fulldata, QAData, indent=4)


def needAccessToWebsite(user_profile_path: str, keys_path: str) -> WILLHANDLE.WILLHANDLE:
    """
    Open the willis website and connect
    :return: a driver at the connection page of willis
    """
    d = WILLHANDLE.WILLHANDLE()
    with open(user_profile_path, 'r') as profiler:
        profiler = profiler.read()
        password = input('Enter the password for the file')
        key, salt = user.load_key_and_salt_from_file(keys_path)
        profiler = user.decrypt_data(profiler, password, key, salt)
        d.willis_moodle_connection(profiler['Willis']['username'], profiler['Willis']['password'])
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
            print('file created')
        driver: WILLHANDLE.WILLHANDLE = needAccessToWebsite(path_to_user_data, path_key)
        driver.open_specific_url(course_Section_url)
        course_url = driver.get_all_quiz_url_in_webpage()
        for course in course_url:
            driver.open_specific_url(course)  # should put on the URL of the website
            quizs_url = driver.get_all_quiz_url_in_webpage()  # should find all the quizs URL
            for quiz in quizs_url:
                driver.open_specific_url(quiz)
                addQuestionToDictionary(driver.get_quiz_review(), driver, willisAnswerFile)


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



