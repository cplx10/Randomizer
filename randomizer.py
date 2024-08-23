# Randomizer v2.0.0/30 Apr 2024 | Made by cplx; 11 Dec 2021.
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
# A GUI would be cool to have, but I don't wanna bother with TKinter for now.
# Either way, I really hope you enjoy!
# 
# ~ cplx

from inquirer import list_input
from random import choice as rchoice
from getpass import getpass
from os import system, name as sysname
from enum import Enum, auto

version = '2.0.0' # program version

#

def clearcmd(): # clear terminal
    system('cls' if sysname == 'nt' else 'clear') # types "cls" on terminal if running on Windows, otherwise "clear" 

#

class Messages(Enum):
    randHeader = auto()
    diceHeader = auto()
    backPrompt = auto()
    errorInput = auto()
    unknownError = auto()

    welcomeMessage = auto()
    whatsNew = auto()
    aboutText = auto()
    
    randAttention = auto()
    eventDeclare = auto()
    noEventError = auto()
    
    chosenEvent = auto()
    evLeftDeclare = auto()
    evLeftText = auto()

    thankYou = auto()
    
    diceText = auto()
    rollText = auto()
    rollResult = auto()

class Languages(Enum):
    EN = auto()
    PT = auto()

# setting up english and portuguese texts in a dictionary

def set_language(language: Languages) -> dict:
    message_response = {}
    match language:
        case Languages.EN:
            message_response[Messages.randHeader] = '[The Randomizer]\n'
            message_response[Messages.diceHeader] = '[Roll a Die!]\n'
            message_response[Messages.backPrompt] = 'Press enter to return.'
            message_response[Messages.errorInput] = 'Error! Invalid input!'
            message_response[Messages.unknownError] = 'Unknown error.'

            message_response[Messages.welcomeMessage] = f'Welcome to the Randomizer v{version}!\n'
            message_response[Messages.whatsNew] = f"Here's what's new in the Randomizer {version}:\n\n - New language selection menu!\nNow you can easily switch between the Portuguese and English versions of the Radomizer\nwithout having to manually open the file yourself!\n\n - Expanded 'main menu'!\nWe have expandede the amount of choices you could make in the program's 'main menu',\nmaking access to new features easy and simple.\n\n - Roll a Die!\nIntroduced with this new version, Roll a Die! is a dice roller built into the program,\nmaking your life easier if you want to use this as a way to roll your d20.\n\n\n"
            message_response[Messages.aboutText] = "[ABOUT THE RANDOMIZER]\n\nThe Randomizer is a program developed by cplx in Python.\n\nIt's initial use as a program to decide random events came\nto be with Starlight's LARP's on the Discord community\nserver The Reservoir. It's first release, version 1.0.0,\ncame to be on 11 December, 2021, and it has been receiving\nnew updates since February 2024, when cplx released version 1.2.0.\n\nFor further information on the history of updates + change logs,\ncheck UpdLogs.txt on the Randomizer's folder.\n\n\n"

            message_response[Messages.randAttention] = '\nATTENTION!\nEnter "x" below to stop the program.\n---'
            message_response[Messages.eventDeclare] = 'Event'
            message_response[Messages.noEventError] = '\nYou must insert at least 1 event!\nPress enter to try again.'

            message_response[Messages.chosenEvent] = 'The chosen event is'
            message_response[Messages.evLeftDeclare] = 'Your events left'
            message_response[Messages.evLeftText] = 'You only have one event left!'

            message_response[Messages.thankYou] = f'Thank you for using the Randomizer v{version}! Made by cplx since 11 December 2021.\n > Press enter to exit.'

            message_response[Messages.diceText] = 'Type in the die you wanna roll (eg. d20)\n > d'
            message_response[Messages.rollText] = 'You rolled a d'
            message_response[Messages.rollResult] = 'Your result was'

        case Languages.PT:
            message_response[Messages.randHeader] = '[O Randomizer]\n'
            message_response[Messages.diceHeader] = '[Role um Dado!]\n'
            message_response[Messages.backPrompt] = 'Pressione enter para voltar.'
            message_response[Messages.errorInput] = 'Erro! Input inválido!'
            message_response[Messages.unknownError] = 'Erro desconhecido.'

            message_response[Messages.welcomeMessage] = f'Bem-vindo ao Randomizer v{version}!\n'
            message_response[Messages.whatsNew] = f"Aqui estão as novidades do Randomizer {version}:\n\n - Novo menu de seleção de idioma!\nAgora você pode facilmente trocar o idioma do Radomizer\nsem ter que abrir o arquivo manualmente!\n\n - 'Menu' expandido!\nNós aumentamos o número de escolhas no 'menu' do programa,\ndeixando o acesso à novas adições mais simples!\n\n - Role um Dado!\nIntroduzido com essa versão, o Role um Dado! é um rolador de dado imbutido no programa,\ndeixando sua vida mais fácil se você quiser rolar um d20.\n\n\n"
            message_response[Messages.aboutText] = "[SOBRE O RANDOMIZER]\n\nO Randomizer é um programa desenvolvido por cplx em Python.\n\nSeu uso inicial como um programa para decidir eventos aleatórios originou-se\ncom os LARP's de Starlight no servidor de comunidade do Discord\nThe Reservoir. Seu primeiro lançamento, a versão 1.0.0,\nveio em 11 Dezembro, 2021, e vem recebendo\natualizações novas desde Fevereiro 2024, quando cplx lançou a versão 1.2.0.\n\nPara mais informações sobre atualizações e change logs,\nveja UpdLogs.txt na pasta do Randomizer.\n\n\n"

            message_response[Messages.randAttention] = '\ATENÇÃO!\nInsira "x" abaixo para parar o programa.\n---'
            message_response[Messages.eventDeclare] = 'Evento'
            message_response[Messages.noEventError] = '\nVocê deve inserir pelo menos 1 events!\nPressione enter para tentar de novo.'

            message_response[Messages.chosenEvent] = 'O evento escolhido foi'
            message_response[Messages.evLeftDeclare] = 'Eventos restantes'
            message_response[Messages.evLeftText] = 'Você só tem um evento restante!'

            message_response[Messages.thankYou] = f'Obrigado por usar o Randomizer v{version}! Feito por cplx desd 11 Dezembro 2021.\n > Pressione enter para sair.'

            message_response[Messages.diceText] = 'Digite o dado que você quer rolar (ex. d20)\n > d'
            message_response[Messages.rollText] = 'Você rolou um d'
            message_response[Messages.rollResult] = 'Seu resultado foi'
    
    return message_response

