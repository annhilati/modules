from datetime import datetime

class Time():
    """
    A collection of functions that format a datetime or return the current

    #### Functions:
        date(): Returns a date in an european format
        time(): Returns a time in an european format
        clock(): Returns a time with second precision
    """
    def date(datetime: datetime = datetime.now()) -> str:
        "Returns a date in an european format"
        return (datetime).strftime("%d.%m.%Y")

    def time(datetime: datetime = datetime.now()) -> str:
        "Returns a time in an european format"
        return (datetime).strftime("%H:%M")
    
    def clock(datetime: datetime = datetime.now()) -> str:
        "Returns a time in an european format"
        return (datetime).strftime("%H:%M:%S")

class Color():
    """
    A collection of constants that change the following text color

    #### Attributes:
        red, orange, yellow, green, blue, aqua, magenta, purple, black, r
            where r stands for reset
    """
    red = "\033[31m"
    orange = "\033[38;2;255;165;0m"
    yellow = "\033[33m"
    green = "\033[32m"
    blue = "\033[34m"
    aqua = "\033[36m"
    magenta = "\033[35m"
    purple = "\033[38;2;128;0;128m"  # Purple (Hex: #800080)
    black = "\033[30m"
    r = "\033[0m"  # Reset

    def get(colorname: str = None) -> str:
        match colorname:
            case None: return Color.r
            case "red": return Color.red
            case "orange": return Color.orange
            case "yellow":return Color.yellow
            case "green": return Color.green
            case "blue": return Color.blue
            case "aqua": return Color.aqua
            case "magenta": return Color.magenta
            case "purple": return Color.purple
            case "black": return Color.black            
            case _: raise SyntaxError(f"Unsupported color: {colorname}")

def log(msg: str, color: str = None) -> None:
    """
    Logs a message to the console

    #### Arguments:
        msg (str): The text that should be printed
        color (str): The color the text is to be displayed in
            red, orange, yellow, green, blue, aqua, magenta, purple, black
    """
    cr = Color.get(None)
    cc = Color.get(color)
    print(f"[{Time.clock()}] " + cc + msg + cr)

class FancyConsole():
    """
    A collection of functions to print fancy console logs

    #### Functions:
        printhead(): Prints a fancy header to the console
        print(): Prints a fancy log to the console
        input(): Asks the user for an input until it matches the criteria
    """

    def printhead(msg: str, first: bool = False) -> None:
        """
        Prints a fancy header to the console

        #### Arguments:
            msg (str): The text that should be displayed in the heading
                Shouldn't be too long so that the format looks good
            first (bool): Whether the heading is the first fancyconsole element after an empty line
        """
        match first:
            case False:
                print(f"╔═╩══════════════════════════════════════════════════════════════════")
                print(f"║ {msg}")
                print(f"╚═╦══════════════════════════════════════════════════════════════════")
            case True:
                print(f"╔════════════════════════════════════════════════════════════════════")
                print(f"║ {msg}")
                print(f"╚═╦══════════════════════════════════════════════════════════════════")

    def print(msg: str, color: str = None) -> None:
        """
        Prints a fancy log to the console

        #### Arguments:
            msg (str): The text that should be printed
                Shouldn't be too long so that the format looks good
            color (str): The color the text is to be displayed in
                red, orange, yellow, green, blue, aqua, magenta, purple, black
        """
        cr = Color.get(None)
        cc = Color.get(color)

        print("  ║ " + cc + msg + cr)

    def input(prompt: str,
              expectedtype: str = "any",
              promptcolor: str = None,
              errormsg: str = "Invalid Input. Try again",
              errorcolor: str = None):
        """
        Asks the user for an input until it matches the criteria

        #### Arguments:
            prompt (str): The message to be displayed when expecting an input
                - Does not need a trailing space
            expectedtype (str): One of `"any"`, `"str"`, `"int"`, `float`, ``
                - use `"any"` when having special criteria implemented specifically
            promptcolor (str): The color to display the prompt in
                - red, orange, yellow, green, blue, aqua, magenta, purple, black
            errormsg (str): The message to be displayed, if the user input does not meet the expected criteria
            errorcolor (str): The color to display the error message in
                - red, orange, yellow, green, blue, aqua, magenta, purple, black
        """
        while True:
            try:
                userInput = input(f"  ║ {Color.get(promptcolor)}{prompt}{Color.r} ")
            
                if expectedtype == "any" or "str":
                    return userInput
                
                elif expectedtype == "int":
                    try:
                        out = int(userInput)
                        return out
                    except:
                        raise Exception
                
                elif expectedtype == "float":
                    try:
                        out = float(userInput)
                        return out
                    except:
                        raise Exception
                    
            except Exception:
                print(f"  ║ {Color.get(errorcolor)}{errormsg}{Color.r}")