import quiz as _quiz

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

        alphabet = "abcdefghijklmnopqrstuvwxyz"

        print(f"{quiz.name}")
        print(f"Topic: {quiz.topic}\n")

        score = 0
        total = quiz.num_of_questions

        for i in range(0, quiz.num_of_questions):
            q = list(quiz.questions)[i]

            ops = quiz.questions[q]["options"]
            ans = quiz.questions[q]["answer"]

            choice = ""

            # output question and options
            print(f"{q}")

            i = 0

            for option in ops:
                letter = alphabet[i]
                print(f"\t{letter}. {option}")
                i += 1

            choice = input("Choice: ").lower()
            user_answers = []

            # get answers
            for letter in choice:
                if letter in alphabet[:len(ops)]:
                    # get index of letter
                    index = 0

                    for l in alphabet:
                        if l == letter:
                            break

                        index += 1

                    user_answers.append(ops[index])

            if self.manager.check_correct(user_answers, ans):
                score += 1

                print("Correct! ")
            else:
                print("Better luck next time!")

            print("") # for newline

        print(f"Thanks for playing the quiz \"{quiz.name}\"! Your score: {score}/{total}.")

    def format_path(self, name, directory=""):
        return f"{directory}/{name}.qjson" if directory != "" else f"{name}.qjson"

    def get_all_quizzes_from_user(self):
        self.quizzes = []

        while True:
            self.directory = input("Enter directory of quizzes: ")
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

    def get_quiz_data_from_name(self):
        path = self.format_path(self.quiz_name, directory=self.directory)
        self.quiz_data = self.manager.read_quiz(path)

    def get_quiz_from_data(self):
        self.quiz = _quiz.Quiz()
        self.quiz.write_json(self.quiz_data)

    def create_quiz(self):
        quiz = _quiz.Quiz()
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        corresponding_indexes = {}

        _index = 0
        for letter in alphabet:
            corresponding_indexes[letter] = _index
            _index += 1

        quiz.name = input("Enter quiz name: ")

        while True:
            q = input("Enter question (hit enter when empty when done adding options): ")
            options = {}
            answers = []

            options_count = 0

            while True:
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
                answer = input("Answer (a=1,b=1,etc - multiple answers allowed): ")

                if len(answer) < 1 or len(answer) > options_count:
                    continue

                answers = list(answer)
                reset = False

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
