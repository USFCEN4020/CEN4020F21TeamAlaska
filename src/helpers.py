# maxNumber is the highest menu item
def validateMenuInput(maxNumber: int) -> int:
    while(True):
        try:
            c = int(input(""))
            if(c in range(0, maxNumber + 1)):
                return c
            else:
                print(
                    "Please try again with an integer between 0 and {}".format(maxNumber))
        except:
            print("Please try again, Enter a valid integer.")
