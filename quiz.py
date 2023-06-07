import json # to read/write file quiz data
import os # to find quiz files

class Quiz:
    def __init__(self):
        self.name = ""
        self.num_of_questions = 0
        self.topic = ""
        # questions will take format of:
        #   {
        #       "Question 1": {
        #           "options":{
        #               "Option A",
        #               "Option B",
        #               "Option C",
        #               "Option D"
        #           }
        #           "answer":["Option A"]
        #       }
        #   }
        self.questions = {}

    def get_question_by_index(self, index):
        if index > 0 and index < self.num_of_questions:
            return list(self.questions)[index]
        else:
            return None

    def get_index_for_question(self, question):
        try:
            ret = list(self.questions.keys()).index(question)
        except ValueError:
            return None

        return ret

    # options is a list, and answer is a list
    def add_question(self, question, options, answer):
        if not isinstance(question, str) or not isinstance(answer, list):
            return 1

        # make sure options is a list
        if not isinstance(options, list):
            print("A")
            return 1

        # make sure answer is length reasonable
        if len(answer) < 1 or len(answer) > 4:
            return 1

        # make sure question doesn't already exist
        if question in list(self.questions):
            return 1

        self.questions[question] = {
            "options":options,
            "answer":answer
        }

        self.num_of_questions += 1

        return 0

    def get_json(self):
        data = {}

        data["__NAME__"] = self.name
        data["__NUM__"] = self.num_of_questions
        data["__TOPIC__"] = self.topic

        questions = {}

        for index in range(0, self.num_of_questions):
            question = list(self.questions)[index]

            questions[question] = self.questions[question]

        data["__QUESTIONS__"] = questions

        return data

    def write_json(self, json_data):
        # reset data
        for index in range(0, self.num_of_questions):
            q = list(self.questions)[index]
            del self.questions[q]

        self.num_of_questions = 0

        # write new data
        self.name = json_data["__NAME__"]
        self.num_of_questions = json_data["__NUM__"]
        self.topic = json_data["__TOPIC__"]

        for index in range(0, self.num_of_questions):
            question = list(json_data["__QUESTIONS__"])[index]
            ops = json_data["__QUESTIONS__"][question]["options"]
            ans = json_data["__QUESTIONS__"][question]["answer"]

            self.add_question(question, ops, ans)
            self.num_of_questions -= 1

class QuizManager:
    def __init__(self):
        pass

    # save a quiz in a particular location
    def save_quiz(self, quiz, location):
        data = quiz.get_json()

        with open(location, 'w') as file:
            # first check to see if file available
            if not file:
                return None

            json.dump(data, file, indent=4)

        return 1

    # read a quiz given the location
    def read_quiz(self, location):
        with open(location, 'r') as file:
            if not file:
                return None

            data = json.load(file)

        return data

    # get all quizzes in a directory
    def get_all_quizzes(self, directory):
        _quizzes = []
        quizzes = []

        try:
            _quizzes = os.listdir(directory)
        except FileNotFoundError:
            return None

        for quiz_name in _quizzes:
            # qjson = quiz json, to distinguish it from other files
            if quiz_name.endswith("qjson"):
                # now remove qjson ending
                quiz_name = quiz_name[:-len(".qjson")]
                quizzes.append(quiz_name)

        return quizzes

    # get all quizzes along with topics
    def get_all_quizzes_topics(self, directory):
        _quizzes = []
        quizzes = []
        quizzes_with_topics = {}

        try:
            _quizzes = os.listdir(directory)
        except FileNotFoundError:
            return None

        for quiz_name in _quizzes:
            # qjson = quiz json, to distinguish it from other files
            if quiz_name.endswith("qjson"):
                # now remove qjson ending
                quiz_name = quiz_name[:-len(".qjson")]
                quizzes.append(quiz_name)

        for quiz in quizzes:
            # if the file is unreadable then just skip
            try:
                data = self.read_quiz(f"{directory}/{quiz}.qjson")
            except json.decoder.JSONDecodeError:
                continue

            if not data:
                continue

            _quiz = Quiz()
            _quiz.write_json(data)
            quizzes_with_topics[quiz] = _quiz.topic

        return quizzes_with_topics

    # both parameters are lists
    # this function makes sure they are identical
    def check_correct(self, user_choices, answers):
        for op in user_choices:
            if op not in answers:
                return False

        for op in answers:
            if op not in user_choices:
                return False

        return True

class Settings:
    @staticmethod
    def open_settings():
        try:
            file = open("settings", "r")
        except FileNotFoundError:
            print("Could not open settings file. ")
            return None

        data = json.loads(file.read())
        file.close()

        return data

    @staticmethod
    def save_settings(data):
        try:
            file = open("settings", "w")
        except FileNotFoundError:
            print("Could not open settings file.")
            return

        json.dump(data, file, indent=4)
        file.close()

    @staticmethod
    def save_data_param(param, new_info):
        data = Settings.open_settings()

        if param in data:
            data[param] = new_info
            Settings.save_settings(data)

    @staticmethod
    def get_data_param(param):
        data = Settings.open_settings()

        if param in data:
            return data[param]
        else:
            return None

    @staticmethod
    def toggle(options, settings_name):
        data = Settings.open_settings()

        # make sure the settings name is valid
        if settings_name not in data:
            return

        # make sure there are only two options, otherwise cannot "toggle"
        if len(data[settings_name]) != 2:
            return

        current = data[settings_name]

        # make sure the current value is valid, otherwise cannot "toggle"
        if current not in options:
            return

        # get current index
        index = 0

        for op in options:
            if current == op:
                break

            index += 1

        # set the data to the other option
        data[settings_name] = options[not index]

        # save data
        Settings.save_data(data)
