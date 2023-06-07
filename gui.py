import quiz as _quiz
import tkinter as tk
import tkinter.ttk as ttk
import sv_ttk
import darkdetect

class SettingsFrame(tk.Frame):
    def __init__(self, master, close_win, save_color):
        tk.Frame.__init__(self, master)

        self.settings = _quiz.Settings

        # display setting
        self.display_name = ttk.Label(self, text="Display")
        current_display = self.settings.get_data_param("display")
        self.display_selected = tk.StringVar(value=current_display)

        displays = ("gui", "cli")

        self.display_btns = []

        for display in displays:
            r = ttk.Radiobutton(self, text=display, value=display, variable=self.display_selected)
            self.display_btns.append(r)

        # set the radiobuttons to what is set in settings
        self.display_selected.set(current_display)

        # color mode setting
        self.color_name = ttk.Label(self, text="Color Mode")
        current_color = self.settings.get_data_param("display-color")
        self.color_selected = tk.StringVar(value=current_color)

        colors = ("light", "dark")

        self.color_btns = []

        for color in colors:
            r = ttk.Radiobutton(self, text=color, value=color, variable=self.color_selected)
            self.color_btns.append(r)

        # set the radiobuttons to what is set in settings
        self.color_selected.set(current_color)

        # buttons to close/save
        self._close_win = close_win
        self._save_win = save_color

        self.close_btn = ttk.Button(self, text="Close", command=self.close_win)
        self.save_btn = ttk.Button(self, text="Save", command=self.save_win, style='Accent.TButton')

        # display widgets
        names = [self.display_name, self.color_name]
        radiobtns = [self.display_btns, self.color_btns]

        row = 0
        index = 0

        # display the names of and the radiobuttons
        for btns in radiobtns:
            names[index].grid(row=row, column=0, padx=5, pady=5)

            # radiobuttons
            for btn in btns:
                btn.grid(row=row, column=1, padx=5, pady=5)
                row += 1

            # add a separator between widgets
            ttk.Separator(self, orient='horizontal').grid(row=row, column=0, columnspan=2)
            row += 1

            # increment index for each iteration of radiobuttons
            index += 1

        self.close_btn.grid(row=row, column=0, padx=5, pady=5)
        self.save_btn.grid(row=row, column=1, padx=5, pady=5)

    def close_win(self):
        self.pack_forget()
        self._close_win()

    def save_win(self):
        display = self.display_selected.get()
        color = self.color_selected.get()

        # save data to file
        self.settings.save_data_param("display", display)
        self.settings.save_data_param("display-color", color)

        self._save_win(color)
        self.close_win()

# first page user gets
# this page has buttons to run or create a quiz
class MainMenu(tk.Frame):
    # quizzes will be a dict with the quiz names and their topics
    def __init__(self, master, quizzes, go_create, submit_quiz, refresh, go_settings):
        tk.Frame.__init__(self, master)

        self.quizzes = quizzes
        self.columns = ("quiz_name", "topic")
        self.go_quiz = submit_quiz

        self.selected = None

        # set up a treeview for user to view quiz names and topics
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")

        self.tree.heading("quiz_name", text="Quiz Name")
        self.tree.heading("topic", text="Topic")

        for i in self.quizzes:
            quiz = (i, self.quizzes[i])
            self.tree.insert("", tk.END, values=quiz)

        self.tree.bind("<ButtonRelease-1>", self.item_selected_event)
        self.tree.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=4, sticky='ns')

        self.creator = ttk.Button(self, text="Create Quiz", command=go_create, style='Accent.TButton')
        self.submit = ttk.Button(self, text="Select Quiz", command=self.select_quiz, style='Accent.TButton')
        self.refresher = ttk.Button(self, text="Refresh", command=lambda: self.do_refresh(refresh))
        self.settings_btn = ttk.Button(self, text="Settings", command=go_settings)

        self.creator.grid(row=1, column=0, padx=5, pady=5)
        self.refresher.grid(row=1, column=1, padx=5, pady=5)
        self.settings_btn.grid(row=1, column=2, padx=5, pady=5)
        self.submit.grid(row=1, column=3, padx=5, pady=5)

    # when the user wants to run a quiz this function runs
    # and finds the selected quiz (if applicable) and runs it
    def select_quiz(self):
        focus = self.tree.focus()
        self.selected = self.tree.item(focus)['values'][0]

        if self.selected != None:
            self.go_quiz()

    # this exists for the tree bind
    def item_selected_event(event, useless_var):
        pass

    def do_refresh(self, get_refreshed):
        # get all new quizzes in case there are more
        self.quizzes = get_refreshed()

        # first delete all prior quizzes
        children = self.tree.get_children()

        for item in children:
            self.tree.delete(item)

        # now get the new ones
        for i in self.quizzes:
            quiz = (i, self.quizzes[i])
            self.tree.insert("", tk.END, values=quiz)

