import random

#class to create a deck of cards
class Cards:
	"""A standard deck of cards"""
	
	def __init__(self):	#create 
		self.deck = []		#current deck
		self.comphand = []	#computers hand
		self.compsets = []	#computers made sets (4 of a kind)
		self.userhand = []	#users hand
		self.usersets = []	#users made sets

		#add 4 of each card to the deck
		for x in range(2, 15):	#each type of card (2-10, J, Q, K, A)
			for y in range(1, 5):	#4 of each type in a deck
				if x == 11:	#jack
					self.deck.append('J')
				elif x == 12:	#queen
					self.deck.append('Q')
				elif x == 13:	#king
					self.deck.append('K')
				elif x == 14:	#ace
					self.deck.append('A')
				else:		#2-10
					self.deck.append(x)

		#select 7 random cards from the deck for the computer
		for x in range(0, 7):
			card = random.choice(self.deck)
			self.comphand.append(card)
			self.deck.remove(card)
		
		#select 7 random cards from the deck for the user
		for x in range(0, 7):
			card = random.choice(self.deck)
			self.userhand.append(card)
			self.deck.remove(card)
	
	#remove 'card' from hand of current 'turn'
	def remove(self, turn, card):
		if turn == 'user':
			self.userhand.remove(card)
		else:
			self.comphand.remove(card)

	#append 'card' to hand of current 'turn'
	def append(self, turn, card):
		if turn == 'user': 
			self.userhand.append(card)
		else:
			self.comphand.append(card)
	
	#print users current hand in order from 2 to Ace
	def printHand(self):
		user_str = " "
		for x in range(2, 15):
			if x == 11:
				curr = 'J'
			elif x == 12:
				curr = 'Q'
			elif x == 13: 
				curr = 'K'
			elif x == 14:
				curr = 'A'
			else:
				curr = str(x)

			if x < 11:
				count = self.userhand.count(x)
			else:
				count = self.userhand.count(curr)

			while count > 0:
				user_str = user_str + curr + ", "
				count = count - 1

		sets_str = str(self.usersets).strip('[]')
		print("Your Hand: " + user_str.replace("'", ""))
		print("Your Sets: " + sets_str.replace("'", ""))
	  
	#draw a random card from the deck on a wrong guess
	def drawCard(self, player):
		card = random.choice(self.deck)
		self.deck.remove(card)
		if player == "comp":
			self.comphand.append(card)
		else:
			self.userhand.append(card)
			
	#check if a set has been made
	def checkForSet(self, player):
		if player == "user":
			for c in self.userhand:
				num = self.userhand.count(c)
				if num == 4:
					for x in range(0, 4):
						self.userhand.remove(c)
					self.usersets.append(c)
		else:
			for c in self.comphand:
				num = self.comphand.count(c)
				if num == 4:
					for x in range(0, 4):
						self.comphand.remove(c)
					self.compsets.append(c)
	
	#print computer sets - removed call to this function as suggested in peer review
	#but left the function here so it could be re-implemented if the player desired
	def printComp(self):
		comp_str = str(self.compsets).strip('[]')
		print("My Sets: " + comp_str.replace("'", ""))
