import random
from card import Card

class Deck:
    def __init__(self):
        self.cards = []
        self.reset()
    
    def reset(self):
        """Create a new deck with all 52 cards."""
        self.cards = []
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self.cards.append(Card(suit, rank))
    
    def shuffle(self):
        """Randomly shuffle the deck."""
        random.shuffle(self.cards)
    
    def deal(self, num_players=4, cards_per_player=13):
        """Deal cards to players."""
        if num_players * cards_per_player > len(self.cards):
            raise ValueError("Not enough cards to deal")
        
        hands = [[] for _ in range(num_players)]
        for i in range(cards_per_player):
            for player in range(num_players):
                hands[player].append(self.cards.pop())
        
        # Sort each hand by suit and rank
        for hand in hands:
            self._sort_hand(hand)
        
        return hands
    
    def _sort_hand(self, hand):
        """Sort a hand by suit and rank."""
        # Sort by suit first (hearts, spades, diamonds, clubs) then by rank
        suit_order = {"hearts": 0, "spades": 1, "diamonds": 2, "clubs": 3}
        hand.sort(key=lambda card: (suit_order[card.suit], card.value))
        
    def __len__(self):
        return len(self.cards)
        
    def __str__(self):
        return str(self.cards) 