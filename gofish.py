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

#Determine the type of card 
def processInput(user_input):
	cardType = -1
	try:
		if ' ' in user_input:
			cardType = -2	#invalid format
		elif user_input.upper() in (card.upper() for card in faceCards):
			cardType = 1	#face card
		elif user_input.upper() in (card.upper() for card in faceStrings):
			cardType = 1	#face card
		elif user_input.upper() in (card.upper() for card in numStrings):
			cardType = 0	#number card
		elif int(user_input) in regCards:
			cardType = 0	#number card
		return cardType
	except ValueError:	#catch exceptions 
		cardType = -2;	#invalid format
		return cardType

#Return either a number (2-10) or J, Q, K, A for display
def adjustCard(cardType, user_input):
	if cardType == 0:	#number card - return int value
		if user_input.upper() in (card.upper() for card in numStrings):
			return int(regCards[numStrings.index(user_input)])
		else:
			return int(user_input)
	else:	#face card - return first letter (K, Q, J, A)
		return user_input[0].upper()

#Handle an incorrect guess
def guessWrong(turn):
	deck.drawCard(turn)
	deck.checkForSet(turn)
	
	if turn == 'user':
		print("Go Fish!")
		deck.printHand()
	else:
		print("Went Fishing...Your Turn!")
		
	time.sleep(1)	#Delay 1 second for user to view output
		
#Handle a correct guess
def guessRight(turn, card, count, cardType):
	if cardType == 0:	#number card
		index = regCards.index(card)
		cardString = numStrings[index]	#word version of number
	else:			#face card
		index = faceCards.index(card)
		cardString = faceStrings[index]	#word version of face card

	if count > 1:
		cardString = cardString + "s"	#add s if there were multiples
	
	if turn == 'user':
		print("I had " + str(count) + " " + cardString)
		print("You get to go again!")
	else:
		print("Thanks for the " + cardString)

	updateHand(count, card, turn)		#update user and comp hands

#Update user and comp hands after a correct guess
def updateHand(count, card, turn):
	if turn == 'user':	#set the opponent
		opp = 'comp'
	else:
		opp = 'user'

	while count > 0:	#for however many of a particular card player had
		deck.remove(opp, card)		#remove from opponent
		deck.append(turn, card)		#give to player
		count = count - 1

	deck.checkForSet(turn)
	time.sleep(1)
		
#Game play continues until a player runs out of cards or the deck is empty
while len(deck.userhand) > 0 and len(deck.comphand) > 0 and len(deck.deck) > 0:
	if turn == "user":	#users turn
		print("\n")
		deck.printHand()	#print the users hand
		
		#ask user to guess and process input
		user_input = input("Which card would you like to ask me for?: ")
		cardType = processInput(user_input)

		if cardType == -1:	#provide error message
			print("Invalid input, please ask for a valid card (i.e. 2 - 10, J, Q, K, A)")
		elif cardType == -2:	#provide error message
			print("Invalid input, please type only a single card")
		else:
			card = adjustCard(cardType, user_input)
			count = deck.comphand.count(card)	#get number of times card appears in hand
			if count == 0:	#not in hand
				guessWrong(turn)
				turn = "comp"	#change turns
			else:	#was in opponents hand
				guessRight(turn, card, count, cardType)
				turn = "user"	#turn remains here

	if turn == "comp":	#computeres turn
		print("\n")
		card = random.choice(deck.comphand)	#select random card from hand to request
		cardType = processInput(str(card))
		print("Do you have any " + str(card) + "s")
		count = deck.userhand.count(card)	#number of times card appears in users hand
		time.sleep(1)

		if count == 0:	#not in users hand
			guessWrong(turn)
			turn = "user"	#change turns
		else:
			guessRight(turn, card, count, cardType)
			turn = "comp"	#turn remains here

#Once while loop terminates handle the end of the game
print("\n")
print("GAME OVER...OUT OF CARDS")
numCompSets = len(deck.compsets)
numUserSets = len(deck.usersets)

print("You made " + str(numUserSets) + " sets")
print("I made " + str(numCompSets) + " sets")

#determine winner based on number of sets
if numCompSets > numUserSets:
	print("I WIN!")
elif numUserSets > numCompSets:
	print("YOU WIN!")
else:
	print("WE TIED!")	 
