gofish
======

Go fish game 
This go fish game involves play against the computer.  Each player starts with 7 cards and takes turns asking eachother for cards.  The goal is to make sets (4 of a kind) and the game ends whenever someone runs out of cards or the end of the deck is reached.  The winner is the player that made the most sets.

To start the game simply run the command ./gofish.py on the command line while in the game directory.  (No compilation necessary) 

The game will prompt the user to ask for a card.  The user may simply type a card number in a standard deck (2-10, J, Q, K, A) and press enter to ask the computer for any given card in their hand.  If the opponent has one or more of that card in thier hand, all of them are given to the player requsting them, and that player gets to go again.  The program will handle input in a case-insensative manner, so capitalization does not matter.  In addition, the user may type either a numeric number or a number in word format (i.e. '2' or 'two') as input, and face cards can be entered by name or by the first letter of thier name (i.e. 'K' or 'king'). 

If an invalid number is entered (i.e. anything outside the 2-10 range or a letter other than J, Q, K, A), the program will provide an error message asking for a valid card and will allow the user to re-enter his/her card request.  I another invalid format is entered (i.e. a sentence instead of just a card value) the program will provide an error message asking for only a single card value, and allow the user to re-enter his/her card request.

The users hand and list of made sets are displayed each time the user has a turn and each time the user draws from the deck.  The users hand is displayed in order beginning at 2 and ending at Ace for convenience (aids user in counting the number of each card type that is present in current hand).  
