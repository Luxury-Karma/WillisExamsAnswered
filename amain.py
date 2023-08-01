import argparse
from module import WillisAnswered


def main():
    parser = argparse.ArgumentParser(description="CLI for DataHandle class")

    subparsers = parser.add_subparsers(dest="command")
    #region I know exacly what I want and ints note in the base program
    init_parser = subparsers.add_parser("init", help="Initialize a DataHandle object")
    init_parser.add_argument("-r", "--regex", help="Provide regex")
    init_parser.add_argument("-j", "--jsonDic", help="Provide a dictionary in json format")
    init_parser.add_argument("-d", "--pathToData", help="Provide path to data")
    init_parser.add_argument("-u", "--pathToUser", help="Provide path to user")
    init_parser.add_argument("-k", "--pathToKey", help="Provide path to key")
    init_parser.add_argument("-c", "--courseURL", help="Provide course URL")
    init_parser.add_argument("-s", "--pathSetting", help="Provide path to setting")
    #endregion

    set_user_account = subparsers.add_parser("add_account", help = "Set Willis college account (email and password)")
    set_user_account.add_argument("-u", "--user", help= "Input your willis email exemple : Jhon.Smith@Students.williscollege.com")
    set_user_account.add_argument("-p", "--password", help = "Input your willis email password")
    set_user_account.add_argument("-fp","--file_password", help="Input the password you will use for the file")


    set_user_setting = subparsers.add_parser("setting", help="Set up the personnal setting for the program")
    set_user_setting.add_argument("-b", "--browser", help="Input the browser (google,edge,safari,firefox)")


    add_quiz_parser = subparsers.add_parser("add_quiz", help="Add a specific quiz review")
    add_quiz_parser.add_argument("-l", "--link_of_review", help="The exact URL of the review you want to add")
    add_quiz_parser.add_argument("-p", "--file_password", help="The password to unlock user file")

    add_question_parser = subparsers.add_parser("add_question", help="Manually add a question and answer")
    add_question_parser.add_argument("-q", "--question", required=True, help="Question to add")
    add_question_parser.add_argument("-a", "--answer", required=True, help="Answer to the question")
    add_question_parser.add_argument("-t", "--course_type", required=True, help="Type of the course")

    add_course_questions_parser = subparsers.add_parser("add_course_questions", help="Add course questions from a link")
    add_course_questions_parser.add_argument("-l", "--course_link", required=True, help="Exact link of the course")
    add_course_questions_parser.add_argument("-p", "--file_password", required=True,
                                             help="The password to unlock user file")

    get_quiz_question_parser = subparsers.add_parser("get_question_answer", help="Get all linked question from the prompt")
    get_quiz_question_parser.add_argument("-c", "--print_in_consol",required=True, help= "Enter y or n if you want it in the cmd or not")
    get_quiz_question_parser.add_argument('-s',"--print_in_file", required=False, help= "Enter the path to a file where you want to save the data")
    get_quiz_question_parser.add_argument("-g", "--get_question_answer", required=True, help="Enter the question you are searching for")

    args = parser.parse_args()

    data_handle =WillisAnswered.DataHandle()

    if args.command == "add_account":
        data_handle.willis_user_creation(args.user, args.password, args.file_password)
    elif args.command == "setting":
        dic = {
            "browser": args.browser
        }
        data_handle.change_user_setting(dic)
    elif args.command == "add_quiz":
        data_handle.willis_add_specific_quiz_review(args.link_of_review, args.file_password)

    elif args.command == "add_question":
        data_handle.manualy_add_question_answer(args.question, args.answer, args.course_type)
        print('Question added')

    elif args.command == "add_course_questions":
        data_handle.willis_add_course_questions(args.course_link, args.file_password)
        print('Question added')

    elif args.command == "get_question_answer":
        qa = []
        for e in data_handle.get_question_from_prompt(args.get_question_answer):
            qa.append(f'Question: {e[0]}\nAnswer: {data_handle.find_answer_by_question(e[0])["answer"]}\n\n')
        qa = ''.join(qa)

        if args.print_in_consol.lower() == 'y':
            print(qa)
        if args.print_in_file:
            try:
                with open(args.print_in_file, 'w') as f:
                    f.write(qa)
            except OSError:
                print('cannot open', args.print_in_file)
    else:
        print(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()