#

def Lang(): # change language
    clearcmd()
    
     # selection menu
    language = list_input('Choose a language',
                          choices=[('English', Languages.EN), ('Português', Languages.PT)],
                          )
    
     # adopts chosen language
    message_response = set_language(language)
    Menu(message_response, language)

#

def Menu(message_response, language): # the main menu
    clearcmd()

     # importing variables
    welcomeMessage = message_response.get(Messages.welcomeMessage)
    whatsNew = message_response.get(Messages.whatsNew)
    aboutText = message_response.get(Messages.aboutText)
    backPrompt = message_response.get(Messages.backPrompt)

    print(welcomeMessage)

     # this will keep running until the function is called again
    while True:
        if language == Languages.EN:      # if is running in English
            start = list_input('Choose an option',
                               choices=[('Start the Randomizer', '1'), ('Roll a Die!', '2'), ("What's new", '3'),
                                        ('About the Randomizer', 'a'), ('Switch languages', 'l'), ('Exit', 'x')],
                               )
        else:                             # if is running in Portuguese
            start = list_input('Escolha uma opção',
                               choices=[('Rodar o Randomizer', '1'), ('Rolar um Dado!', '2'), ('Novidades', '3'),
                                        ('Sobre o Randomizer', 'a'), ('Trocar de idioma', 'l'), ('Sair', 'x')],
                               )

        match start:
            case '1': Rand(message_response, language)           # runs the program
            case '2': DiceMain(message_response, language)       # runs Roll a Die!
            case '3':                                            # what's new in the program
                clearcmd()
                print(whatsNew), getpass(backPrompt)
            
            case 'a':                                            # about the program
                clearcmd()
                print(aboutText), getpass(backPrompt)
            
            case 'l': Lang()                                     # switches languages
            case 'x': choiceContinue(message_response, language) # exits
    
        Menu(message_response, language)

#

def Rand(message_response, language): # the Randomizer
    clearcmd()

     # importing variables
    eventDeclare = message_response.get(Messages.eventDeclare)
    noEventError = message_response.get(Messages.noEventError)
    randAttention = message_response.get(Messages.randAttention)
    errorInput = message_response.get(Messages.errorInput)

    go = 1

    print(randAttention)

    Events = []

    while True: # events input
        choiceEvent = input(f' > {eventDeclare} {go}: ').strip()

        if not choiceEvent: print(errorInput) # if choiceEvent has no content
        elif choiceEvent == 'x': break        # breaks the program
        else:
            go += 1
            Events.append(choiceEvent)        # adds event to Events list

    if not Events: # if Events list is empty
        input(noEventError)
        Rand(message_response, language)

    choiceCheck(message_response, language, Events)

#

