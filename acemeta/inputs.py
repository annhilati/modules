def inputInt(prompt: str, errormsg: str = None) -> int:
    while True:
        userInput = input(prompt)
        try:
            return int(userInput)
        except:
            if errormsg:
                print(errormsg)

def inputFloat(prompt: str, errormsg: str = None) -> float:
    while True:
        userInput = input(prompt)
        try:
            return float(userInput)
        except:
            if errormsg:
                print(errormsg)

def inputYN(prompt: str, errormsg: str = None) -> bool:
    allowedChar = "ynYN"
    while True:
        userInput = input(prompt)
        if len(userInput) == 1 and all(char in allowedChar for char in userInput):
            if userInput in "yY":
                return True
            else:
                return False
        else:
            if errormsg:
                print(errormsg)