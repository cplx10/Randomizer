#Randomizer v1.2.1/06 Feb 2024 | Made by cplx; 11 Dec 2021.

from keyword import iskeyword
import random
import os

validYes = ['yes','ye','y']
validNo = ['no','n']

errorInput = 'Error! Invalid input!'

def clearcmd():
    os.system('cls' if os.name == 'nt' else 'clear')

def Main():
    clearcmd()
    print('ATTENTION!\nEnter "x" below to stop the program.\n---')

    Events = []
    for x in range(9999):
        choiceEvent = input('Event '+str(x+1)+' >>> ')

        if choiceEvent == 'x': break
        else: Events.append(choiceEvent)

    if not Events:
        input('---\nYou must insert at least 1 event!\nPress enter to try again.'), Main()

    clearcmd()

    result = str(random.choices(Events))
    print('The chosen event is: '+result.strip("['']")+'.')

    choiceContD()

def choiceContD():
    choiceContinue = input('Would you like to close the program? [y/n] >>> ')

    if choiceContinue.lower() in validYes: input('---\nThank you for using the Randomizer! Made by cplx on 11 December 2021.\nPress enter to exit.'); exit()
    elif choiceContinue.lower() in validNo: clearcmd(); Main()
    else: print(errorInput); choiceContD()

def startCode():
    start = input('\nStart program? [y/n] >>> ')

    if start in validYes: Main()
    elif start in validNo: choiceContD()
    else: print(errorInput), startCode()

print('Welcome to the Randomizer v1.2.1!\nThis program lets you input a (near) infinite number of events into an algorith which randomly chooses one of them.')
startCode()