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
        """ Checks user input's format, returns format if ok
            Timer must be pos int, macros must be in acceptedHotkeys
            Loops input() until correct format is given
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
            print("Please re-enter in the correct format:")
            user_input = input()
            try:
                temp_timer = int(user_input[3:])
                while user_input[:2] not in acceptedHotkeys:
                    print("\nAccepted key edits are the following:")
                    print(' '.join(map(str, acceptedHotkeys)) + '\n')
                while not temp_timer in range(0, 301):
                    print("  ... Wrong timer range, must be between 0-300.")
                int_lock += 1
            except ValueError:
                print("  ... Wrong timer data type.\n  ... Format example: m1 35\n")

        return user_input

    def keystroke_checker(user_input):
        """ Checks user input's format, returns format if ok
            Keys must be in acceptedKeys
            Key placement must be in acceptedKeyplace
            Loops input() until correct format is given
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

    def processname_checker(user_input):
        """ Checks json file's process_name's format
            Makes sure it is an .exe
            Loops input() until correct format is given
        """

        pformat = ".exe"

        while pformat not in user_input:
            print("Please try again. Input must end with '.exe'")
            user_input = input()

        return user_input

    def autobuff_checker(user_input):
        """ Checks user input's format, returns format if ok
            Food timer must be between 3 and 60
            Pot timer must be between 3 and 15
            Loops input() until correct format is given
        """

        food_lock = 0
        pot_lock = 0

        try:
            temp_food = int(user_input[0])
            if not temp_food in range(3, 61):
                raise ValueError
        except ValueError:
            food_lock += 1
            pass

        try:
            temp_pot = int(user_input[1])
            if not temp_pot in range(3, 16):
                raise ValueError
        except ValueError:
            pot_lock += 1
            pass

        while food_lock == 1:
            try:
                food_input = input("Food format or timer range is incorrect. Please try again:\n")
                temp_food = int(food_input)
                while not temp_food in range(3, 61):
                    print("  ... Food buff timer needs to be between 3 to 60.\n")
                food_lock += 1
            except ValueError:
                print("  ... Food buff timer must be an integer.\n")

        while pot_lock == 1:
            try:
                pot_input = input("Pot format or timer range is incorrect. Please try again:\n")
                temp_pot = int(pot_input)
                while not temp_pot in range(3, 16):
                    print("  ... Pot buff timer needs to be between 3 to 15.\n")
                pot_lock += 1
            except ValueError:
                print("  ... Pot buff timer must be an integer.\n")

        user_input[0] = int(temp_food)
        user_input[1] = int(temp_pot)

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
