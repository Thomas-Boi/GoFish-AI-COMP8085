class Move:
    def __init__(self, asker: str, target: str, card: int):
        """
        Record a Move that was made. This is just a data container, no functionality.
        :param asker, name of the player that asked for the card.
        :param target, name of the target player that was asked for the card.
        :param card, card value.
        """
        self.asker = asker
        """
        Name of the player that asked for the card.
        """

        self.target = target
        """
        Name of the target player that was asked for the card.
        """

        self.card = card
        """
        Card value.
        """

        self.succeed = None
        """
        Whether the player succeeded.
        """

        self.amount = 0
        """
        The amount of cards the asker gotten from the target.
        """

        self.found_fours = False
        """
        Whether the asker found a four-of-a-kind as a result of the move.
        """

    def __str__(self) -> str:
        txt = f"{self.asker} asked {self.target} for {self.card}."
        if self.succeed is not None and self.amount is not None:
            succeed = 'successful' if self.succeed else 'not successful'
            txt += f"\nThe move was {succeed} and {self.asker} got {self.amount} cards of value '{self.card}'."

        if self.found_fours:
            txt += f"\n{self.asker} collected FOUR OF A KIND for {self.card}"
        return txt