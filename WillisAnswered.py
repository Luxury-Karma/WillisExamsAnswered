import re
import json
from module import WILLHANDLE


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


def addQuestionToDictionary():
    d = WILLHANDLE.WILLHANDLE()
    d.


def main():
    r = regexCreator(userInput('word search: '))
    jdata = openJsonData('.\\data.json')
    questionList: list[[str,int]] = findAllMatchingQuestion(r, jdata)
    for question in questionList:
        print(f'{question[0]} the answer is : {jdata[question[0]]["answer"]}, from the course : {jdata[question[0]]["cours"]}')


if __name__ == '__main__':
    main()



