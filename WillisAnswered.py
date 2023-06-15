import re
import json
from module import WILLHANDLE
from module import user_handeling as user
import os


def regexCreator(searchedWords):
    regStr = '|'.join(searchedWords)
    return f'(?:{regStr})'


def openJsonData(pathToData: str) -> dict:
    jsonDic ={}
    try :
        with open(pathToData, 'r') as data:
            jsonDic = json.load(data)
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
        newData = driv.get_question_dict()
        fulldata = existingdata.append(newData)
    with open(QAFilePath, 'w') as QAData:
        json.dump(fulldata, QAData, indent=4)








def needAccessToWebsite():
    """
    Open the willis website and connect
    :return: a driver at the connection page of willis
    """
    d = WILLHANDLE.WILLHANDLE()
    with open('profile.json', 'r') as profiler:
        profiler = profiler.read()
        with open('decryption.txt', 'r') as decryption:
            password = input('Enter the password for the file')
            key, salt = user.load_key_and_salt_from_file('decryption.txt')
            profiler = user.decrypt_data(profiler, password, key, salt)
        d.willis_moodle_connection(profiler['Willis']['username'], profiler['Willis']['password'])
    return d






def main():
    if not os.path.isfile('willisAnswer.json'):
        pass  # When we do not have the file of answer
    if not os.path.isfile('profile.json'):
        path_to_data = 'username.json'
        willis_username = input("Enter your Willis email (e.g., 'bob.ross@students.williscollege.com'): ")
        willis_password = input("Enter your Willis email password: ")
        fpassword = input("File password")
        user.create_data_file(path_to_data, willis_username, willis_password, fpassword)
        base_key, base_salt = user.generate_base_key_and_salt()
        user.save_key_and_salt_to_file(base_key, base_salt, 'decryption.txt')
        user.encrypt_file(path_to_data, fpassword, base_key, base_salt)

    r = regexCreator(userInput('word search: '))
    jdata = openJsonData('.\\data.json')
    questionList: list[[str,int]] = findAllMatchingQuestion(r, jdata)
    for question in questionList:
        print(f'{question[0]} the answer is : {jdata[question[0]]["answer"]}, from the course : {jdata[question[0]]["cours"]}')


if __name__ == '__main__':
    main()



