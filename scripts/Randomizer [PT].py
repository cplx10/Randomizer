#Randomizer v1.2/06 Feb 2024 | Feito por cplx; 11 Dec 2021.

from keyword import iskeyword
import random
import os

validYes = ['sim','ss','s']
validNo = ['não','nao','nn','n']

errorInput = 'Erro! Input inválido!'

def clearcmd():
    os.system('cls' if os.name == 'nt' else 'clear')

def Main():
    clearcmd()
    print('ATENÇÃO!\nInsira "x" abaixo para parar o programa.\n---')

    Events = []
    for x in range(9999):
        choiceEvent = input('Evento '+str(x+1)+' >>> ')

        if choiceEvent == 'x': break
        else: Events.append(choiceEvent)

    clearcmd()
    
    result = str(random.choices(Events))
    print('O evento escolhido foi: '+result.strip("['']")+'.')

    choiceContD()

def choiceContD():
    choiceContinue = input('Você quer fechar o programa? [sim/não] >>> ')

    if choiceContinue.lower() in validYes: input('---\nObrigado por usar o Randomizer! Feito por cplx em 11 Dezembro de 2021.\nPressione enter pra sair.'); exit()
    elif choiceContinue.lower() in validNo: clearcmd(); Main()
    else: print(errorInput); choiceContD()

def startCode():
    start = input('\nIniciar programa? [sim/não] >>> ')

    if start in validYes: Main()
    elif start in validNo: choiceContD()
    else: print(errorInput), startCode()

print('Bem-vindo(a) ao Randomizer v1.2!\nEste programa lhe deixa inserir eventos (quase) infinitos em um algoritmo que escolhe um deles aleatoriamente.')
startCode()