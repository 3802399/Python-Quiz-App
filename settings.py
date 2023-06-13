import quiz

# settings app for command-line
class SettingsApp:
    def __init__(self):
        print("Settings App\n")
        self.change_display()
        self.change_display_color()

    # given several acceptable options, the user has to choose between them and this function saves it to settings
    def change_toggle(self, acceptable_inputs, input_str, param):
        print("-----------------------------\n")

        user_input = " "
        acceptable_inputs.append("")

        while user_input not in acceptable_inputs:
            user_input = input(input_str).lower()

        if user_input != "":
            quiz.Settings.save_data_param(param, user_input)

        print()

    def change_display(self):
        acceptable_inputs = ["cli", "gui"]
        self.change_toggle(acceptable_inputs, "Enter display mode (cli/gui): ", "display")

    def change_display_color(self):
        self.change_toggle(["light", "dark"], "Enter color of GUI (light/dark): ", "display-color")

if __name__ == "__main__":
    SettingsApp()