# page to ask user a question for a quiz they are running
class Question(tk.Frame):
    def __init__(self, master, question, options, answers, go_back, submit):
        tk.Frame.__init__(self, master)

        # save question, options, and answers as class variables
        self.question = question
        self.options = options
        self.answers = answers

        self._submit = submit # save the submit function so that we can first verify something was selected when submitting

        self.selected = {}
        self.tk_options = []

        for option in options:
            self.selected[option] = tk.IntVar()

        self.q_label = ttk.Label(self, text=self.question)
        self.q_label.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        # there are 4 rows for options
        self.option_row = 1

        for option in options:
            # a check button to let user select their choices (more than 1 answer possible)
            chkbtn = ttk.Checkbutton(self, text=f"{option}", variable=self.selected[option])
            chkbtn.grid(row=self.option_row, column=0, sticky='nsew', padx=5, pady=5)

            self.option_row += 1

            self.tk_options.append(chkbtn)

        # buttons to go back or forward
        self.back = ttk.Button(self, text="Back", command=lambda: go_back(self))
        self.submit = ttk.Button(self, text="Next", command=self.return_submit, style='Accent.TButton')

        self.back.grid(row=self.option_row, column=0, padx=5, pady=5, columnspan=2)
        self.submit.grid(row=self.option_row, column=2, padx=5, pady=5, columnspan=2)

    def get_selected(self):
        # used by GUI class to get what was selected to check answer to calculate user score
        selected = []

        for op in self.options:
            if self.selected[op].get() == 1:
                selected.append(op)

        return selected

    def return_submit(self):
        selected = self.get_selected()

        if len(selected) == 0:
            # possibly warn user to select choices
            return

        self._submit(self)

# page to tell user their score before going to main menu
class QuizEnd(tk.Frame):
    def __init__(self, master, score, total, go_home):
        tk.Frame.__init__(self, master)

        self.go_home = go_home

        # a label to tell user their score and button to return to main menu
        self.score_label = ttk.Label(self, text=f"Your score: {score}/{total}. ")
        self.home = ttk.Button(self, text="Main Menu", command=self.return_home)

        self.score_label.grid(row=0, column=0, padx=5, pady=5)
        self.home.grid(row=1, column=0, padx=5, pady=5)

    def return_home(self):
        self.pack_forget()
        self.go_home()

# page to ask user of name and topic of new quiz being created
class QuizCreateMain(tk.Frame):
    def __init__(self, master, go_back, go_next):
        tk.Frame.__init__(self, master)

        self.go_next = go_next

        # actually ask user for name and topic
        self.name_label = ttk.Label(self, text="Name: ")
        self.topic_label = ttk.Label(self, text="Topic: ")

        self.name = ttk.Entry(self)
        self.topic = ttk.Entry(self)

        # show it on the frame
        self.name_label.grid(row=0, column=0, padx=5, pady=5)
        self.topic_label.grid(row=1, column=0, padx=5, pady=5)
        self.name.grid(row=0, column=1, padx=5, pady=5)
        self.topic.grid(row=1, column=1, padx=5, pady=5)

        # either return home (and delete new quiz) or proceed in creating quiz
        self.return_home = ttk.Button(self, text="Main Menu", command=go_back)
        self.next = ttk.Button(self, text="Next", command=self.submit)

        self.return_home.grid(row=3, column=0, padx=5, pady=5)
        self.next.grid(row=3, column=1, padx=5, pady=5)

    def submit(self):
        # this function exists to verify there is at least a name of length 1+
        if len(self.name.get()) <= 0:
            return

        self.go_next(self)

