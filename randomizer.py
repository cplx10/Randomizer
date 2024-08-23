# Randomizer v2.0.0/xx Aug 2024 | Made by cplx; 11 Dec 2021.
#
# [~ INFORMATION REGARDING SCRIPT ~]
#
# In short, what this program does depends on the functionality you choose:
# ~ 1. the Randomizer picks a random event from a list you input and returns it;
# ~ 2. Roll a Die! rolls a die, like a d6 or a d20;
#
# The program features a translation feature making use of dictionaries that
# imports the variables in the chosen language. All functions besides Lang()
# take in the dictionary, stored in the messages_response variable, as arguments.
# 
# I plan on using JSON dictionaries in the future to clean up code and reduce
# the file's size. Furthermore, adding "save states" would be very interesting
# to make choosing random events from a permanent list easier and simpler, the
# same applies to Roll a Die!
# 
# Either way, I really hope you enjoy!
# 
# ~ cplx

from time import sleep
from json import dump as jdump, load as jload
from inquirer import list_input
from random import choice as rchoice
from getpass import getpass
from os import system, name as sysname
from enum import Enum, auto
from datetime import datetime

version = '2.0.0' # program version

#

groups = ['type', 'name', 'info'] # important for presets

#

def clearcmd(): # clear terminal
    system('cls' if sysname == 'nt' else 'clear') # types "cls" on terminal if running on Windows, otherwise "clear" 

#

class Languages(Enum): # setting up english and portuguese texts in a dictionary
    EN = auto()
    PT = auto()

#

class Main:

    def set_language(language: Languages) -> dict:
        message_response = {}
        match language:
            case Languages.EN:
                with open('data/languages/english.json') as f:
                    message_response = jload(f)

            case Languages.PT:
                with open('data/languages/portuguese.json') as f:
                    message_response = jload(f)
        
        return message_response

    #

    def Lang(): # change language
           
        while True:
            clearcmd()

            # selection menu
            language = list_input('Choose a language',
                                choices=[('English', Languages.EN), ('Português', Languages.PT)],
                                )
            
            # adopts chosen language
            message_response = Main.set_language(language)
            Main.Menu(message_response, language)

    #

    def Menu(message_response, language): # the main menu

        # importing variables: main messages
        textMenuWelcome  = message_response.get("textMenuWelcome")
        textMenuNew      = message_response.get("textMenuNew")
        textMenuAbout    = message_response.get("textMenuAbout")
        
        # importing variables: option texts
        textMenuOptionRandomizer = message_response.get("textMenuOptionRandomizer")
        textMenuOptionDice       = message_response.get("textMenuOptionDice")
        textMenuOptionNew        = message_response.get("textMenuOptionNew")
        textMenuOptionAbout      = message_response.get("textMenuOptionAbout")
        textMenuOptionLanguage   = message_response.get("textMenuOptionLanguage")

        # importing variables: generics
        genericChooseAction = message_response.get("genericChooseAction")
        genericChooseExit   = message_response.get("genericChooseExit")
        genericEnterBack    = message_response.get("genericEnterBack")

        # this will keep running until the function is called again
        while True:
            clearcmd()

            print(textMenuWelcome+version+'!\n')

            start = list_input(genericChooseAction,
                            choices=[(textMenuOptionRandomizer, '1'), (textMenuOptionDice, '2'), (textMenuOptionNew, '3'),
                                        (textMenuOptionAbout, 'a'), (textMenuOptionLanguage, 'l'), (genericChooseExit, 'x')],
                            )

            match start:
                case '1': Randomizer.Main(message_response)     # run the Randomizer
                case '2': Main.DiceMenu(message_response)       # run Roll a Die!
                case '3':                                       # what's new in the program
                    clearcmd(), print(textMenuNew)
                    getpass(genericEnterBack)
                case 'a':                                       # about the program
                    clearcmd(), print(textMenuAbout)
                    getpass(genericEnterBack)
                case 'l': break                                 # switch languages
                case 'x': Main.choiceContinue(message_response) # exit
    
    #
    
    def choiceContinue(message_response): # exit the program
        clearcmd()

        # importing variables: exit texts
        textExitChoice   = message_response.get("textExitChoice")
        textExitThank    = message_response.get("textExitThank")

        # importing variables: header and generics
        headerRandomizer = message_response.get("headerRandomizer")
        genericYes       = message_response.get("genericYes")
        genericNo        = message_response.get("genericNo")

        print(headerRandomizer)

        # selection menu
        promptContinue = list_input(textExitChoice,
                                    choices=[(genericYes,'y'),(genericNo,'n')],
                                    )

        if promptContinue == 'y': # close if 'y' is chosen (getpass is used to hide user input)
            getpass(textExitThank), exit()

    #

    def DiceMenu(message_response): # main menu for Roll a Die!
        while True:
        
            clearcmd()

            # importing variables: welcome message
            textDiceMenuWelcome = message_response.get("textDiceMenuWelcome")

            # importing variables: selection menu (generics)
            genericChooseAction = message_response.get("genericChooseAction")
            genericChooseExit   = message_response.get("genericChooseExit")

            # importing variables: selection menu
            textDiceMenuOptionRoll   = message_response.get("textDiceMenuOptionRoll")
            textDiceMenuOptionPreset = message_response.get("textDiceMenuOptionPreset")
            textDiceMenuOptionReturn = message_response.get("textDiceMenuOptionReturn")
            
            
            print(textDiceMenuWelcome,'\n')
            
            # selection menu
            choicestart = list_input(genericChooseAction,
                                choices=[(textDiceMenuOptionRoll, '1'),(textDiceMenuOptionPreset, '2'),
                                         (textDiceMenuOptionReturn, '3'),(genericChooseExit,'x')]
                                )

            match choicestart:
                case '1': RollDice.Dice(message_response)                 # runs Roll a Die!
                case '2': RollDice.PresetDice(message_response)           # manage presets
                case '3': return                                          # returns to main menu
                case 'x': Main.choiceContinue(message_response)           # exits the program

