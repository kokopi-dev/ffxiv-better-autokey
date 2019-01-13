"""
format_checker contains a class with functions to help
check data types and input formats
"""
import sys

class FormatCheck:
    """ FormatCheck
        user_input is from input(), locked to type string
    """
    def __init__(self):
        self.user_input = user_input

    def timer_format(user_input):
        """ Checks user input's format, returns if format is ok
            Timer must be pos int, macros must be in acceptedHotkeys
        """

        acceptedHotkeys = ["m1", "m2", "m3", "m4"]
        int_lock = 0
        try:
            temp_timer = int(user_input[3:])
            if temp_timer < 0:
                raise ValueError
        except ValueError:
            int_lock += 1

        while int_lock == 1:
            print("Wrong timer data type.\nFormat example: m1 35\n")
            user_input = input()
            try:
                temp_timer = int(user_input[3:])
                while user_input[:2] not in acceptedHotkeys:
                    print("\nAccepted key edits are the following:")
                    print(' '.join(map(str, acceptedHotkeys)) + '\n')
                    user_input = input()
                while not temp_timer in range(0, 301):
                    print("Wrong timer range, must be between 0-300.")
                    user_input = input()
                int_lock += 1
            except ValueError:
                print("Wrong timer data type.\nFormat example: m1 35\n")

        return user_input

    def keystroke_checker(user_input):
        """ Checks user input's format, returns if format is ok
            Keys must be in acceptedKeys
            Key placement must be in acceptedKeyplace
        """
        
        acceptedKeys = ["1", "2", "3", "4", "5", "6", "7",
                        "8", "9", "0", "-", "="]
        acceptedKeyplace = ["k1", "k2", "k3", "k4", "k5"]

        while not (user_input[:2] in acceptedKeyplace and user_input[3:]
            in acceptedKeys and user_input[2] == ' '):
            print("Keystroke and or hotkey not accepted. Format example: k1 1")
            print("\nAccepted key edits are the following:\n")
            print(' '.join(map(str, acceptedKeys)) + '\n')
            user_input = input()

        return user_input

    def input_splitter(user_input):
        """ Splits the user input into two vars and returns them in a list
        """

        temp_list = []
        try:
            mtime = int(user_input[3:])
            m = user_input[:2]
        except:
            print("Wrong format.\nFormat example: m1 35")
            sys.exit()

        temp_list.extend((mtime, m))
        return temp_list