def choiceCheck(message_response, language, Events): # checks the events chosen
    clearcmd()

     # importing variables
    randHeader = message_response.get(Messages.randHeader)
    chosenEvent = message_response.get(Messages.chosenEvent)
    evLeftDeclare = message_response.get(Messages.evLeftDeclare)
    evLeftText = message_response.get(Messages.evLeftText)

    print(randHeader)

    while len(Events) > 1:                                             # events available + event picked + events left
        result = str(rchoice(Events)).strip("[']")                     # picks a random event and formats to remove [] and ''
        Events.remove(result)
        evleft = str(Events).translate(str.maketrans('', '', "[']"))   # formats events list to remove [] and ''

        print(f'{chosenEvent}: {result}.\n{evLeftDeclare}: {evleft}.') # The chosen event is: {result}. Your events left: {evleft}.

        if language == Languages.EN:
            rerun = list_input('Would you like to',
                               choices=[(f'Re-run with the events left (you have {len(Events)} left!)', '1'),
                                        ('Input new events', '2'), ('Return to menu', '3'), ('Exit the program', 'x')],
                               )
        else:
            rerun = list_input('Você gostaria de',
                               choices=[(f'Rodar de novo com os eventos restantes (você tem {len(Events)} restantes!)', '1'),
                                        ('Inserir novos eventos', '2'),('Voltar ao menu', '3'),('Fechar o programa', 'x')],
                               )
        
        match rerun:
            case '1': 0                                      # re-runs
            case '2': Rand(message_response, language)       # inputs new events
            case '3':                                        # retuns to menu
                clearcmd(), Menu(message_response, language)
                break
            case 'x':                                        # exits
                clearcmd(), choiceContinue(message_response, language)

    # choices once there's only one event left
    evleft = str(Events).translate(str.maketrans('', '', "[']"))
    
    print(f'{evLeftText} ({evleft})') # You only have one event left! ({evleft})

     # selection menu
    if language == Languages.EN:
        choiceEvent = list_input('Choose one of the following',
                                 choices=[('Input new events', '1'),('Return to menu','2'),('Exit the program','x')],
                                 )
    else:
        choiceEvent = list_input('Escolha um dos itens abaixo',
                                 choices=[('Inserir novos eventos', '1'),('Voltar ao menu','2'),('Sair do programa','x')],
                                 )
        
    match choiceEvent:
        case '1': Rand(message_response, language)                       # inputs new events
        case '2': clearcmd(), Menu(message_response, language)           # returns to menu
        case 'x': clearcmd(), choiceContinue(message_response, language) # exits

    exit()

#

def choiceContinue(message_response, language): # exit the program
    clearcmd()

     # importing variables
    thankYou = message_response.get(Messages.thankYou)
    randHeader = message_response.get(Messages.randHeader)

    print(randHeader)

     # selection menu
    if language == Languages.EN:
        promptContinue = list_input('Are you sure you want to close the program?',
                                    choices=[('Yes','y'),('No','n')],
                                    )
    else:
        promptContinue = list_input('Você tem certeza que quer fechar o programa?',
                                    choices=[('Sim','y'),('Não','n')],
                                    )

    if promptContinue == 'y': # close if 'y' is chosen (getpass is used to hide user input)
        getpass(thankYou), exit()

#

def DiceMain(message_response, language): # main menu for Roll a Die!
    clearcmd()

     # selection menu
    if language == Languages.EN:
        chostart = list_input('Welcome to Roll a Die! Choose an action',
                              choices=[('Run Roll a Die!', '1'),('Return to the Randomizer', 'x'),
                                       ('Save/load dice preset (coming soon!)', 'soon')]
                              )
    else:
        chostart = list_input('Bem-vindo ao Role um Dado! Escolha uma ação',
                              choices=[('Rodar Role um Dado!', '1'),('Voltar ao Randomizer', 'x'),
                                       ('Salvar/carregar preset de dados (em breve!)','soon')]
                              )

    match chostart:
        case '1': clearcmd(), Dice(message_response, language) # runs Roll a Die!
        case 'x': Menu(message_response, language)             # returns to main menu
        case 'soon': DiceMain(message_response, language)      # coming soon!

#

def Dice(message_response, language): # runs Roll a Die!

     # importing variables
    diceHeader = message_response.get(Messages.diceHeader)
    diceText = message_response.get(Messages.diceText)
    errorInput = message_response.get(Messages.errorInput)
    unknownError = message_response.get(Messages.unknownError)

    print(diceHeader)
    
    # asks you to type in a die, displaying an error message if something goes wrong
    try:
        dice = int(input(diceText))
    except ValueError:
        print(errorInput, '\n')
        Dice(message_response, language)
    except Exception as e:
        print(f"{unknownError}{e}\n")
        Dice(message_response, language)

    if not dice or dice <= 1: # in case user doesn't input any numbers, or if its less than 1
        print(errorInput,'\n')
        Dice(message_response, language)

    Roll(message_response, language, dice), exit()

#

def Roll(message_response, language, dice): # (re)rolls the die
    clearcmd()

     # importing variables
    diceHeader = message_response.get(Messages.diceHeader)
    rollText = message_response.get(Messages.rollText)
    rollResult = message_response.get(Messages.rollResult)

    result = str(rchoice(range(1,(dice+1)))) # picks a random number between 1 and the one you chose and transforms it into a string

    print(f'{diceHeader}\n{rollText}{dice}.\n{rollResult}: {result}.') # You rolled a d{dice}. Your result was: {result.}
    
     # selection menu
    if language == Languages.EN:
        re = list_input('Choose an action',
                        choices=[('Reroll the die', '1'),('Roll another die', '2'),('Return to menu', '3')],
                        )
    else:
        re = list_input('Escolha uma ação',
                        choices=[('Rerolar o dado', '1'),('Rolar outro dado', '2'),('Voltar ao menu', '3')],
                        )
    match re:
        case '1': Roll(message_response, language, dice)       # re-rolls die
        case '2': clearcmd(), Dice(message_response, language) # rolls another die
        case '3': DiceMain(message_response, language)         # returns to menu

# loads the language selection menu
Lang()