#

class Randomizer:

    def Main(message_response): # the Randomizer
        
        repeat = True

        while repeat is True:
            clearcmd()

            # importing variables: header
            headerRandomizer = message_response.get("headerRandomizer")

            # importing variables: texts
            textRandomizerAttention = message_response.get("textRandomizerAttention")
            textRandomizerEvent     = message_response.get("textRandomizerEvent")

            # importing variables: error messages
            errorRandomizerNoEvent = message_response.get("errorRandomizerNoEvent")
            errorInvalidInput      = message_response.get("errorInvalidInput")

            go = 1

            print(headerRandomizer,textRandomizerAttention)

            Events = []

            while True: # events input
                choiceEvent = input(f' > {textRandomizerEvent} {go}: ').strip()

                if not choiceEvent: print(errorInvalidInput) # if choiceEvent has no content
                elif choiceEvent == 'x': break               # if choiceEvent is 'x'
                else:
                    go += 1
                    Events.append(choiceEvent)               # adds event to Events list

            if not Events:                                   # if the events list is empty
                getpass(errorRandomizerNoEvent)
                continue

            repeat = Randomizer.choiceCheck(message_response, Events, headerRandomizer)

    #

    def choiceCheck(message_response, Events, headerRandomizer): # checks the events chosen
        clearcmd()

        # importing variables: information texts
        textRandomizerEventsChosen  = message_response.get("textRandomizerEventsChosen")
        textRandomizerEventsLeft    = message_response.get("textRandomizerEventsLeft")
        textRandomizerEventsWarning = message_response.get("textRandomizerEventsWarning")

        # importing variables: generics
        genericChooseAction = message_response.get("genericChooseAction")
        genericChooseExit   = message_response.get("genericChooseExit")
        genericChooseReturn = message_response.get("genericChooseReturn")

        # importing variables: list_inputs
        textRandomizerOptionRerun1  = message_response.get("textRandomizerOptionRerun1")
        textRandomizerOptionRerun2  = message_response.get("textRandomizerOptionRerun2")
        textRandomizerOptionInsert  = message_response.get("textRandomizerOptionInsert")

        print(headerRandomizer)

        while len(Events) > 1:                                           # events available + event picked + events left
            result = str(rchoice(Events)).strip("[']")                   # picks a random event and formats to remove [] and ''
            Events.remove(result)
            evleft = str(Events).translate(str.maketrans('', '', "[']")) # formats events list to remove [] and ''

            print(f'{textRandomizerEventsChosen}: {result}.\n{textRandomizerEventsLeft}: {evleft}.\n') # The chosen event is: {result}. Your events left: {evleft}.

            if len(Events) == 1:
                break
            
            rerun = list_input(genericChooseAction,
                               choices=[(f'{textRandomizerOptionRerun1}{len(Events)}{textRandomizerOptionRerun2}', '1'),
                                        (textRandomizerOptionInsert, '2'), (genericChooseReturn, '3'), (genericChooseExit, 'x')],
                              )
            
            match rerun:
                case '1':                                       # re-runs
                    print(' #---#---#---#---#\n')
                    continue
                case '2': return True                           # inputs new events
                case '3': return False                          # retuns to menu
                case 'x':                                       # exits
                    Main.choiceContinue(message_response)
                    return False

        # choices once there's only one event left
        evleft = str(Events).translate(str.maketrans('', '', "[']"))
        
        print(f'{textRandomizerEventsWarning} ({evleft})') # You only have one event left! ({evleft})

        # selection menu
        choiceEvent = list_input(genericChooseAction,
                                 choices=[(textRandomizerOptionInsert, '1'),(genericChooseReturn,'2'),(genericChooseExit,'x')],
                                )
            
        match choiceEvent:
            case '1': return True                           # inputs new events
            case '2': return False                          # returns to menu
            case 'x':                                       # exits
                Main.choiceContinue(message_response)
                return False

