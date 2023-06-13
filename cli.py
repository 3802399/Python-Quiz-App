import quiz as _quiz
import random

class CLI:
    def __init__(self):
        self.quiz_name = ""
        self.quiz_data = None
        self.quiz = None
        self.directory = ""
        self.quizzes = []

        self.manager = _quiz.QuizManager()

    def find_and_run_quiz(self):
        # if not creating a quiz, run it
        self.get_all_quizzes_from_user()
        self.get_user_choice_of_quiz()
        self.get_quiz_data_from_name()
        self.get_quiz_from_data()
        self.run_quiz()

    def run_quiz(self):
        quiz = self.quiz

        # letters are easier for user to put as option instead of manually typing it out where there is bigger probability of error
        alphabet = "abcdefghijklmnopqrstuvwxyz"

        print(f"{quiz.name}")
        print(f"Topic: {quiz.topic}\n")

        score = 0
        total = quiz.num_of_questions

        for i in range(0, quiz.num_of_questions):
            q = list(quiz.questions)[i]

            ops = quiz.questions[q]["options"]
            ans = quiz.questions[q]["answer"]
            # get the randomized list of options
            randomized_ops = []

            for op in ops:
                randomized_ops.append(op)

            # shuffle the random list
            random.shuffle(randomized_ops)

            choice = ""

            # output question and options
            print(f"{q}")

            i = 0

            for option in randomized_ops:
                letter = alphabet[i]
                print(f"\t{letter}. {option}")
                i += 1

            choice = input("Choice: ").lower()
            user_answers = []

            # get answers
            for letter in choice:
                if letter in alphabet[:len(randomized_ops)]:
                    # get index of letter
                    index = 0

                    for l in alphabet:
                        if l == letter:
                            break

                        index += 1

                    user_answers.append(randomized_ops[index])

            # check if the users given answers are correct
            if self.manager.check_correct(user_answers, ans):
                score += 1

                print("Correct! ")
            else:
                print("Better luck next time!")

            print("") # for newline

        print(f"Thanks for playing the quiz \"{quiz.name}\"! Your score: {score}/{total}.")

    # format a path with .qjson at the end to make it easy
    def format_path(self, name, directory=""):
        return f"{directory}/{name}.qjson" if directory != "" else f"{name}.qjson"

    def get_all_quizzes_from_user(self):
        self.quizzes = []

        while True:
            self.directory = input("Enter directory of quizzes: ")
            # given the directory name find the quizzes in that directory
            self.quizzes = self.manager.get_all_quizzes(self.directory)

            if self.quizzes != None and len(self.quizzes) > 0:
                break

            if self.quizzes == None:
                print("Quiz directory not found.")
            elif len(self.quizzes) == 0:
                print("Quiz directory empty.")

    def get_user_choice_of_quiz(self):
        quizzes = self.quizzes

        quiz_choice_int = -1
        quiz_choice_str = ""
        total_quizzes = len(quizzes)

        # show the user the quiz names and let them select from them
        print(f"Total quizzes: {total_quizzes}")

        for i in range(0, total_quizzes):
            print(f"{i + 1}.\t{quizzes[i]}")

        while quiz_choice_int < 1 or quiz_choice_int > total_quizzes:
            # reset to prevent infinite loop if quiz_choice_int <1 or >total_quizzes, else it will skip next while loop and infinite loop
            quiz_choice_str = ""

            while quiz_choice_str == "" or not quiz_choice_str.isdigit():
                quiz_choice_str = input("Enter choice of quiz: ")

            quiz_choice_int = int(quiz_choice_str)

        self.quiz_name = quizzes[quiz_choice_int - 1]

    # get raw JSON data given a name
    def get_quiz_data_from_name(self):
        path = self.format_path(self.quiz_name, directory=self.directory)
        self.quiz_data = self.manager.read_quiz(path)

    # get a runnable quiz itself given raw JSON
    def get_quiz_from_data(self):
        self.quiz = _quiz.Quiz()
        self.quiz.write_json(self.quiz_data)

    # function for user to create a quiz
    def create_quiz(self):
        # create an empty quiz to fill later
        quiz = _quiz.Quiz()
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        corresponding_indexes = {}

        # use dict to store indexes for letters instead of writing a for loop each time we need an index from a letter
        _index = 0
        for letter in alphabet:
            corresponding_indexes[letter] = _index
            _index += 1

        quiz.name = input("Enter quiz name: ")

        while True:
            q = input("Enter question (hit enter when empty when done adding options): ")
            # options[option_num] = option
            options = {}
            answers = []

            options_count = 0

            while True:
                # the letter we display to the user will be based on index
                letter = alphabet[options_count]
                option = input(f"{letter}. ")

                # if option is empty then assume no more options if number of options total is 2 or more
                if option == "" and options_count >= 2:
                    break
                elif option == "":
                    continue

                options[options_count] = option
                options_count += 1

            answer = ""

            while True:
                # now that the user has finished adding the options they need to select the correct one(s)
                answer = input("Answer (a=1,b=1,etc - multiple answers allowed): ")

                # 1 <= number of correct options <= number of options
                if len(answer) < 1 or len(answer) > options_count:
                    continue

                answers = list(answer)
                reset = False

                # make sure that the letters that signify which answers are correct are within proper boundaries
                # i.e., when we find indexes from the letters we shouldn't have out-of-bound letters
                for i in answers:
                    if i not in alphabet[:options_count]:
                        reset = True
                        break

                if reset:
                    continue
                break

            # get actual correct options from user input
            for letter in answer:
                index = corresponding_indexes[letter]

                if options[index] not in answers:
                    answers.append(options[index])

            # get all options as list
            _options = []
            for op in options:
                _options.append(options[op])

            quiz.add_question(q, _options, answers)

            cont = input("Add another question (q) or exit. ").lower()

            if cont != "q":
                break

        self.manager.save_quiz(quiz, f"quizzes/{quiz.name}.qjson")
