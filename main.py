import quiz
import gui
import cli
import json
import sys

class Main:
    def __init__(self):
        self.settings = self.open_settings()
        display = self.settings["display"]

        if display not in ["cli", "gui"]:
            print("Settings file invalid. Display mode in settings file not 'cli' nor 'gui'. Exiting.")
            sys.exit()
        else:
            if display == "cli":
                self.open_cli()
            else:
                self.open_gui()

    def open_settings(self):
        # if we can open settings, we should
        try:
            file = open("settings", "r")
        except FileNotFoundError:
            print("Cannot open 'settings' file. Exiting.")
            sys.exit()

        # try to open JSON, otherwise invalid JSON
        try:
            settings = json.loads(file.read())
        except:
            print("Error: cannot load JSON. Exiting.")
            sys.exit()

        file.close()

        return settings

    def open_cli(self):
        interface = cli.CLI()

        while True:
            # see if the user wants to create a quiz - if so, then do so
            # if not, run a quiz
            choice = input("Do you want to create a quiz (c)?")

            if choice.lower() == "c":
                interface.create_quiz()

            interface.find_and_run_quiz()

            # ask the user if they want to quit (instead of having to Ctrl+C)
            exit = input("Do you want to exit? (y/n) ")

            if exit.lower() == "y":
                break

    def open_gui(self):
        gui.GUI().mainloop()

if __name__ == "__main__":
    Main()
