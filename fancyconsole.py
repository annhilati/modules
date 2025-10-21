from datetime import datetime
import textwrap

class Time():
    """
    A collection of functions that format a datetime or return the current

    #### Functions:
        date(): Returns a date in an european format
        time(): Returns a time in an european format
        clock(): Returns a time with second precision
    """
    @staticmethod
    def date(datetime: datetime) -> str:
        "Returns a date in an european format"
        return (datetime).strftime("%d.%m.%Y")

    @staticmethod
    def time(datetime: datetime) -> str:
        "Returns a time in an european format"
        return (datetime).strftime("%H:%M")
    
    @staticmethod
    def clock(datetime: datetime) -> str:
        "Returns a time in an european format including seconds"
        return (datetime).strftime("%H:%M:%S")

# class Color():
#     """
#     A collection of constants that change the following text color

#     #### Attributes:
#         red, orange, yellow, green, blue, aqua, magenta, purple, black, r
#             where r stands for reset
#     """
#     @staticmethod
#     def code_from_rgb(rgb: tuple[int, int, int], background: bool = False):
#         r, g, b = rgb
#         if background:
#             return f"\033[48;2;{r};{g};{b}m"
#         else:
#             return f"\033[38;2;{r};{g};{b}m"
        
#     red =       code_from_rgb((255, 0, 0))
#     orange =    code_from_rgb((255, 127, 0))
#     yellow =    code_from_rgb((255, 255, 0))
#     green =     code_from_rgb((0, 255, 0))
#     blue =      code_from_rgb((0, 0, 255))
#     cyan =      code_from_rgb((0, 255, 255))
#     magenta =   code_from_rgb((255, 0, 255))
#     purple =    code_from_rgb((127, 0, 255))
#     black =     code_from_rgb((0, 0, 0))
#     r = "\033[0m"  # Reset

#     def get(colorname: str = None) -> str:
#         if colorname is None:
#             return Color.r
#         return getattr(Color, colorname)

# def log(msg: str, color: str = None) -> None:
#     """
#     Logs a message to the console

#     #### Arguments:
#         msg (str): The text that should be printed
#         color (str): The color the text is to be displayed in
#             red, orange, yellow, green, blue, aqua, magenta, purple, black
#     """
#     cr = Color.get(None)
#     cc = Color.get(color)
#     print(f"[{Time.clock()}] " + cc + msg + cr)

import os

cols, rows = os.get_terminal_size()

CHAR_LIMIT = 65 if cols + 4 > 65 else cols - 4

class FancyConsole():
    """
    A collection of functions to print fancy console logs
    """

    @staticmethod
    def printhead(msg: str, first: bool = False) -> None:
        """
        Prints a fancy header to the console
        """
        # if len(msg) > CHAR_LIMIT:
        #     raise ValueError(f"Message should not be longer than {CHAR_LIMIT} characters")

        match first:
            case False:
                print(f"╔═╩" + CHAR_LIMIT * "═" + "╗")
            case True:
                print(f"╔══" + CHAR_LIMIT * "═" + "╗")
        for line in textwrap.wrap(msg, width=CHAR_LIMIT):
            print(f"║ {line + (CHAR_LIMIT + 1 - len(line)) * ' ' + '║'}")
        print(f"╚═╦" + CHAR_LIMIT * "═" + "╝")

    @staticmethod
    def print(msg: str) -> None:
        """
        Prints a fancy log to the console
        """

        print("  ║ " + msg)

    @staticmethod
    def printsegment(msg: str) -> None:#
        print("  ╠══ " + msg)
        
    # @staticmethod
    # def input(prompt: str,
    #           expectedtype: str = "any",
    #           promptcolor: str = None,
    #           errormsg: str = "Invalid Input. Try again",
    #           errorcolor: str = None):
    #     """
    #     Asks the user for an input until it matches the criteria

    #     #### Arguments:
    #         prompt (str): The message to be displayed when expecting an input
    #             - Does not need a trailing space
    #         expectedtype (str): One of `"any"`, `"str"`, `"int"`, `float`, ``
    #             - use `"any"` when having special criteria implemented specifically
    #         promptcolor (str): The color to display the prompt in
    #             - red, orange, yellow, green, blue, aqua, magenta, purple, black
    #         errormsg (str): The message to be displayed, if the user input does not meet the expected criteria
    #         errorcolor (str): The color to display the error message in
    #             - red, orange, yellow, green, blue, aqua, magenta, purple, black
    #     """
    #     while True:
    #         try:
    #             userInput = input(f"  ║ {Color.get(promptcolor)}{prompt}{Color.r} ")
            
    #             if expectedtype == "any" or "str":
    #                 return userInput
                
    #             elif expectedtype == "int":
    #                 try:
    #                     out = int(userInput)
    #                     return out
    #                 except:
    #                     raise Exception
                
    #             elif expectedtype == "float":
    #                 try:
    #                     out = float(userInput)
    #                     return out
    #                 except:
    #                     raise Exception
                    
    #         except Exception:
    #             print(f"  ║ {Color.get(errorcolor)}{errormsg}{Color.r}")