#

class RollDice:

    def Dice(message_response): # runs Roll a Die!

        # importing variables: header and main text
        headerDice       = message_response.get("headerDice")
        textDiceRollType = message_response.get("textDiceRollType")

        # importing variables: error messages
        errorInvalidInput = message_response.get("errorInvalidInput")
        errorUnknown      = message_response.get("errorUnknown")
        
        repeat = True

        # asks you to type in a die, displaying an error message if something goes wrong
        while repeat is True:

            clearcmd()
            print(headerDice)

            try:
                dice = int(input(textDiceRollType))
                print('\n')

            except ValueError:
                print(errorInvalidInput, '\n'), sleep(1.5)
                continue

            except Exception as e:
                print(f'{errorUnknown}{e}\n'), sleep(1.5)
                continue



            if not dice or dice <= 1: # in case user doesn't input any numbers, or if its less than 1
                print(errorInvalidInput,'\n'), sleep(1.5)
                continue

            repeat = RollDice.Roll(message_response, headerDice, dice)

    #
    
    def Roll(message_response, headerDice, dice): # (re)rolls the die
        
        # importing variables: text information
        textDiceRoll       = message_response.get("textDiceRoll")
        textDiceRollResult = message_response.get("textDiceRollResult")

        # importing variables: generics
        genericChooseAction = message_response.get("genericChooseAction")
        genericChooseExit   = message_response.get("genericChooseExit")
        genericChooseReturn = message_response.get("genericChooseReturn")

        # importing variables: list_input options
        textDiceOptionReroll  = message_response.get("textDiceOptionReroll")
        textDiceOptionAnother = message_response.get("textDiceOptionAnother")

        while True:

            clearcmd()
            result = str(rchoice(range(1,(dice+1)))) # picks a random number between 1 and the one you chose and transforms it into a string

            print(f'{headerDice}\n{textDiceRoll}{dice}.\n{textDiceRollResult}: {result}.\n') # You rolled a d{dice}. Your result was: {result}.
            
            # selection menu
            re = list_input(genericChooseAction,
                            choices=[(textDiceOptionReroll, '1'),(textDiceOptionAnother, '2'),(genericChooseReturn, '3'),
                                     (genericChooseExit,'x')],
                           )
            match re:
                case '1': continue                                  # re-rolls die
                case '2': return True                               # rolls another die
                case '3': return False                              # returns to menu
                case 'x':                                           # exits the program
                    Main.choiceContinue(message_response)
                    return False

    # 

    def PresetDice(message_response): # options about presets, namely create, load, edit and delete presets
        
        # importing variables: generics
        genericChooseAction = message_response.get("genericChooseAction")
        genericChooseReturn = message_response.get("genericChooseReturn")

        # importing variables: list_input options
        genericPresetOptionNew    = message_response.get("genericPresetOptionNew")
        genericPresetOptionLoad   = message_response.get("genericPresetOptionLoad")
        genericPresetOptionEdit   = message_response.get("genericPresetOptionEdit")
        genericPresetOptionDelete = message_response.get("genericPresetOptionDelete")

        clearcmd()

        presets = PresetActions()

        savechoice = list_input(genericChooseAction,
                                choices=[(genericPresetOptionNew,'create'),
                                        (genericPresetOptionLoad,'load'), (genericPresetOptionEdit, 'edit'),
                                        (genericPresetOptionDelete,'delete'), (genericChooseReturn, 'x')],
                            )
         
        match savechoice:

            case 'create': # create a new dice preset

                # importing variables: error messages
                errorInvalidInput = message_response.get("errorInvalidInput")
                errorUnknown      = message_response.get("errorUnknown")

                # importing variables: preset texts
                textPresetDiceNewType = message_response.get("textPresetDiceNewType")
                genericPresetNewName  = message_response.get("genericPresetNewName")

                preset_dice = []

                clearcmd()
                print(textPresetDiceNewType)

                while True:
                    
                    input_dice = input(' >>> d')
                    if input_dice == 'x': break

                    try:
                        input_dice = int(input_dice)
                    except ValueError:
                        print(errorInvalidInput, '\n'), sleep(1.5)
                        continue

                    except Exception as e:
                        print(f'{errorUnknown}{e}\n'), sleep(1.5)
                        continue



                    if not input_dice or input_dice <= 1: # in case the user doesn't input any numbers, or if it's less than 1
                        print(errorInvalidInput,'\n'), sleep(1.5)
                        continue

                    preset_dice.append(input_dice)
                
                preset_name = input(genericPresetNewName)
                
                presets.CreatePreset(message_response, 'dice', preset_name, preset_dice)
            
            case 'load': # load a dice preset

                presets.LoadDicePreset(message_response)

            case 'edit': # edit a dice preset
                
                print('Work in progress!')
                None
            
            case 'delete': # delete a dice preset
                presets.DeletePreset(message_response, 'dice')
            
            case 'x': return
        
        presets.UpdatePresets() # update preset list

