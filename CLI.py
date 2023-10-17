
from module import quizletModule, user_handeling, WILLHANDLE, WillisAnswered
import argparse
import sys
"""
LINK TO ADD 
https://quizlet.com/388298485/chapters-5-6-flash-cards/
https://quizlet.com/164457278/3408-comp-security-exam-2-flash-cards/
https://quizlet.com/394116988/chapter-5-6-quiz-flash-cards/
https://quizlet.com/388298485/chapters-5-6-flash-cards/
https://quizlet.com/au/449898184/cis2005-mod-4-review-quiz-flash-cards/
https://quizlet.com/392661676/chapters-13-14-flash-cards/
https://quizlet.com/279820082/network-security-basics-test-2-flash-cards/
"""



def cli_helper():
    parser = argparse.ArgumentParser(description='The CLI usage to get all your questions and answers')
    parser.add_argument('-ql', '--quizlet', nargs=1, help='Enter the quizlet link')
    parser.add_argument('-mql', '--getMultipleQuestion', nargs='+', help='go take multiple link for quizlet in this '
                                                              'format [URL,URL,URL...]')
    parser.add_argument('-q', '--getQuestion', help='Research a question inside the database')

    return parser


def speakToQuizlet(quizlet_link, quizlet_t: quizletModule.quizlet_talker) -> quizletModule.quizlet_talker:
    quizlet_t.website = quizlet_link
    quizlet_t.go_to_quiz()
    page_data = quizlet_t.quizlet_communication_question_answer()
    dataHandle.add_dictionary_to_json(page_data)
    return quizlet_t


if __name__ == '__main__':
    parser = cli_helper()
    args = parser.parse_args()
    dataHandle = WillisAnswered.DataHandle()

    if args.quizlet:
        quizlet_page = quizletModule.quizlet_talker()
        speakToQuizlet(args.quizlet[0], quizlet_page).close_quizlet_driver()

    if args.getMultipleQuestion:
        quizlet_page = quizletModule.quizlet_talker()
        for e in args.getMultipleQuestion:
            quizlet_page = speakToQuizlet(e, quizlet_page)
        quizlet_page.close_quizlet_driver()

    if args.getQuestion:
        answer = dataHandle.get_question_from_prompt(args.getQuestion)
        for e in answer:
            print(e)

