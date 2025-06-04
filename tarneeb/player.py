import random

class Player:
    def __init__(self, name, player_id):
        self.name = name
        self.id = player_id
        self.hand = []
        self.team = player_id % 2  # Players 0,2 are team 0, Players 1,3 are team 1
        self.ai = True  # By default, all players are AI
    
    def set_hand(self, cards):
        self.hand = cards
        
    def has_suit(self, suit):
        """Check if player has any cards of the given suit."""
        return any(card.suit == suit for card in self.hand)
    
    def play_card(self, card_index):
        """Play a card from hand by index."""
        if 0 <= card_index < len(self.hand):
            return self.hand.pop(card_index)
        return None
    
    def get_valid_cards(self, leading_suit=None):
        """Get indices of valid cards that can be played."""
        if leading_suit is None or not self.has_suit(leading_suit):
            # No leading suit or doesn't have the suit, can play any card
            return list(range(len(self.hand)))
        
        # Must follow suit if possible
        return [i for i, card in enumerate(self.hand) if card.suit == leading_suit]
    
    def ai_bid(self, current_highest_bid, bids):
        """AI bidding strategy."""
        # Count high cards (A, K, Q) and trump potential
        high_cards = sum(1 for card in self.hand if card.rank in ["A", "K", "Q"])
        
        # Count cards by suit
        suit_counts = {suit: sum(1 for card in self.hand if card.suit == suit) 
                      for suit in ["clubs", "diamonds", "hearts", "spades"]}
        
        # Find most numerous suit for potential trump
        best_suit = max(suit_counts, key=suit_counts.get)
        strongest_suit_count = suit_counts[best_suit]
        
        # Calculate potential tricks
        potential_tricks = min(high_cards + strongest_suit_count // 2, 13)
        
        # Conservative bidding strategy
        if potential_tricks >= 9:
            bid = max(current_highest_bid + 1, 9)
        elif potential_tricks >= 8:
            bid = max(current_highest_bid + 1, 8)
        elif potential_tricks >= 7:
            bid = 7
        else:
            # Pass if hand is weak
            bid = 0
        
        # Don't exceed 13
        bid = min(bid, 13)
        
        # If we can't outbid, pass
        if bid <= current_highest_bid:
            return 0, None
        
        # Return bid and chosen trump suit
        return bid, best_suit
    
    def ai_play(self, trick, leading_suit, trump_suit):
        """AI card playing strategy."""
        valid_indices = self.get_valid_cards(leading_suit)
        
        if not valid_indices:
            return 0  # Shouldn't happen, but just in case
        
        # If we're the first to play in the trick
        if not trick:
            # Play highest non-trump card if possible
            non_trump_cards = [i for i in valid_indices if self.hand[i].suit != trump_suit]
            if non_trump_cards:
                return max(non_trump_cards, key=lambda i: self.hand[i].value)
            # Otherwise play lowest trump
            return min(valid_indices, key=lambda i: self.hand[i].value)
        
        # Get the highest card played so far
        highest_card = None
        for card in trick:
            if card is not None:
                if highest_card is None or card.beats(highest_card, leading_suit, trump_suit):
                    highest_card = card
        
        # Check if partner is winning
        partner_winning = False
        if len(trick) >= 3 and trick[len(trick) - 2] is not None:
            if highest_card == trick[len(trick) - 2]:
                partner_winning = True
        
        if partner_winning:
            # Partner is winning, play the lowest valid card
            return min(valid_indices, key=lambda i: self.hand[i].value)
        
        # Try to win the trick
        winning_cards = []
        for i in valid_indices:
            if self.hand[i].beats(highest_card, leading_suit, trump_suit):
                winning_cards.append(i)
        
        if winning_cards:
            # Play the lowest winning card
            return min(winning_cards, key=lambda i: self.hand[i].value)
        
        # Can't win, play the lowest card
        return min(valid_indices, key=lambda i: self.hand[i].value)
    
    def __str__(self):
        return f"Player {self.id}: {self.name}" 