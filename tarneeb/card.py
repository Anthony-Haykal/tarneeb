class Card:
    SUITS = ["clubs", "diamonds", "hearts", "spades"]
    RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    SUIT_SYMBOLS = {"clubs": "♣", "diamonds": "♦", "hearts": "♥", "spades": "♠"}
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.visible = False
        self.image = None
        self.small_image = None
    
    def __str__(self):
        return f"{self.rank}{self.SUIT_SYMBOLS[self.suit]}"
    
    def __repr__(self):
        return self.__str__()
    
    @property
    def value(self):
        return Card.RANKS.index(self.rank)
    
    def beats(self, other, leading_suit, trump_suit):
        # If the other card is None, this card wins by default
        if other is None:
            return True
        
        # Both cards are trump, higher trump wins
        if self.suit == trump_suit and other.suit == trump_suit:
            return self.value > other.value
        
        # Only this card is trump, it wins
        if self.suit == trump_suit and other.suit != trump_suit:
            return True
        
        # Only other card is trump, it wins
        if self.suit != trump_suit and other.suit == trump_suit:
            return False
        
        # Neither is trump, check if they match the leading suit
        if self.suit == leading_suit and other.suit == leading_suit:
            return self.value > other.value
        
        # This card follows suit, other doesn't - this card wins
        if self.suit == leading_suit and other.suit != leading_suit:
            return True
        
        # This card doesn't follow suit, other does - other card wins
        if self.suit != leading_suit and other.suit == leading_suit:
            return False
        
        # Neither follows suit and neither is trump - higher card of leading suit wins
        # But in this case, the first played card is considered the winner
        return False 