#

class PresetActions:

    def __init__(self):
        
        self.presets = []

        with open('data/presets.json') as file:
            preset_load = jload(file)
        
        for i in range(len(preset_load)):
            a = []
            self.presets.append(a)
            for j in groups:
                a.append(preset_load[i][j])

    #

    def CreatePreset(self, message_response, preset_type, name, info): # creates a preset
        
        # importing variables: text information
        genericPresetNewCreate   = message_response.get("genericPresetNewCreate")
        genericPresetNewComplete = message_response.get("genericPresetNewComplete")
        
        print(genericPresetNewCreate)

        self.presets.append((preset_type, name, info))
       
        # updates the presets list with the following contents:
        # 
        # - the type of the preset ('rand' or 'dice');
        # - the name of the preset;
        # - the information stored (either the dice to be used or the events chosen).

        print(genericPresetNewComplete)

        sleep(2)

    #

    def LoadDicePreset(self, message_response): # loads a dice preset, as there are specifics differing from Randomizer presets
        
        # importing variables
        textPresetDiceLoadNote = message_response.get("textPresetDiceLoadNote")
        genericChoosePreset    = message_response.get("genericChoosePreset")

        clearcmd()
        
        print(textPresetDiceLoadNote)
        preset_list = []
        preset_name_lst = set()

        for block in self.presets:
            if block[0] == 'dice':
                preset_list.append(block)
        
        for block in preset_list:
            preset_name_lst.add(block[1])
        
        preset_name_lst = list(preset_name_lst)
        preset_name_lst.sort()

        choose_preset_name = list_input(genericChoosePreset, choices=preset_name_lst)

        for block in self.presets:
            if block[1] == choose_preset_name:
                PresetActions.RollDicePreset(message_response, block[2])
                return
    
    #

    def RollDicePreset(message_response, dice): # rolls the dice loaded from the preset
        
        # importing variables: header and main text
        headerDice              = message_response.get("headerDice")
        textPresetDiceLoadStart = message_response.get("textPresetDiceLoadStart")

        # importing variables: text information & list_input option #1
        textDiceRoll            = message_response.get("textDiceRoll")
        textDiceRollResult      = message_response.get("textDiceRollResult")
        textDiceOptionReroll    = message_response.get("textDiceOptionReroll")
        textPresetDiceLoadTotal = message_response.get("textPresetDiceLoadTotal")

        # importing variables: generics
        genericChooseAction = message_response.get("genericChooseAction")
        genericChooseReturn  = message_response.get("genericChooseReturn")
        
        while True:

            clearcmd()
            print(f'{headerDice}\n{textPresetDiceLoadStart}\n')
            sleep(1)

            dice_sum = 0

            for die in dice:
                sleep(1)

                result = str(rchoice(range(1,(die+1)))) # picks a random number between 1 and the one you chose and transforms it into a string
                print(f'{textDiceRoll}{die}.\n{textDiceRollResult}: {result}.\n') # You rolled a d{dice}. Your result was: {result}.

                dice_sum += int(result)

            sleep(0.5)
            print(f' > {textPresetDiceLoadTotal}: {dice_sum}\n')
            sleep(0.5)

            re = list_input(genericChooseAction,
                            choices=[(textDiceOptionReroll, '1'),(genericChooseReturn, '2')],
                            )
        
            match re:
                case '1': continue # re-rolls die                
                case '2': break    # returns to menu

    #

    def LoadRandomizerPreset(self, message_response):
        
        print('Work in progress!')

        # importing variables
        textPresetRandomizerLoadNote = message_response.get("textPresetRandomizerLoadNote")
        genericChoosePreset          = message_response.get("genericChoosePreset")

        clearcmd()
        
        print(textPresetRandomizerLoadNote)
        preset_list = []
        preset_name_lst = set()

        for block in self.presets:
            if block[0] == 'rand':
                preset_list.append(block)
        
        for block in preset_list:
            preset_name_lst.add(block[1])
        
        preset_name_lst = list(preset_name_lst)
        preset_name_lst.sort()

        choose_preset_name = list_input(genericChoosePreset, choices=preset_name_lst)

        for block in self.presets:
            if block[1] == choose_preset_name:
                PresetActions.RunRandomizerPreset(message_response, block[2])
                return

        return 0

    #

    def RunRandomizerPreset(self, message_response, Events):

        # importing variables: header and information texts
        headerRandomizer            = message_response.get("headerRandomizer")
        textRandomizerEventsChosen  = message_response.get("textRandomizerEventsChosen")
        textRandomizerEventsLeft    = message_response.get("textRandomizerEventsLeft")
        textRandomizerEventsWarning = message_response.get("textRandomizerEventsWarning")

        # importing variables: generics
        genericEnterBack    = message_response.get("genericEnterBack")
        genericChooseAction = message_response.get("genericChooseAction")
        genericChooseExit   = message_response.get("genericChooseExit")
        genericChooseReturn = message_response.get("genericChooseReturn")

        # importing variables: list_inputs
        textRandomizerOptionRerun1  = message_response.get("textRandomizerOptionRerun1")
        textRandomizerOptionRerun2  = message_response.get("textRandomizerOptionRerun2")

        print(headerRandomizer)

        while len(Events) > 1:                                           # events available + event picked + events left
            result = str(rchoice(Events)).strip("[']")                   # picks a random event and formats to remove [] and ''
            Events.remove(result)
            evleft = str(Events).translate(str.maketrans('', '', "[']")) # formats events list to remove [] and ''

            print(f'{textRandomizerEventsChosen}: {result}.\n{textRandomizerEventsLeft}: {evleft}.\n') # The chosen event is: {result}. Your events left: {evleft}.

            if len(Events) == 1:
                break
            
            rerun = list_input(genericChooseAction,
                               choices=[(f'{textRandomizerOptionRerun1}{len(Events)}{textRandomizerOptionRerun2}', '1'),
                                        (genericChooseReturn, '3'), (genericChooseExit, 'x')],
                              )
            
            match rerun:
                case '1':                         # re-runs
                    print(' #---#---#---#---#\n')
                    continue
                case '3': return                  # retuns to menu

        # action once there's only one event left
        evleft = str(Events).translate(str.maketrans('', '', "[']"))
        
        print(f'{textRandomizerEventsWarning} ({evleft})') # You only have one event left! ({evleft})

        getpass(genericEnterBack)

    #

    def DeletePreset(self, message_response, type): # deletes a preset
        
        # importing variables
        headerPresetDelete        = message_response.get("headerPresetDelete")
        genericChoosePreset       = message_response.get("genericChoosePreset")
        genericPresetDeleteCheck  = message_response.get("genericPresetDeleteCheck")
        genericPresetDeleteFinish = message_response.get("genericPresetDeleteFinish")
        genericPresetDeleteCancel = message_response.get("genericPresetDeleteCancel")

        genericYes = message_response.get("genericYes")
        genericNo  = message_response.get("genericNo")

        clearcmd()

        print(headerPresetDelete)

        preset_list = []
        preset_name_lst = set()

        for block in self.presets:
            if block[0] == type:
                preset_list.append(block)
        
        for block in preset_list:
            preset_name_lst.add(block[1])
        
        preset_name_lst = list(preset_name_lst)
        preset_name_lst.sort()

        choose_preset_item = list_input(genericChoosePreset, choices=preset_name_lst) # user chooses the preset to delete

        confirm = list_input(genericPresetDeleteCheck, choices=((genericYes, 'y'), genericNo))

        for block in self.presets:
            if block[1] == choose_preset_item:
                preset_item = block

        if confirm == 'y':
            self.presets.remove(preset_item)
            print('...'), sleep(.5)
            print(genericPresetDeleteFinish) # item deleted
        else:
            print(genericPresetDeleteCancel) # operation cancelled

        sleep(2)
    
    #

    def UpdatePresets(self): # updates the file presets.json
        
        new_presets = []

        for block in self.presets:
            preset_list = {
                'type':block[0],
                'name':block[1],
                'info':block[2]
            }

            new_presets.append(preset_list)
        
        with open('data/presets.json', 'w') as file:
            jdump(new_presets, file, indent=4)
        
# loads the language selection menu
Main.Lang()