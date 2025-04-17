from os import system, name
def clear():
    if name != 'nt':
        system("clear")
    else:
        system("cls")
