              ####################################################
              ####################################################
              ###                                              ###
              ###                       NAME:                  ###
              ###                    Kevin Cui                 ###
              ###                                              ###
              ###                       DATE:                  ###
              ###                    2019-02-14                ###
              ###                                              ###
              ###                   DESCRIPTION:               ###
              ###                   Hangman Game               ###
              ###                 Made With Python             ###
              ###                                              ###
              ####################################################
              ####################################################

# flowchart: https://www.lucidchart.com/documents/edit/3cda7fd5-be10-4a69-8f7b-c1f07f198b48/0
# flowchart does not include methods for saving and displaying scores

import random
import os

play = True
wins = 0
losses = 0

while play:

    print("===========\n  Hangman\n===========\nBy: Kevin Cui\n") #title
    print("Hello and welcome to the game of hangman.\n\nThere is a word that is unknown to you.\nGuess the letters, and maybe you'll find out what it is.\nHowever, you guess wrong, and another piece of the 'hangman' will to hang.\nGet all the letters in the word correct, and 'hangman' is free.\nBut, seven wrong guesses, and 'hangman' is hanged.\nGood luck!\n") #message


    if os.stat("log.txt").st_size > 27: #read score board
        while True:
            try:
                with open("log.txt", "r") as ins:
                    for line in ins:
                        print((line.lower()).upper()[:-1], end="\n")
                    print()
                    break
            except IOError:
               print("Error: word set file not found")
    if wins>0 or losses>0: #check current player's score
        print("\n"+name+"'S score:")
        print("\tWins:", wins, "\tLosses:", losses, "\n")
    else:
        name = input("PLAYER NAME:\n>>> ").upper() #enter name for leaderboard

    while True: #error proof file finding
        try:
            select = ["(>)", "( )", "( )", "( )"]
            click = 0
            choices = ["T", "E", "D", "R"]
            while True: #topic selection
                try:
                    selection = input("Select a game (press 1 to go to the next option, press 2 to select):\n\t"+select[0]+"Test --> Test Word\n\t"+select[1]+"Easy --> Mathematicians\n\t"+select[2]+"Difficult --> Programming Languages\n\t"+select[3]+"RUSSIAN --> Food Products\n>>> ").upper()
                    if selection == "1":
                        select[click] = "( )"
                        click += 1
                        if click>3:
                            click=0
                        select[click] = "(>)"
                    elif selection == "2":
                        topicCode = choices[click]
                        break
                    else:
                        print("Invalid response. Please press 1 to go to the next option or press 2 to select")
                except:
                    print("Invalid response. Please press 1 to go to the next option or press 2 to select")
            
            if topicCode=="E": #topic code check
                file = "math.txt"
                topic = "Mathematicians"
            elif topicCode=="D":
                file = "com.txt"
                topic = "Computer Programming Languages"
            elif topicCode=="R":
                eng = ['a', 'be', 've', 'ge', 'de', 'ye', 'yo', 'zhe', 'ze', 'ee', 'ee2', 'ka', 'el',
                       'em', 'en', 'o', 'pe', 'er', 'es', 'te', 'oo', 'ef', 'kha', 'tse', 'che', 'sha',
                       'scha', '?', 'ih', '!', 'e', 'yoo', 'ya'] #latin code words
                rusDict = {'a':'a', 'be':'б', 've':'в', 'ge':'г', 'de':'д', 'ye':'е', 'yo':'ё', 'zhe':'ж',
                            'ze':'з', 'ee':'и', 'ee2':'й', 'ka':'к', 'el':'л', 'em':'м', 'en':'н', 'o':'о',
                            'pe':'п', 'er':'р', 'es':'с', 'te':'т', 'oo':'у', 'ef':'ф', 'kha':'х', 'tse':'ц',
                            'che':'ч', 'sha':'ш', 'scha':'щ', '?':'ъ', 'ih':'ы', '!':'ь', 'e':'э', 'yoo':'ю', #Russian alphabet
                            'ya':'я'}
                wordSet = ["яблоко", "картофель", "борщ", "Бефстроганов", "солянка", "капуста", "блины", "окрошка", "хинкали", "рис"] #Russian word set (not ansi)
                topic = "Food Products продукты питания"
                break
            elif topicCode=="T":
                wordSet = ["hello world"] #set test
                break
            if topicCode!="R":
                with open(file, "r") as ins:
                    wordSet = []
                    for line in ins:
                        wordSet.append(line.lower()[:-1])
                    break
        except IOError:
           print("Error: word set file not found")
           
    if topicCode=="R": #alternate message for Russian
        print("The topic of the word is '"+topic[:-17]+"'. Тема слова'"+topic[14:]+"'.", end=" ") #topic
        print("There will be", len(wordSet), "word possibilities. Там будет", len(wordSet),"слов возможностей.")
    elif topicCode=="T": #alternate message for test run
        print("This is a test run. The secret word is 'hello world'")
    else:
        print("The topic of the word is '"+topic+"'.", end=" ") #topic
        print("There will be", len(wordSet), "word possibilities.")

    secretWord = random.choice(wordSet) #set secret word to a random word out of 4

    usedLetters = " " #initialize used letters
    attempts = 7 #set attempts to 7
    missingLetters = len(secretWord) #set missing letters to length of secret word

    r1 = "   ____ " #row possibilities for hangman
    r2 = "  |    |"
    r3 = "  |     "
    r11= "  |    X"
    r4 = "  |    O"
    r5 = "  |    |"
    r6 = "  |   /|"
    r7 = "  |   /|\\"
    r8 = "  |   / "
    r9 = "  |   / \\"
    r10= "------"

    print(r1+"\n"+r2+"\n"+r3+"\n"+r3+"\n"+r3+"\n"+r10) #empty hangman

    for i in secretWord:
        if i == " ":
            print(i, end=" ") #spaces
        else:
            print("_", end=" ") #empty word line

    print(" Used letters:", usedLetters) #output initial used letters

    if (topicCode=="R"):
                    
        print("-------------------------------------------------------------------\nRUSSIAN KEYBOARD/РУССКАЯ РАСКЛАДКА КЛАВИАТУРЫ\n-------------------------------------------------------------------")
        cnt = 0
        for code in eng:
            if code in rusDict:
                print("|", rusDict[code], ":", code, "|", end="")
                cnt+=1
                if cnt==5:
                    print()
                    cnt = 0
                elif cnt==0:
                    print("\t")
        print("\n-------------------------------------------------------------------")
        print("To see Russian keyboard again, guess 'key'. Чтобы снова увидеть русскую клавиатуру, угадайте 'key'")

    while attempts>0: #begin while loop to allow for continuous input, until no more attempts are left

        if topicCode=="R":
            while True: #error proof Russian input, allow for re-input if invalid or error
                try:
                    newLetter = input("Guess a letter. Угадай письмо:\n>>> ").lower()
                    if newLetter == 'key':
                        print("-------------------------------------------------------------------\nRUSSIAN KEYBOARD/РУССКАЯ РАСКЛАДКА КЛАВИАТУРЫ\n-------------------------------------------------------------------")
                        cnt = 0
                        for code in eng:
                            if code in rusDict:
                                print("|", rusDict[code], ":", code, "|", end="")
                                cnt+=1
                                if cnt==5:
                                    print("|")
                                    cnt = 0
                                elif cnt==0:
                                    print("\t")
                        print("\n-------------------------------------------------------------------")
                        print("To see Russian keyboard again, guess 'key'. Чтобы снова увидеть русскую клавиатуру, угадайте 'key'")
                    elif newLetter not in eng:
                        print("Invalid input, check Russian keyboard. Неверный ввод, проверьте русскую клавиатуру.")
                    elif rusDict[newLetter] in usedLetters:
                        print("Already guessed, try again. Уже догадался, попробуйте еще раз.")
                    else:
                        newLetter = rusDict[newLetter]
                        break
                except:
                    print("Invalid input, print a valid letter. Неверный ввод, напечатайте правильное письмо.")

        else:
            while True: #error proof input, allow for re-input if invalid or error
                try:
                    newLetter = input("Guess a letter:\n>>> ").lower() #input new letter
                    if len(newLetter) != 1: #check input is 1 letter
                        print("Invalid input, print 1 letter.")
                    elif newLetter in usedLetters: #check letter has not been guessed
                        print("Already guessed, try again.")
                    elif not newLetter.isalpha(): #check letter is in alphabet
                        print("Invalid input, print a letter from A-Z.")
                    else:
                        break
                except:
                    print("Invalid input, print a valid letter.")
        
        usedLetters += newLetter #add new letter to used letters

        if newLetter not in secretWord: #if wrong
            attempts -= 1 #use up an attempt
            
        print(r1+"\n"+r2) #output hangman
        if attempts == 0:
            print(r11)
        elif attempts <=6:
            print(r4)
        else:
            print(r3)
        if attempts<=3:
            print(r7)
        elif attempts<=4:
            print(r6)
        elif attempts<=5:
            print(r5)
        else:
            print(r3)
        if attempts<=1:
            print(r9)
        elif attempts<=2:
            print(r8)
        else:
            print(r3)
        print(r10)

        check = 0 #set check to 0, stores number of unknown letters

        for i in range (missingLetters):
            if secretWord[i] in usedLetters:
                 print(secretWord[i], end=" ") #print correctly guessed letters
            else:
                print("_", end=" ") #print blanks as unknown letters
                check+=1 #increase check
                
        print(" Used letters:", usedLetters) #output used letters
            
        if newLetter not in secretWord: #if wrong
            print ("Nope. You have", attempts,"attempts left.") #output remaining attempts

        if attempts == 0: #if there are no attempts left
            print("You lost, the word was", secretWord+".\n") #you lose
            losses+=1
        elif check==0: #if there are no unknown letters left
            print("You won!\n") #you win
            wins+=1
            break

    if check==0 or attempts==0: #play again option
        while True:
            try:
                again = input("Play again? (Y/N)\n>>> ").upper() #code for playing again
                if again=="Y":
                    play = True #keep true
                    break
                elif again=="N": #exit game
                    play = False    
                    f = open("log.txt", "a")
                    s = name+"--> Wins: "+str(wins)+", Losses: "+str(losses)+"\n"
                    f.write(s)
                    f.close()
                    while True:
                        try:
                            again = input("Would you like to keep the scoreboard? (Y/N)\n>>> ").upper() #code for playing again
                            if again=="Y":
                                break
                            elif again=="N": #delete scores from log
                                f = open("log.txt", "w")
                                f.write("|=|=| scoreboard |=|=|\n")
                                f.close()
                                print("Score board cleared.", end=" ")
                                break
                            else:
                                print("Invalid response. Reply 'Y' for yes, and 'N' for no")
                        except:
                            print("Error ending game, log file not found")                    
                    print("Goodbye!")
                    break
                else:
                    print("Invalid response. Reply 'Y' for yes, and 'N' for no")
            except:
                print("Error ending game, log file not found")

                
        

        
