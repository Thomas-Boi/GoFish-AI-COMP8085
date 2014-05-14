import random

class Cards:
	"""A standard deck of cards"""
	
	def __init__(self):
		self.deck = []
		self.comphand = []
		self.compsets = []
		self.userhand = []
		self.usersets = []

		for x in range(2, 15):
			for y in range(1, 5):
				if x == 11:
					self.deck.append('J')
				elif x == 12:
					self.deck.append('Q')
				elif x == 13:
					self.deck.append('K')
				elif x == 14:
					self.deck.append('A')
				else:
					self.deck.append(x)
		
		for x in range(0, 7):
			card = random.choice(self.deck)
			self.comphand.append(card)
			self.deck.remove(card)

		for x in range(0, 7):
			card = random.choice(self.deck)
			self.userhand.append(card)
			self.deck.remove(card)
	
	def remove(self, turn, card):
		if turn == 'user':
			self.userhand.remove(card)
		else:
			self.comphand.remove(card)

	def append(self, turn, card):
		if turn == 'user': 
			self.userhand.append(card)
		else:
			self.comphand.append(card)
	
	def printHand(self):
		temp = []
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

		#user_str = str(self.userhand).strip('[]')
		sets_str = str(self.usersets).strip('[]')
		print("Your Hand: " + user_str.replace("'", ""))
		print("Your Sets: " + sets_str.replace("'", ""))
	  
	def drawCard(self, player):
		card = random.choice(self.deck)
		self.deck.remove(card)
		if player == "comp":
			self.comphand.append(card)
		else:
			self.userhand.append(card)
			
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

	def printComp(self):
		comp_str = str(self.compsets).strip('[]')
		print("My Sets: " + comp_str.replace("'", ""))
