# Randomizer v2.0.0/** Sep 2024 | Made by cplx; 11 Dec 2021.

from time import sleep
from copy import deepcopy
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
    ES = auto()

#

class Main:

    def set_language(language: Languages) -> dict:
        message_response = {}
        match language:
            case Languages.EN:
                with open('data/languages/english.json', encoding='utf-8') as f:
                    message_response = jload(f)

            case Languages.PT:
                with open('data/languages/portuguese.json', encoding='utf-8') as f:
                    message_response = jload(f)

            case Languages.ES:
                with open('data/languages/spanish.json', encoding='utf-8') as f:
                    message_response = jload(f)
        
        return message_response

    #

    def Lang(): # change language
           
        while True:
            clearcmd()

            # selection menu
            language = list_input('Choose a language',
                                choices=[('English', Languages.EN), ('Português', Languages.PT),
                                         ('Español', Languages.ES)],
                                )
            
            # adopts chosen language
            message_response = Main.set_language(language)
            Main.Menu(message_response)

    #

    def Menu(message_response): # the main menu

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
        genericChooseAction     = message_response.get("genericChooseAction")
        genericChooseExit       = message_response.get("genericChooseExit")
        genericEnterBack        = message_response.get("genericEnterBack")
        genericMenuManagePreset = message_response.get("genericMenuManagePreset")

        # this will keep running until the function is called again
        while True:
            clearcmd()

            print(textMenuWelcome+version+'!\n')

            start = list_input(genericChooseAction,
                            choices=[(textMenuOptionRandomizer, '1'), (textMenuOptionDice, '2'), (genericMenuManagePreset, '3'), (textMenuOptionNew, 'new'),
                                        (textMenuOptionAbout, 'a'), (textMenuOptionLanguage, 'l'), (genericChooseExit, 'x')],
                            )

            match start:
                case '1': Randomizer.Main(message_response)       # run the Randomizer
                case '2': Main.DiceMenu(message_response)         # open the Roll a Die! main menu
                case '3':                                         # manage Randomizer presets
                    Randomizer.PresetRandomizer(message_response)
                case 'new':                                       # what's new in the program
                    clearcmd(), print(textMenuNew)
                    getpass(genericEnterBack)
                case 'a':                                         # about the program
                    clearcmd(), print(textMenuAbout)
                    getpass(genericEnterBack)
                case 'l': break                                   # switch languages
                case 'x': Main.choiceContinue(message_response)   # exit
    
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

            # importing variables: generics
            genericMenuManagePreset = message_response.get("genericMenuManagePreset")
            genericChooseAction     = message_response.get("genericChooseAction")
            genericChooseExit       = message_response.get("genericChooseExit")

            # importing variables: selection menu
            textDiceMenuOptionRoll   = message_response.get("textDiceMenuOptionRoll")
            textDiceMenuOptionReturn = message_response.get("textDiceMenuOptionReturn")
            
            
            print(textDiceMenuWelcome,'\n')
            
            # selection menu
            choicestart = list_input(genericChooseAction,
                                choices=[(textDiceMenuOptionRoll, '1'),(genericMenuManagePreset, '2'),
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

    def PresetRandomizer(message_response): # manage Randomizer presets
        
        # importing variables: header
        headerPreset = message_response.get("headerPreset")

        # importing variables: generics
        genericChooseAction = message_response.get("genericChooseAction")
        genericChooseReturn = message_response.get("genericChooseReturn")

        # importing variables: list_input options
        genericPresetOptionNew    = message_response.get("genericPresetOptionNew")
        genericPresetOptionLoad   = message_response.get("genericPresetOptionLoad")
        genericPresetOptionEdit   = message_response.get("genericPresetOptionEdit")
        genericPresetOptionDelete = message_response.get("genericPresetOptionDelete")

        clearcmd()

        print(headerPreset)
        presets = PresetActions()

        savechoice = list_input(genericChooseAction,
                                choices=[(genericPresetOptionNew,'create'),
                                        (genericPresetOptionLoad,'load'), (genericPresetOptionEdit, 'edit'),
                                        (genericPresetOptionDelete,'delete'), (genericChooseReturn, 'x')],
                            )
         
        match savechoice:

            case 'create': # create a new rand preset

                # importing variables: header
                headerPresetNew = message_response.get("headerPresetNew")

                # importing variables: error messages
                errorInvalidInput      = message_response.get("errorInvalidInput")
                errorRandomizerNoEvent = message_response.get("errorRandomizerNoEvent")

                # importing variables: preset texts
                textPresetRandomizerNewType = message_response.get("textPresetRandomizerNewType")
                genericPresetNewName        = message_response.get("genericPresetNewName")
                
                preset_rand = []

                clearcmd()
                print(f'{headerPresetNew}\n{textPresetRandomizerNewType}')
                    
                while True:

                    while True:
                        input_rand = input(' > ').strip()

                        if not input_rand: print(errorInvalidInput) # if input_rand has no content
                        elif input_rand == 'x': break               # if input_rand is 'x'
                        else:
                            preset_rand.append(input_rand)          # adds event to preset_rand

                    if not input_rand:                              # if the events list is empty
                        getpass(errorRandomizerNoEvent)
                        continue

                    break
                
                preset_name = input(genericPresetNewName)
                
                presets.CreatePreset(message_response, 'rand', preset_name, preset_rand)
            
            case 'load': # load a rand preset

                presets.LoadRandomizerPreset(message_response)

            case 'edit': # edit a rand preset
                
                presets.EditPreset(message_response, 'rand')
            
            case 'delete': # delete a rand preset

                presets.DeletePreset(message_response, 'rand')
            
            case 'x': return

        presets.UpdatePresets() # update preset list

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
                
            except OverflowError as over:
                print(f'{errorInvalidInput} {over}'), sleep(1.5)
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

    def PresetDice(message_response): # manage Roll a Die! presets
        
        # importing variables: header
        headerPreset = message_response.get("headerPreset")

        # importing variables: generics
        genericChooseAction = message_response.get("genericChooseAction")
        genericChooseReturn = message_response.get("genericChooseReturn")

        # importing variables: list_input options
        genericPresetOptionNew    = message_response.get("genericPresetOptionNew")
        genericPresetOptionLoad   = message_response.get("genericPresetOptionLoad")
        genericPresetOptionEdit   = message_response.get("genericPresetOptionEdit")
        genericPresetOptionDelete = message_response.get("genericPresetOptionDelete")

        clearcmd()

        print(headerPreset)

        presets = PresetActions()

        savechoice = list_input(genericChooseAction,
                                choices=[(genericPresetOptionNew,'create'),
                                        (genericPresetOptionLoad,'load'), (genericPresetOptionEdit, 'edit'),
                                        (genericPresetOptionDelete,'delete'), (genericChooseReturn, 'x')],
                            )
         
        match savechoice:

            case 'create': # create a new dice preset

                # importing variables: header
                headerPresetNew = message_response.get("headerPresetNew")

                # importing variables: error messages
                errorInvalidInput = message_response.get("errorInvalidInput")
                errorUnknown      = message_response.get("errorUnknown")

                # importing variables: preset texts
                textPresetDiceNewType = message_response.get("textPresetDiceNewType")
                genericPresetNewName  = message_response.get("genericPresetNewName")

                preset_dice = []

                while True:
                    clearcmd()
                    print(f'{headerPresetNew}\n{textPresetDiceNewType}')

                    while True:
                        
                        input_dice = input(' > d')
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
                    
                    if not preset_dice:
                        print(errorInvalidInput,'\n'), sleep(1.5)
                        continue
                    
                    preset_name = input(genericPresetNewName)
                    break
                
                presets.CreatePreset(message_response, 'dice', preset_name, preset_dice)
            
            case 'load': # load a dice preset

                presets.LoadDicePreset(message_response)

            case 'edit': # edit a dice preset
                
                presets.EditPreset(message_response, 'dice')
            
            case 'delete': # delete a dice preset
                presets.DeletePreset(message_response, 'dice')
            
            case 'x': return
        
        presets.UpdatePresets() # update preset list

#

class PresetActions:

    def __init__(self): # opens the preset list
        
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

    def LoadDicePreset(self, message_response): # loads a Roll a Die! preset
        
        # importing variables
        textPresetDiceLoadNote = message_response.get("textPresetDiceLoadNote")
        genericChoosePreset    = message_response.get("genericChoosePreset")

        clearcmd()
        
        print(textPresetDiceLoadNote)
        choose_preset_item = PresetActions.GetPresetNameList(self.presets, 'dice', genericChoosePreset)

        for block in self.presets:
            if block[1] == choose_preset_item:
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
        genericChooseAction  = message_response.get("genericChooseAction")
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

    def LoadRandomizerPreset(self, message_response): # loads a Randomizer preset

        # importing variables
        textPresetRandomizerLoadNote = message_response.get("textPresetRandomizerLoadNote")
        genericChoosePreset          = message_response.get("genericChoosePreset")

        clearcmd()
        
        print(textPresetRandomizerLoadNote)
        choose_preset_item = PresetActions.GetPresetNameList(self.presets, 'rand', genericChoosePreset)

        for block in self.presets:
            if block[1] == choose_preset_item:
                presets = block[2]
            
        PresetActions.RunRandomizerPreset(message_response, presets)
        return

    #

    def RunRandomizerPreset(message_response, Events): # runs the events from the preset

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

        clearcmd()
        temp_events = Events.copy()
        print(headerRandomizer)

        while len(temp_events) > 1:                                           # events available + event picked + events left
            result = str(rchoice(temp_events)).strip("[']")                   # picks a random event and formats to remove [] and ''
            temp_events.remove(result)
            evleft = str(temp_events).translate(str.maketrans('', '', "[']")) # formats events list to remove [] and ''

            print(f'{textRandomizerEventsChosen}: {result}.\n{textRandomizerEventsLeft}: {evleft}.\n') # The chosen event is: {result}. Your events left: {evleft}.

            if len(temp_events) == 1:
                break
            
            rerun = list_input(genericChooseAction,
                               choices=[(f'{textRandomizerOptionRerun1}{len(temp_events)}{textRandomizerOptionRerun2}', '1'),
                                        (genericChooseReturn, '2'), (genericChooseExit, 'x')],
                              )
            
            match rerun:
                case '1':                                 # re-runs
                    print(' #---#---#---#---#\n')
                    continue
                case '2': return                          # retuns to menu
                case 'x':                                 # exits
                    Main.choiceContinue(message_response)

        # action once there's only one event left
        evleft = str(temp_events).translate(str.maketrans('', '', "[']"))
        
        print(f'{textRandomizerEventsWarning} ({evleft})') # You only have one event left! ({evleft})

        getpass(genericEnterBack)

    #

    def EditPreset(self, message_response, type): # edits a preset

        # importing variables: header & main messages
        headerPresetEdit    = message_response.get("headerPresetEdit")
        genericChoosePreset = message_response.get("genericChoosePreset")

        clearcmd()
        print(headerPresetEdit)

        choose_preset_item = PresetActions.GetPresetNameList(self.presets, type, genericChoosePreset)

        for block in self.presets:
            if block[1] == choose_preset_item:
                temp = PresetActions.EditOperations(message_response, type, block)
        
        self.presets = [temp if temp[1] == block[1] else block for block in self.presets]        
        return
    
    #

    def EditOperations(message_response, type, info): # editing operations

        # importing variables: main message
        headerPresetEdit    = message_response.get("headerPresetEdit")
        genericChooseAction = message_response.get("genericChooseAction")

        # importing variables: errors
        errorInvalidInput = message_response.get("errorInvalidInput")
        errorUnknown      = message_response.get("errorUnknown")

        # importing variables: list_input #1 options
        genericPresetEditOptionAdd     = message_response.get("genericPresetEditOptionAdd")
        genericPresetEditOptionRemove  = message_response.get("genericPresetEditOptionRemove")
        genericPresetEditOptionConfirm = message_response.get("genericPresetEditOptionConfirm")
        genericPresetEditOptionCancel  = message_response.get("genericPresetEditOptionCancel")

        # importing variables: choose an item to remove
        genericPresetEditChooseRemove = message_response.get("genericPresetEditChooseRemove")

        # importing variables: text prompts
        genericPresetEditTextConfirm = message_response.get("genericPresetEditTextConfirm")
        textPresetRandomizerNewType  = message_response.get("textPresetRandomizerNewType")
        textPresetDiceNewType        = message_response.get("textPresetDiceNewType")

        # importing variables: final messages
        genericPresetDeleteFinish = message_response.get("genericPresetDeleteFinish")
        genericPresetCancel       = message_response.get("genericPresetCancel")

        temp_info = deepcopy(info)

        while True:
            clearcmd()

            print(f'{headerPresetEdit}\n #-> {temp_info[1]} <-#\n')
            
            for item in temp_info[2]:
                print(f' > {item}')
            
            print('')
            
            choose_action = list_input(genericChooseAction,
                                       choices=[(genericPresetEditOptionAdd,'add'), (genericPresetEditOptionRemove, 'remove'),
                                                (genericPresetEditOptionConfirm, 'confirm'), (genericPresetEditOptionCancel, 'cancel')]
                                      )
            
            match choose_action:
                case 'add': # adds a new item to the list

                    # rand
                    if type == 'rand':

                        print(textPresetRandomizerNewType)

                        while True: # events input
                            choiceEvent = input(f' > ').strip()

                            if not choiceEvent: print(errorInvalidInput) # if choiceEvent has no content
                            elif choiceEvent == 'x': break               # if choiceEvent is 'x'
                            else:
                                temp_info[2].append(choiceEvent)         # adds event to Events list

                    # dice
                    if type == 'dice':
                        
                        print(textPresetDiceNewType)

                        while True:
                            
                            input_dice = input(' > d')
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

                            temp_info[2].append(input_dice)
                
                case 'remove': # deletes an item

                    remove_check = list_input(genericPresetEditChooseRemove,
                                              choices=temp_info[2]
                                             )

                    for item in temp_info[2]:
                        if item == remove_check:
                            temp_info[2].remove(item)
                    
                    print(genericPresetDeleteFinish)
                
                case 'confirm': # commits changes and exits
                    
                    print(genericPresetEditTextConfirm), sleep(2)
                    return temp_info

                case 'cancel': # cancels, reverses changes and exits

                    print(genericPresetCancel), sleep(2)
                    return info

    #

    def DeletePreset(self, message_response, type): # deletes a preset
        
        # importing variables
        headerPresetDelete        = message_response.get("headerPresetDelete")
        genericChoosePreset       = message_response.get("genericChoosePreset")
        genericPresetDeleteCheck  = message_response.get("genericPresetDeleteCheck")
        genericPresetDeleteFinish = message_response.get("genericPresetDeleteFinish")
        genericPresetCancel       = message_response.get("genericPresetCancel")

        genericYes = message_response.get("genericYes")
        genericNo  = message_response.get("genericNo")

        clearcmd()

        print(headerPresetDelete)

        choose_preset_item = PresetActions.GetPresetNameList(self.presets, type, genericChoosePreset)

        confirm = list_input(genericPresetDeleteCheck, choices=((genericYes, 'y'), genericNo))

        for block in self.presets:
            if block[1] == choose_preset_item:
                preset_item = block

        if confirm == 'y':
            self.presets.remove(preset_item)
            print('...'), sleep(.5)
            print(genericPresetDeleteFinish) # item deleted
        else:
            print(genericPresetCancel) # operation cancelled

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
        
        with open('data/presets.json', 'w', encoding='utf-8') as file:
            jdump(new_presets, file, indent=4)
    
    #

    def GetPresetNameList(presets, type, genericChoosePreset): # gets the list of names

        preset_list = []
        preset_name_lst = set()

        for block in presets:
            if block[0] == type:
                preset_list.append(block)
        
        for block in preset_list:
            preset_name_lst.add(block[1])
        
        preset_name_lst = list(preset_name_lst)
        preset_name_lst.sort()

        choose_preset_item = list_input(genericChoosePreset, choices=preset_name_lst) # user chooses a preset

        return choose_preset_item
        
# loads the language selection menu
Main.Lang()
