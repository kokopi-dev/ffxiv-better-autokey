#!/usr/bin/env python3
from utils.tty_colors import PrintColor as printc
from time import sleep


class FCCraft:
    @staticmethod
    def pilgram(proc, amt):
        printc.text("> Make sure that key 1 has a macro with /ta <f> in it.", "yel")
        start_sequence = [
            "1", "{VK_NUMPAD0}", "{VK_NUMPAD0}", "{VK_NUMPAD0}", "{DOWN}", "{VK_NUMPAD0}",
            "{UP}", "{VK_NUMPAD0}", "{VK_NUMPAD0}", "{LEFT}", "{VK_NUMPAD0}"
        ]
        submit_first_sequence = [
            "{VK_NUMPAD0}", "{VK_NUMPAD0}", "'", "{VK_NUMPAD0}", "{VK_NUMPAD0}",
            "{VK_NUMPAD0}"
        ]
        submit_after_sequence = [
            "{VK_NUMPAD0}", "'", "{VK_NUMPAD0}", "{VK_NUMPAD0}",
            "{VK_NUMPAD0}"
        ]
        collect_sequence = []

        count = 1
        while True:
            try:
                if amt and count > amt:
                    printc.text(">> Crafts finished.", "gre")
                    break

                for k in start_sequence:
                    print(f"> Pressing {k}")
                    proc.press_key(k)
                    sleep(1.5)

                # 3 submits, move down 4 times
                for x in range(4):
                    for i in range(3):
                        if x == 0 and i == 0:
                            for k in submit_first_sequence:
                                print(f"> Pressing {k}")
                                proc.press_key(k)
                                sleep(1.5)
                        else:
                            for k in submit_after_sequence:
                                print(f"> Pressing {k}")
                                proc.press_key(k)
                                sleep(1.5)

                    print("> Pressing {DOWN}")
                    proc.press_key("{DOWN}")
                    sleep(1.5)

                count += 1
            except KeyboardInterrupt:
                print("> Stopping fc craft")
                break

