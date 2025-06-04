from deck import Deck
from player import Player
import random

class TarneebGame:
    def __init__(self, target_score=31):
        self.deck = Deck()
        self.players = [
            Player("You", 0),
            Player("AI-1", 1),
            Player("Partner", 2),
            Player("AI-2", 3)
        ]
        self.players[0].ai = False  # First player is human
        
        self.current_player = 0
        self.dealer = random.randint(0, 3)
        self.target_score = target_score
        self.scores = {0: 0, 1: 0}  # Team scores
        self.reset_round()
    
    def reset_round(self):
        """Reset for a new round."""
        self.deck.reset()
        self.deck.shuffle()
        hands = self.deck.deal()
        
        for i, player in enumerate(self.players):
            player.set_hand(hands[i])
        
        # Start with player to the right of dealer
        self.current_player = (self.dealer + 1) % 4
        
        # Reset round variables
        self.bidding_phase = True
        self.trick_phase = False
        self.bids = [0, 0, 0, 0]
        self.highest_bid = 0
        self.highest_bidder = -1
        self.trump_suit = None
        self.tricks_won = {0: 0, 1: 0}  # Tricks won by each team
        self.current_trick = [None, None, None, None]
        self.leading_suit = None
        self.trick_winner = None
        self.trick_starter = self.current_player
    
    def next_player(self):
        """Move to the next player."""
        self.current_player = (self.current_player + 1) % 4
    
    def place_bid(self, bid, trump_suit=None):
        """Place a bid for the current player."""
        if not self.bidding_phase:
            return False
        
        # Players can only pass (bid 0) or outbid the highest bid
        if bid != 0 and bid <= self.highest_bid:
            return False
        
        # Bids must be between 7 and 13
        if bid != 0 and (bid < 7 or bid > 13):
            return False
        
        # Record the bid
        self.bids[self.current_player] = bid
        
        # Update highest bid if necessary
        if bid > self.highest_bid:
            self.highest_bid = bid
            self.highest_bidder = self.current_player
            self.trump_suit = trump_suit
        
        # Move to next player
        self.next_player()
        
        # Check if bidding is complete
        if self.current_player == self.trick_starter:
            if self.highest_bidder == -1:
                # No one bid, force dealer to bid 7
                self.highest_bid = 7
                self.highest_bidder = self.dealer
                # Simple AI chooses most common suit as trump
                suit_counts = {}
                for card in self.players[self.dealer].hand:
                    suit_counts[card.suit] = suit_counts.get(card.suit, 0) + 1
                self.trump_suit = max(suit_counts, key=suit_counts.get)
            
            # End bidding phase
            self.bidding_phase = False
            self.trick_phase = True
            self.current_player = self.trick_starter
        
        return True
    
    def play_card(self, card_index):
        """Play a card for the current player."""
        if not self.trick_phase:
            return False
        
        player = self.players[self.current_player]
        
        # Check if the card is valid to play
        valid_indices = player.get_valid_cards(self.leading_suit)
        if card_index not in valid_indices:
            return False
        
        # Play the card
        card = player.play_card(card_index)
        if card is None:
            return False
        
        # Set leading suit if this is the first card in the trick
        if self.leading_suit is None:
            self.leading_suit = card.suit
        
        # Add the card to the current trick
        self.current_trick[self.current_player] = card
        
        # We'll move to the next player, but we won't complete the trick immediately
        # That will be handled by the GUI after a delay
        self.next_player()
        
        # Flag for the GUI to know that the trick is complete and waiting for animation
        if self.current_trick.count(None) == 0:
            return "trick_complete"
        
        return True
    
    def complete_trick(self):
        """Complete the current trick and determine the winner."""
        # Find the winning card
        winning_card = None
        winner = None
        
        for i, card in enumerate(self.current_trick):
            if winning_card is None or card.beats(winning_card, self.leading_suit, self.trump_suit):
                winning_card = card
                winner = i
        
        # Update tricks won
        team = self.players[winner].team
        self.tricks_won[team] += 1
        
        # Set the winner as the starter of the next trick
        self.current_player = winner
        self.trick_starter = winner
        
        # Reset for next trick
        self.current_trick = [None, None, None, None]
        self.leading_suit = None
        self.trick_winner = winner
        
        # Check if round is over
        if all(len(player.hand) == 0 for player in self.players):
            self.score_round()
    
    def score_round(self):
        """Score the round."""
        bidding_team = self.players[self.highest_bidder].team
        bid = self.highest_bid
        
        # Check if bidding team made their bid
        if self.tricks_won[bidding_team] >= bid:
            self.scores[bidding_team] += self.tricks_won[bidding_team]
        else:
            self.scores[bidding_team] -= bid
        
        # Other team always scores their tricks
        other_team = 1 - bidding_team
        self.scores[other_team] += self.tricks_won[other_team]
        
        # Check if the game is over
        if self.is_over():
            # Game is over, don't start a new round
            self.bidding_phase = False
            self.trick_phase = False
            return
        
        # Prepare for next round
        self.dealer = (self.dealer + 1) % 4
        self.reset_round()
    
    def ai_turn(self):
        """Let AI take its turn."""
        player = self.players[self.current_player]
        
        if not player.ai:
            return False
        
        if self.bidding_phase:
            bid, suit = player.ai_bid(self.highest_bid, self.bids)
            self.place_bid(bid, suit)
        elif self.trick_phase:
            card_index = player.ai_play(
                [self.current_trick[i] for i in range(len(self.current_trick)) if i != self.current_player],
                self.leading_suit,
                self.trump_suit
            )
            return self.play_card(card_index)
        
        return True
    
    def is_over(self):
        """Check if game is over (a team reached the target score)."""
        return max(self.scores.values()) >= self.target_score
    
    def winner(self):
        """Return the winning team if game is over."""
        if self.scores[0] >= self.target_score:
            return 0
        elif self.scores[1] >= self.target_score:
            return 1
        return None 