# a frame to create a new question
class QuizCreateQuestion(tk.Frame):
    def __init__(self, master, go_back, go_next, finish_create, question_no):
        tk.Frame.__init__(self, master)

        self.options = {}
        self.correct = []
        self.chkbtns = []

        self.total_options = 2

        # create an IntVar to keep track of the options that are correct are selected
        for i in range(self.total_options):
            op = tk.IntVar()
            self.correct.append(op)

        # question_label and question are to ask user the question itself
        self.question_label = ttk.Label(self, text=f"Question {question_no}: ")
        self.question_label.grid(row=0, column=0, padx=5, pady=5)

        self.question = ttk.Entry(self)
        self.question.grid(row=0, column=1, padx=5, pady=5)

        self.chkbtn_row = 1

        # create checkbuttons and entry box for 4 options for the question
        for i in range(self.total_options):
            self.add_chkbtn(i)

        self.msg = ttk.Label(self, text="") # this is to tell user of failure if not successful

        # buttons to go back, next, or finish the creation of quiz
        self.back = ttk.Button(self, text="Back", command=lambda: go_back(self))
        self.next = ttk.Button(self, text="New Question", command=lambda: self.submit(go_next))
        self.finish = ttk.Button(self, text="Finish Quiz", command=lambda: self.submit(finish_create))

        # buttons to add/remove checkbuttons
        self.add_option_btn = ttk.Button(self, text="Add Option", command=self.add_option)
        self.remove_option_btn = ttk.Button(self, text="Remove Option", command=self.remove_option)

        self.grid_btns_and_msg()

    def remove_option(self):
        # first ensure there is no less than 3 options
        if self.total_options < 3:
            return

        num = self.total_options - 1
        self.remove_chkbtn(num)

    # remove last chkbtn
    # num is the index of which option to remove
    def remove_chkbtn(self, num):
        entry = self.options[num]
        chkbtn = self.chkbtns[num]

        self.correct.pop(num)

        entry.grid_remove()
        chkbtn.grid_remove()

        del self.options[num]
        self.chkbtns.pop(num)

        self.ungrid_btns_and_msg()
        self.chkbtn_row -= 1
        self.grid_btns_and_msg()

        self.total_options -= 1

    # add a new option
    def add_option(self):
        # remove the grid because we are inserting a new widget before them
        self.ungrid_btns_and_msg()
        self.add_chkbtn(self.total_options)

        self.total_options += 1

        self.grid_btns_and_msg()

    # add new widgets for new option
    # num is the number of options
    def add_chkbtn(self, num):
        self.correct.append(tk.IntVar())

        btn = ttk.Checkbutton(self, variable=self.correct[num])
        btn.grid(row=self.chkbtn_row, column=0, padx=5, pady=5)

        entry = ttk.Entry(self)
        entry.grid(row=self.chkbtn_row, column=1, padx=5, pady=5)

        self.options[num] = entry
        self.chkbtns.append(btn)

        self.chkbtn_row += 1

    def grid_btns_and_msg(self):
        # grid bottom widgets: message and btns
        self.msg.grid(row=self.chkbtn_row, column=0, columnspan=2, padx=5, pady=5)
        self.back.grid(row=self.chkbtn_row + 1, column=0, padx=5, pady=5)
        self.next.grid(row=self.chkbtn_row + 1, column=1, padx=5, pady=5)
        self.finish.grid(row=self.chkbtn_row + 1, column=2, padx=5, pady=5)

        self.add_option_btn.grid(row=self.chkbtn_row + 2, column=0, padx=5, pady=5)
        self.remove_option_btn.grid(row=self.chkbtn_row + 2, column=2, padx=5, pady=5)

    def ungrid_btns_and_msg(self):
        self.msg.grid_remove()
        self.back.grid_remove()
        self.next.grid_remove()
        self.finish.grid_remove()

        self.add_option_btn.grid_remove()
        self.remove_option_btn.grid_remove()

    def submit(self, func):
        # make sure the length of the question is at least one
        if len(self.question.get()) > 0:
            options_good = True

            # make sure the lengths of the possible options is bigger than 0
            for i in range(self.total_options):
                if len(self.options[i].get()) <= 0:
                    options_good = False

            # make sure at least one correct answer is selected
            correct_count = 0

            for i in range(self.total_options):
                if self.correct[i].get():
                    correct_count += 1

            if correct_count == 0:
                options_good = False

            if options_good:
                # if question creation successful move on (whether new question or finish)
                func(self)
            else:
                # if not tell user that
                self.msg.config(text="Finish question creation")
        else:
            self.msg.config(text="Finish question creation")

