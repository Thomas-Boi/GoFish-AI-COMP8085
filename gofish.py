#!/usr/bin/env python3

import cards
import sys
import random
import time

deck = cards.Cards()
turn = "user"
faceCards = ['K', 'k', 'Q', 'q', 'J', 'j', 'A', 'a']
regCards = [2, 3, 4, 5, 6, 7, 8, 9, 10]
faceCard = 0

while len(deck.userhand) > 0 and len(deck.comphand) > 0 and len(deck.deck) > 0:
	if turn == "user":
		print("\n")
		deck.printHand()
		card = input("Ask me for a card: ")
		faceCard = 0

		if faceCards.count(card) == 0:
			card = int(card)
		else:
			card = card.upper()
			faceCard = 1

		if regCards.count(card) == 0 and faceCard == 0:
			print("Invalid input, please type a valid card")
		else:
			if deck.comphand.count(card) == 0:
				print("Go Fish")
				deck.drawCard("user")
				deck.checkForSet("user")
				deck.printHand()
				time.sleep(1)
				turn = "comp"
			else:
				print("Here's a " + str(card) + ". You get to go again!")
				deck.comphand.remove(card)
				deck.userhand.append(card)
				deck.checkForSet("user")
				time.sleep(1)
				turn = "user"

	if turn == "comp":
		print("\n")
		deck.printComp()
		card = random.choice(deck.comphand)
		print("Do you have any " + str(card) + "s")
		time.sleep(1)
		if deck.userhand.count(card) == 0:
			print("Went Fishing...Your turn")
			deck.drawCard("comp")
			deck.checkForSet("comp")
			time.sleep(1)
			turn = "user"
		else:
			print("Thanks for the " + str(card))
			deck.comphand.append(card)
			deck.userhand.remove(card)
			deck.checkForSet("comp")
			time.sleep(1)
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
