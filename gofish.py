#!/usr/bin/env python3

import cards
import sys
import random
import time

deck = cards.Cards()
turn = "user"
faceCards = ['K', 'Q', 'J', 'A']
regCards = [2, 3, 4, 5, 6, 7, 8, 9, 10]
numStrings = ['two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
faceStrings = ['King', 'Queen', 'Jack', 'Ace']
faceCard = 0

def processInput(user_input):
	cardType = -1
	try:
		if ' ' in user_input: 
			cardType = -2
		elif user_input.upper() in (card.upper() for card in faceCards):
			cardType = 1
		elif user_input.upper() in (card.upper() for card in faceStrings):
			cardType = 1
		elif user_input.upper() in (card.upper() for card in numStrings):
			cardType = 0
		elif int(user_input) in regCards:
			cardType = 0
		return cardType
	except ValueError:
		cardType = -2;
		return cardType

def adjustCard(cardType, user_input):
	if cardType == 0:
		if user_input.upper() in (card.upper() for card in numStrings):
			return int(regCards[numStrings.index(user_input)])
		else:
			return int(user_input)
	else:
		return user_input[0].upper()

def guessWrong(turn):
	deck.drawCard(turn)
	deck.checkForSet(turn)
	
	if turn == 'user':
		print("Go Fish!")
		deck.printHand()
	else:
		print("Went Fishing...Your Turn!")
		
	time.sleep(1)
		
def guessRight(turn, card, count, cardType):
	if cardType == 0:
		index = regCards.index(card)
		cardString = numStrings[index]
	else:
		index = faceCards.index(card)
		cardString = faceStrings[index]

	if count > 1:
		cardString = cardString + "s"
	
	if turn == 'user':
		print("I had " + str(count) + " " + cardString)
		print("You get to go again!")
	else:
		print("Thanks for the " + cardString)

	updateHand(count, card, turn)

def updateHand(count, card, turn):
	if turn == 'user':
		opp = 'comp'
	else:
		opp = 'user'

	while count > 0:
		deck.remove(opp, card)
		deck.append(turn, card)
		count = count - 1

	deck.checkForSet(turn)
	time.sleep(1)
		

while len(deck.userhand) > 0 and len(deck.comphand) > 0 and len(deck.deck) > 0:
	if turn == "user":
		print("\n")
		deck.printHand()
		
		user_input = input("Which card would you like to ask me for?: ")
		cardType = processInput(user_input)

		if cardType == -1:
			print("Invalid input, please ask for a valid card (i.e. 2 - 10, J, Q, K, A)")
		elif cardType == -2:
			print("Invalid input, please type only a single card")
		else:
			card = adjustCard(cardType, user_input)
			count = deck.comphand.count(card)
			if count == 0:
				guessWrong(turn)
				turn = "comp"
			else:
				guessRight(turn, card, count, cardType)
				turn = "user"

	if turn == "comp":
		print("\n")
		card = random.choice(deck.comphand)
		cardType = processInput(str(card))
		print("Do you have any " + str(card) + "s")
		count = deck.userhand.count(card)
		time.sleep(1)

		if count == 0:
			guessWrong(turn)
			turn = "user"
		else:
			guessRight(turn, card, count, cardType)
			turn = "comp"

print("\n")
print("GAME OVER...OUT OF CARDS")
numCompSets = len(deck.compsets)
numUserSets = len(deck.usersets)

print("You made " + str(numUserSets) + " sets")
print("I made " + str(numCompSets) + " sets")

if numCompSets > numUserSets:
	print("I WIN!")
elif numUserSets > numCompSets:
	print("YOU WIN!")
else:
	print("WE TIED!")	 
