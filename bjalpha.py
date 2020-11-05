import tkinter as tk
from tkinter import messagebox as mb
import time as te
import string
import random

infoText = ('''Project Card Alpha
Copyright ConorSS 2020''')

# Fully original code
# Written and tested by ConorSS

# Functions 

class bj:
    number = ['ac','02','03','04','05','06','07','08','09','10','jk','qu','kg']
    numint = [True,2,3,4,5,6,7,8,9,10,10,10,10]
    symbol = ['sb','dr','cb','hr']
    numstr = ['Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King','Null']
    symstr = ['Spades','Diamonds','Clubs','Hearts','Nulls']
    egg = ['sn','es']
    
    def newDeck():  # Creates a deck of cards and returns it
        out = []
        for sym in bj.symbol:
            for num in bj.number:
                out.append(num+sym)
        return out
    
    def playerAI(hand = []): # Player AI algorithm
        total = bj.convTotal(hand)
        #print(total,pow(total/21,3)*130)
        if type(total) is int:
            rand = random.randint(1, 100)
            if rand == 69:
                out = 'doubnice'
            elif int(pow(total/21,3)*130) < 19:
                if rand > 50:
                    out = 'doub'
                else:
                    out = 'twismax'
            elif rand > int(pow(total/21,3)*130):
                out = 'twisran'
            else:
                out = 'stik'
        else:
            mb.showwarning('AI error','playerAI had an internal error. (0125)')
            out = 'fail'
        return out
    
    def convTotal(hand = []):   # Convert hand list to total in int
        handtmp = []
        final = 0
        aces = 0
        numbalt = bj.number
        for card in hand:
            handtmp.append(card[0:2])
        for card in handtmp:
            if type(card) is str:
                indextmp = bj.number.index(card)
                value = bj.numint[indextmp]
                if type(value) is bool:     # Ace algorithm
                    acetotal = 0
                    acetmp = aces
                    for acecard in handtmp: # Does the handtmp loop, substituting all aces for 11 except already tested 1s
                        aceindextmp = bj.number.index(acecard)
                        acevalue = bj.numint[aceindextmp]
                        if type(acevalue) is bool:
                            if acetmp != 0:
                                acetotal += 1
                                acetmp -= 1
                            else:
                                acetotal += 11
                        else:
                            acetotal += acevalue
                    if acetotal > 21:
                        aces += 1
                        final += 1
                    else:
                        final += 11
                else:
                    final += value
            else:
                final = None
        return final
    
    def drawRand(deck, hand):   # Moves random card from 'deck' to 'hand'
        tmp = -1
        for x in deck:
            tmp += 1
        nwcrd = deck.pop(random.randint(0,tmp))
        hand.append(nwcrd)
        return nwcrd
    
    def clearHand(hand, deck):  # Places all cards from 'hand' to 'deck'
        tmp = []
        for card in hand:
            deck.append(card)
        hand.clear()

    def cardToString(card):     # Converts card name to printable, user friendly string and returns it
        numidx = 13
        symidx = 4
        try:
            numidx = bj.number.index(card[0:2])
            symidx = bj.symbol.index(card[2:4])
        except:
            pass
        return (bj.numstr[numidx]+" of "+bj.symstr[symidx].lower())

    def cardToInt(card):    # Converts card name to numeric value (Aces always 11)
        numidx = 13
        out = None
        try:
            numidx = bj.number.index(card[0:2])
        except:
            pass
        
        if bj.numint[numidx] == True:
            out = 11
        else:
            out = bj.numint[numidx]
        return numidx
            