# a page after having created a quiz to inform user quiz was created
class QuizCreationEnd(tk.Frame):
    def __init__(self, master, msg, go_home):
        tk.Frame.__init__(self, master)

        self.go_home = go_home

        # a label to tell user a msg, success vs. failure
        self.msg = ttk.Label(self, text=msg)
        self.msg.grid(row=0, column=0, padx=0, pady=5)

        # a button to go to main menu
        self.home = ttk.Button(self, text="Main Menu", command=self.return_home)
        self.home.grid(row=1, column=0)

    def return_home(self):
        self.pack_forget()
        self.go_home()

# main window class
class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self) # initialize a new window

        self.title("Quiz Application")
        self.geometry("450x300")

        self.directory = "quizzes"
        self.manager = _quiz.QuizManager()

        # tk theme
        saved_theme = _quiz.Settings.get_data_param("display-color")
        self.valid_themes = ["light", "dark"]
        self.save_color(saved_theme)

        # quiz data
        self.quizzes = self.manager.get_all_quizzes_topics(self.directory)
        self.current_quiz = None
        self.quiz_frames = []
        self.current_frame = -1

        # widgets
        self.main_menu = MainMenu(self, self.quizzes, self.create, self.run_quiz, self.refresh, self.go_settings)
        self.quiz_creator = QuizCreateMain(self, self.go_home_from_creator, self.create_question)
        self.settings_frame = SettingsFrame(self, self.close_settings, self.save_color)

        self.main_menu.pack(expand="yes")

    def go_settings(self):
        # go to the settings frame
        self.main_menu.pack_forget()
        self.settings_frame.pack(expand="yes")

    def save_color(self, color):
        if color in self.valid_themes:
            sv_ttk.set_theme(color)
        else:
            # if settings data is invalid then use OS default
            os_theme = darkdetect.theme().lower()
            sv_ttk.set_theme(os_theme)

    def close_settings(self):
        self.main_menu.pack(expand="yes")

    # in case there is a new quiz (ex. a quiz was created and user returned to main menu)
    # get all quizzes in directory
    #
    # this function is used primarily by the main menu to refresh the quizzes shown to user
    def refresh(self):
        self.quizzes = self.manager.get_all_quizzes_topics(self.directory)
        return self.quizzes

    # go to first page of creating a new quiz
    # which asks for name and topic of quiz
    def create(self):
        self.main_menu.pack_forget()
        self.quiz_creator.pack(expand="yes")

    def go_home_from_creator(self):
        # empty the Entry widgets
        self.quiz_creator.name.delete(0, tk.END)
        self.quiz_creator.topic.delete(0, tk.END)

        # hide the creator menu and return home
        self.quiz_creator.pack_forget()
        self.main_menu.pack(expand="yes")

    # set up all the questions and let user iterate through questions
    def run_quiz(self):
        # get quiz data
        quiz_name = self.main_menu.selected
        data = self.manager.read_quiz(f"{self.directory}/{quiz_name}.qjson")

        # if data is nonexistent or unreadable we can't run so just stop here
        if data == None:
            return

        # if we can run it create a Quiz instance which will help us run
        quiz = _quiz.Quiz()
        quiz.write_json(data)

        self.current_quiz = quiz

        # reset the frames list in case it isn't empty
        self.quiz_frames = []

        # create a new question page for each question after getting question, options, and answers
        for question in quiz.questions:
            options = quiz.questions[question]["options"]
            answers = quiz.questions[question]["answer"]

            # finish adding back and submit
            frame = Question(self, question, options, answers, self.run_question_back, self.run_question_submit)
            self.quiz_frames.append(frame)

        self.main_menu.pack_forget()

        if len(self.quiz_frames) == 0:
            # if zero questions just end immediately
            self.run_question_submit(self.main_menu)
        else:
            first_frame = self.quiz_frames[0]
            first_frame.pack(expand="yes")

            self.current_frame = 0

    # given a frame find its index
    def find_frame_index(self, frame):
        z = 0

        for i in self.quiz_frames:
            if frame == i:
                return z

            z += 1

        return -1

    # return to the last frame
    def run_question_back(self, frame):
        index = self.find_frame_index(frame)

        if index == -1:
            # frame not found
            print("ERROR: frame index not found.")
        elif index == 0:
            # an index == 0 means this is first question
            self.current_quiz = None
            self.quiz_frames = []
            frame.pack_forget()

            # check whether we should return home (if user was running a quiz)
            # or we should return to the quiz creator main page (name + topic entries)
            if isinstance(frame, QuizCreateQuestion):
                self.quiz_creator.pack(expand="yes")
                self.current_frame = -1
            else:
                self.main_menu.pack(expand="yes")
                self.current_frame = 0
        else:
            # an index > 0 means that this wasn't the only question and we go back to another question
            back_frame = self.quiz_frames[index - 1]
            self.current_frame -= 1

            frame.pack_forget()
            back_frame.pack(expand="yes")

    # ran when user submits answer to question
    def run_question_submit(self, frame):
        # get index of quiz
        index = self.find_frame_index(frame)

        if index == (len(self.quiz_frames) - 1) or index == -1:
            # quiz finished
            score = 0
            total = self.current_quiz.num_of_questions

            for _frame in self.quiz_frames:
                user_selected = _frame.get_selected()
                answers = _frame.answers

                if self.manager.check_correct(user_selected, answers):
                    score += 1

            # the end-of-quiz page to let user know their score
            quiz_end = QuizEnd(self, score, total, self.go_home_from_end)

            # reset quiz class variables
            self.quiz = None
            self.quiz_frames = []

            frame.pack_forget()
            quiz_end.pack(expand="yes")

            self.current_frame = -1
        else:
            # next question
            next_frame = self.quiz_frames[index + 1]

            # check if the next frame is the last frame
            # and if it is tell the user that
            if (index + 1) == (len(self.quiz_frames) - 1):
                next_frame.submit.config(text="Finish")

            frame.pack_forget()
            next_frame.pack(expand="yes")

            self.current_frame += 1

    # show the main menu and refresh quizzes
    def go_home_from_end(self):
        self.main_menu.pack(expand="yes")
        self.main_menu.do_refresh(self.refresh)

    # create a new question
    def create_question(self, frame):
        # edit next/new-question button text in last frame
        if len(self.quiz_frames) > 0:
            last_frame = self.quiz_frames[len(self.quiz_frames) - 1]
            last_frame.next.config(text="Next")

        # create new question
        question = QuizCreateQuestion(self, self.run_question_back, self.next_or_new, self.quiz_creation_finish, len(self.quiz_frames) + 1)
        self.quiz_frames.append(question)

        # check to see which was the last frame
        # if it was the quiz creator main menu (name + topic), then hide that
        # otherwise it was another question and hide that
        if len(self.quiz_frames) == 1:
            # indicates this is first question
            self.quiz_creator.pack_forget()
            self.current_frame = 0
        else:
            _frame = self.quiz_frames[self.current_frame] # get the question that is currently shown to user
            _frame.pack_forget()
            self.current_frame += 1

        question.pack(expand="yes")

    # check to see if this is last frame (then create a new question) or not (then go the next frame that already exists)
    def next_or_new(self, frame):
        if self.current_frame == (len(self.quiz_frames) - 1):
            self.create_question(frame)
        else:
            self.current_frame += 1

            frame.pack_forget()
            self.quiz_frames[self.current_frame].pack(expand="yes")

    # finish creation of quiz
    def quiz_creation_finish(self, last_frame):
        total_options = 4

        # create a new quiz with data user provided
        quiz = _quiz.Quiz()

        quiz.name = self.quiz_creator.name.get()
        quiz.topic = self.quiz_creator.topic.get()

        msg = ""

        # add each question user submitted to the quiz
        for frame in self.quiz_frames:
            total_options = frame.total_options
            question = frame.question.get()
            _options = {}
            options = []
            answers = []

            # get options
            for op in range(total_options):
                _options[op] = frame.options[op].get()

            # get answers
            for op in range(total_options):
                if frame.correct[op].get():
                    answers.append(_options[op])

            # get options as a list
            for obj in _options:
                options.append(_options[obj])

            quiz.add_question(question, options, answers)

        # save quiz to hard drive here and inform user they successfully/failed to create(d) the quiz
        ret = self.manager.save_quiz(quiz, f"{self.directory}/{quiz.name}.qjson")

        if ret:
            msg = "Successfully saved!"
        else:
            msg = "Failed to save quiz."

        # create and go to the page that tells user whether quiz creation success/fail
        quiz_create_end = QuizCreationEnd(self, msg, self.go_home_from_end)

        last_frame.pack_forget()
        quiz_create_end.pack(expand="yes")
