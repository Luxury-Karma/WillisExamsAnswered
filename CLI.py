
from module import quizletModule, user_handeling, WILLHANDLE, WillisAnswered
import argparse
import sys

def cli_helper():
    parser = argparse.ArgumentParser(description='The CLI usage to get all your questions and answers')
    parser.add_argument('-ql', '--quizlet', nargs=1, help='Enter the quizlet link')
    return parser

if __name__ == '__main__':
    parser = cli_helper()
    args = parser.parse_args()
    dataHandle = WillisAnswered.DataHandle()

    if args.quizlet:
        quizlet_link = args.quizlet[0]
        quizlet = quizletModule.quizlet_talker(quizlet_website=quizlet_link)
        page_data = quizlet.quizlet_communication_question_answer()
        dataHandle.add_dictionary_to_json(page_data)