class terminalGame:   # Game on terminal interface
    class sp:   # Singleplayer interface functions
        helptext = '''help\tDisplays help list
start\tStarts a game of blackjack with settings provided
options\tEdit settings and options
exit\tCloses SP terminal interface'''
        config = [['players',8],['playAsBanker',True],['lightspeed',False],['outDelay',0.2]]
        defaultconfig = config
        configdesc = ['\nAmount of players (Includes you).\nNumeric value','\nAllows players to play as banker.\nTHIS OPTION IS BROKEN. DO NOT SET TO FALSE.\nTrue/False','\nDisable all delays.\nTrue/False','\nDelay between lines of text.\nNumeric value']
        rootValues = [1]
        
        def bjGame(config):     # Blackjack singleplayer interface
            allHands = []
            def pause():    # Saves me having to do an if statement for every time.sleep
                if not config[2][1]:
                    te.sleep(config[3][1])
            
            def listings(mode = 1, allHands = allHands):   # Lists player name, card total, and status.
                if mode == 0:    # debug listings mode
                    print('[debug listall]\nName\tTotal\tCards\tStatus\t\tBet')
                    for playerData in allHands:
                        stat = 'In play'
                        bet = playerData[4]
                        if bj.convTotal(playerData[2]) > 21:
                            stat = 'Bust'
                        if playerData[3] == True:
                            bet = 'Banker'
                        print('{}\t{}\t{}\t{}\t\t{}'.format(playerData[0],bj.convTotal(playerData[2]),len(playerData[2]),stat,bet))
                    input('[e2c]')
                elif mode == 1:
                    print('Current standings:\nName\tCards\tBet')
                    for playerData in allHands:
                        if playerData[3] != True:
                            cards = None
                            if not bj.convTotal(playerData[2]) > 21:
                                cards = len(playerData[2])
                            else:
                                cards = 'Bust'
                            print('{}\t{}\t{}'.format(playerData[0],cards,playerData[4]))
                    input('[enter to continue]')
                    
            
            for player in range(1,config[0][1]+1):    # Set up player hand list
                allHands.append(["AI "+str(player),player,[],False,None,1000])  # format: [player-name, player-number, hand, banker-flag, bet, nymbs]
            allHands[0][0] = 'User'     # Player line
            if config[1][1] == True:    # Banker set script
                banker = random.choice(allHands)
                allHands[allHands.index(banker)][3] = True
                print(banker[0],'is the banker.')
            else:
                banker = None
            while 1:    # Game ready, loop begin
                pause()
                deck = bj.newDeck()
                
                for playerData in allHands: # Draw first two player cards
                    if len(playerData[2]) <= 0:
                        pass
                    else:
                        playerData[2] = []
                    for zxy in range(0,2):
                        bj.drawRand(deck, playerData[2])
                        
                for playerData in allHands: # Betting phase
                    if playerData[3] != True:
                        pause()
                        betmp = 50
                        if playerData[0].startswith('User'):
                            print(playerData[0]+' is betting.\nYour card:',bj.cardToString(playerData[2][0]),'\nYour total money:',str(playerData[5])+'Nb\nType what you want to bet.')
                            while 1:
                                try:
                                    betmp = int(input('>>'))     #full amount*(card value/13)^2
                                except:
                                    betmp = None
                                if type(betmp) == int:
                                    if betmp <= 50:
                                        print('Bet must be more than 50Nb.')
                                    else:
                                        playerData[4] = betmp
                                        print(playerData[0],'has placed their bet of',str(playerData[4])+'Nb.')
                                        break
                                elif type(betmp) == float:
                                    print('Invalid input. Decimals not supported.')
                                else:
                                    print('Invalid input. Please type a number.')
                        else:
                            print(playerData[0]+' is betting.')
                            pause()
                            playerData[4] = int(playerData[5]*(bj.cardToInt(playerData[2][0])/13))+random.randint(-9,9)   # ai algorithm
                            if playerData[4] <= 50:
                                playerData[4] = 50
                            print(playerData[0],'has placed their bet of',str(playerData[4])+'Nb.')
                            
                for playerData in allHands: # Playing phase
                    if playerData[3] != True:
                        pause()
                        pd = False
                        print(playerData[0]+'\'s turn\t\tBet:',playerData[4])
                        if bj.convTotal(playerData[2]) == 21:
                            pause()
                            print(playerData[0],'has a PERFECT DECK')
                            print(playerData[0],'sticks on',len(playerData[2]),'cards.')
                            pd = True
                        while 1:
                            if pd:
                                break
                            pause()
                            if bj.convTotal(playerData[2]) > 21:
                                print(playerData[0],'is bust! Total:',bj.convTotal(playerData[2]))
                                break
                            if len(playerData[2]) >= 5:
                                print(playerData[0],'has a FIVE CARD TRICK')
                                print(playerData[0],'sticks on',len(playerData[2]),'cards.')
                                break
                            if playerData[0].startswith('User'):    # Player's turn
                                print('[YOUR HAND]:')
                                for card in playerData[2]:
                                    print(bj.cardToString(card))
                                print('[TOTAL:',str(bj.convTotal(playerData[2]))+']')
                                chse = input('You can Twist, Double or Stick.\n>>')
                                pause()
                                if chse.lower().startswith('s'):   # Stick 
                                    print(playerData[0],'sticks on',len(playerData[2]),'cards.')
                                    break
                                elif chse.lower().startswith('t'):  # Twist
                                    print(playerData[0],'twists.\nGot',bj.cardToString(bj.drawRand(deck,playerData[2]))+'.')
                                elif chse.lower().startswith('d'):  # Double
                                    playerData[4] *= 2
                                    print('(Got '+bj.cardToString(bj.drawRand(deck,playerData[2]))+')')
                                    print(playerData[0],'doubles!\nGot a card. Bet increased to '+str(playerData[4])+'.')
                                else:
                                    print('Invalid input.')
                            else:   # AI's turn
                                pause()
                                chse = bj.playerAI(playerData[2])
                                #print(chse)
                                if chse.lower().startswith('s'):   # Stick          copypaste
                                    print(playerData[0],'sticks on',len(playerData[2]),'cards.')
                                    break
                                elif chse.lower().startswith('t'):  # Twist
                                    print(playerData[0],'twists.\nGot',bj.cardToString(bj.drawRand(deck,playerData[2]))+'.')
                                elif chse.lower().startswith('d'):  # Double
                                    playerData[4] *= 2
                                    bj.drawRand(deck,playerData[2])
                                    print(playerData[0],'doubles!\nGot a card. Bet increased to '+str(playerData[4])+'.')
                
                listings()
                fcardflag = False
                pdeckflag = False
                bnkidx = None
                if 1 == 0:
                    pass    # conor please add section for no banker
                else:
                    for playerData in allHands: # Banker's phase (mostly copypaste of player's phase)
                        if playerData[3] == True:
                            bnkidx = allHands.index(playerData)
                            print('Banker\'s turn. ('+playerData[0]+')')
                            if playerData[0].startswith('User'):
                                print('Your total money: '+str(playerData[5]))
                            if bj.convTotal(playerData[2]) == 21:
                                pause()
                                print(playerData[0],'has a PERFECT DECK')
                                print(playerData[0],'sticks on',len(playerData[2]),'cards. Total:',bj.convTotal(playerData[2]))
                                pdeckflag = True
                            while 1:
                                pause()
                                if pdeckflag:
                                    break
                                if bj.convTotal(playerData[2]) > 21:
                                    print(playerData[0],'is bust! Total:',bj.convTotal(playerData[2]))
                                    break
                                if len(playerData[2]) >= 5:
                                    print(playerData[0],'has a FIVE CARD TRICK')
                                    print(playerData[0],'sticks on',len(playerData[2]),'cards. Total:',bj.convTotal(playerData[2]))
                                    fcardflag = True
                                    break
                                if playerData[0].startswith('User'):    # Player is banker
                                    print('[YOUR HAND]:')
                                    for card in playerData[2]:
                                        print(bj.cardToString(card))
                                    print('[TOTAL:',str(bj.convTotal(playerData[2]))+']')
                                    chse = input('You can Twist or Stick.\n>>')
                                    pause()
                                    if chse.lower().startswith('s'):   # Stick 
                                        print(playerData[0],'sticks on',len(playerData[2]),'cards. Total:',bj.convTotal(playerData[2]))
                                        break
                                    elif chse.lower().startswith('t'):  # Twist
                                        print(playerData[0],'twists.\nGot',bj.cardToString(bj.drawRand(deck,playerData[2]))+'.')
                                    elif chse.lower().startswith('d'):  # Double
                                        print('Double unavailable when banker. (You can\'t bet.)')
                                    else:
                                        print('Invalid input.')
                                else:   # AI is banker
                                    pause()
                                    chse = bj.playerAI(playerData[2])
                                    #print(chse)
                                    if chse.lower().startswith('s'):   # Stick
                                        print(playerData[0],'sticks on',len(playerData[2]),'cards. Total:',bj.convTotal(playerData[2]))
                                        break
                                    elif chse.lower().startswith('t'):  # Twist
                                        print(playerData[0],'twists.\nGot',bj.cardToString(bj.drawRand(deck,playerData[2]))+'.')
                                    elif chse.lower().startswith('d'):  # Double
                                        print(playerData[0],'twists.\nGot',bj.cardToString(bj.drawRand(deck,playerData[2]))+'.')
                input('[enter to continue]')
                errorflag = False
                bnkorig = allHands[bnkidx][5]
                bnkscor = ''
                print('P A Y O U T')
                try:
                    x = allHands[bnkidx][2]
                except:
                    print('---\nGAME ERROR\nBJ01\nNo banker allocated\nRedownload reccomended')
                    input('---')
                    errorflag = True
                    exit() #er3h saw r0noc
                if fcardflag:
                    print('Banker has a five card trick. Banker wins all.')
                elif pdeckflag:
                    print('Banker has a perfect deck. Banker pays five card tricks only.')
                elif bj.convTotal(allHands[bnkidx][2]) > 21:
                    print('Banker is bust. Banker pays all.')
                else:
                    print('Number to beat:',bj.convTotal(allHands[bnkidx][2]))
                print('Name\tTotal\t\tStatus\tWinnings\tNb')
                for playerData in allHands: # P A Y O U T
                    if playerData[3] != True:
                        status = 'null'
                        win = '+-0'         # winnings string
                        total = str(bj.convTotal(playerData[2]))
                        winint = playerData[4]
                        nbstr = ' ('+str(playerData[5])+')'
                        if bj.convTotal(playerData[2]) > 21:
                            status = 'bust'
                            win = '-'+str(playerData[4])
                            total += '\t'
                            winint = -winint
                        else:
                            if len(playerData[2]) >= 5:
                                total += ' (five card)'
                            elif len(playerData[2]) == 2 and bj.convTotal(playerData[2]) == 21:
                                total += ' (perfect)'
                            else:
                                total += '\t'
                            if fcardflag:
                                if len(playerData[2]) >= 5:
                                    status = 'draw'
                                else:
                                    status = 'lose'
                                    win = '-'+str(playerData[4])
                            elif pdeckflag:
                                if len(playerData[2]) >= 5:
                                    status = 'win'
                                    win = '+'+str(playerData[4])
                                elif len(playerData[2]) == 2 and bj.convTotal(playerData[2]) == 21:
                                    status = 'draw'
                                else:
                                    status = 'lose'
                                    win = '-'+str(playerData[4])
                            elif bj.convTotal(allHands[bnkidx][2]) > 21:
                                status = 'win'
                                win = '+'+str(playerData[4])
                            else:
                                if bj.convTotal(playerData[2]) > bj.convTotal(allHands[bnkidx][2]):
                                    status = 'win'
                                    win = '+'+str(playerData[4])
                                elif bj.convTotal(playerData[2]) < bj.convTotal(allHands[bnkidx][2]):
                                    status = 'lose'
                                    win = '-'+str(playerData[4])
                                else:
                                    status = 'draw'
                            if status == 'lose':
                                winint = -winint
                            elif status != 'win':
                                winint = 0
                        playerData[5] += winint
                        allHands[bnkidx][5] -= winint
                        if status == 'draw':
                            nbstr = str(playerData[5])
                        else:
                            nbstr = str(playerData[5])+nbstr
                        print('{}\t{}\t{}\t{}\t\t{}'.format(playerData[0],total,status,win,nbstr))
                    else:
                        bnkscor = '{}\t{}\t\t{}\t{}\t\t{}'.format(playerData[0],'BANKER','{}','{}','{} ('+str(bnkorig)+')')
                stat = 'loss'
                win = allHands[bnkidx][5]-bnkorig
                if win == 0:
                    win = '+-0'
                    stat = 'n/a'
                elif win > 0:
                    win = '+'+str(win)
                    stat = 'profit'
                print(bnkscor.format(stat,win,allHands[bnkidx][5]))
                input('[enter to continue]')
                pause()
                newbnkr = []
                for playerData in allHands: # check for new banker
                    if playerData[3] != True:
                        if len(playerData[2]) == 2 and bj.convTotal(playerData[2]) == 21:
                            newbnkr.append(allHands.index(playerData))
                if len(newbnkr) > 0: #fix this
                    newbnkrfnl = random.choice(newbnkr)
                    allHands[newbnkrfnl][3] = True
                    allHands[bnkidx][3] = False
                    print('Banker switched to '+allHands[newbnkrfnl][0]+'.')
                else:
                    print(allHands[bnkidx][0]+' is still the banker.')
                pause()
                print('-- NEXT ROUND --')   # end bj, 05/11/2020
                
        def configModif(command,config):    # Config list interface
            def resetToDefault(default = terminalGame.sp.defaultconfig, config = config):   # pyception: functions within functions
                config = default
                print('Reset settings to default.')
                input('[Enter to continue]')
                
            def dispAll(config = config):   # Display all settings and values
                print('(Showing all options)\n\nSetting\t\t Value')
                for item in config:
                    print(item[0],"\t",item[1])
                print('\nTo modify a setting, type:\noptions <setting> <value>')
                
            def modify(replace = [], config = config):  # Modify settings and values
                index = None
                index2 = None
                stored = None
                for item in config:
                    if replace[0] == item[0]:
                        index = config.index(item)
                        stored = item
                if index == None:
                    print('Invalid setting input for modify "'+replace[0]+'".')
                    dispAll()
                else:
                    if type(stored[1]) is bool:
                        if replace[1].lower().startswith('t'):
                            stored[1] = True
                            print('Set "'+stored[0]+'" to True.')
                        elif replace[1].lower().startswith('f'):
                            stored[1] = False
                            print('Set "'+stored[0]+'" to False.')
                        else:
                            print('Invalid value input for modify "'+replace[0],replace[1]+'". (Boolean)')
                            dispAll()
                    elif type(stored[1]) is int:
                        try:
                            int(replace[1])
                        except:
                            print('Invalid value input for modify "'+replace[0],replace[1]+'". (Integer)')
                            dispAll()
                        else:
                            stored[1] = int(replace[1])
                            print('Set "'+stored[0]+'" to '+str(stored[1])+'.')
                    else:
                        print('Internal data error. Reset options to default?')# carry on doing this
                        select = input('[Y/N]>')
                        if select.lower().startswith('y'):
                            resetToDefault()
            
            def desc(read = [], config = config):   # Sync description list with config list and output
                index = None
                count1 = 0
                count2 = 0
                for item in config:
                    count1 += 1
                    try:
                        index = item.index(read)
                    except:
                        count2 += 1
                    else:
                        index = config.index(item)
                        print('Setting:',item[0],'\tValue:',item[1],terminalGame.sp.configdesc[index],'\nTo modify this value, type options '+read+' <new value>.')
                        break
                if count2 == count1:
                    print('Invalid setting input "'+read+'".')  
                    dispAll()
                    
            command = command.split(' ')
            try:
                command[1]
            except:
                dispAll()
            else:
                try:
                    command[2]
                except:
                    desc(command[1])
                else:
                    modify([command[1],command[2]])

        def rootLoop(): # SP root loop
            print(infoText+'\nSP terminal interface\nType Help for a list of commands')
            while 1:
                rloopin = input('>')
                if rloopin.lower().startswith('h' or 'help'):
                    print(terminalGame.sp.helptext)
                elif rloopin.lower().startswith('e' or 'exit'):
                    break
                elif rloopin.lower().startswith('o' or 'options'):
                    terminalGame.sp.configModif(rloopin,terminalGame.sp.config)
                elif rloopin.lower().startswith('s' or 'start'):
                    terminalGame.sp.bjGame(terminalGame.sp.config)
    class dbg:  # Debug interface
        helptext = '''help\tDisplays help list
exit\tCloses debug interface
sequence\tRelays dev test sequence
sp\tStarts singleplayer rootloop'''
        def devsequence(): # Dev test sequence
            testdeck = bj.newDeck()
            testhand = []
            print(bj.drawRand(testdeck,testhand))
            bj.clearHand(testhand, testdeck)
            print(testdeck)
            bj.drawRand(testdeck,testhand)
            bj.drawRand(testdeck,testhand)
            bj.drawRand(testdeck,testhand)
            print(testhand)
            print(bj.convTotal(testhand))
            print(bj.convTotal(['ac','ac','kg']))
            for card in testhand:
                print(bj.cardToString(card))
        def rootLoop(): # Debug root loop
            print('[DEBUG]')
            while 1:
                rloopin = input('>')
                if rloopin.lower().startswith('h' or 'help'):
                    print(terminalGame.dbg.helptext)
                elif rloopin.lower().startswith('e' or 'exit'):
                    break
                elif rloopin.lower().startswith('sp' or 'singleplayer'):
                    print()
                    te.sleep(0.2)
                    terminalGame.sp.rootLoop()
                    print('[DEBUG]')
                elif rloopin.lower().startswith('s' or 'sequence'):
                    terminalGame.dbg.devsequence()


terminalGame.dbg.rootLoop()
        
