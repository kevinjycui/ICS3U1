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

import random

print("Hangman\nBy: Kevin Cui\n") #title
print("Hello and welcome to the game of hangman.\nThere is a word that is unknown to you.\nGuess the letters, and maybe you'll find out what it is.\nHowever, you guess wrong, and another piece of the 'hangman' will to hang.\nGet all the letters in the word correct, and 'hangman' is free.\nBut, seven wrong guesses, and 'hangman' is hanged.\nGood luck!") #message
print("The topic of the word is 'Mathematicians'.", end=" ") #topic

wordSet = ["euler", "euclid", "gauss", "pythagoras", "brahmagupta",
           "archimedes", "turing", "boole", "einstein", "pascal", "babbage",
           "descartes", "nash", "fermat", "newton", "reimann", "leibniz",
           "hilbert", "neumann", "fourier", "fibonacci", "cantor", "noether",
           "poincare", "galois", "godel", "hardy", "ptolemy", "klein",
           "cauchy", "abel", "frege", "bhaskara", "eratosthenes", "khayyam",
           "laplace", "cayley", "napier", "bernoulli", "thales", "hipparchus",
           "fryer", "hypatia", "lovelace", "aryabhata", "ramanujan",
           "alkhwarizmi", "grothendieck", "perelman", "madhava", "germain",
           "hero", "yang", "seki"] #word possibilities

print("There will be", len(wordSet), "word possibilities.")
secretWord = random.choice(wordSet) #set secret word to a random word out of 4

usedLetters = "" #initialize used letters
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

for i in range (missingLetters):
    print("_", end=" ") #empty word line

print(" Used letters:", usedLetters) #output initial used letters

while attempts>0: #begin while loop to allow for continuous input, until no more attempts are left

    while True: #error proof input, allow for re-input if invalid or error
        try:
            newLetter = input("Guess a letter: ").lower() #input new letter
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
        print("You lost, the word was", secretWord, end=".") #you lose
    elif check==0: #if there are no unknown letters left
        print("You won!") #you win
        break #escape loop
    

            

