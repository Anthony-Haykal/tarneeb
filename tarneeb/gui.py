import pygame
import os
import math
from card import Card

# Define colors
GREEN = (16, 109, 16)
DARKER_GREEN = (10, 90, 10)
DARK_GREEN = (0, 77, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
RED = (200, 0, 0)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)

class GUI:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.width, self.height = screen.get_size()
        self.font = pygame.font.SysFont('Arial', 32)
        self.small_font = pygame.font.SysFont('Arial', 24)
        self.tiny_font = pygame.font.SysFont('Arial', 16)
        
        self.card_images = {}
        self.card_back = None
        self.load_card_images()
        
        self.bid_buttons = []
        self.trump_buttons = []
        self.bid_selected = 0
        self.trump_selected = None
        self.create_bid_buttons()
        self.create_trump_buttons()
        
        self.player_areas = self.create_player_areas()
        self.card_width = 80
        self.card_height = 116
        
        self.message = ""
        self.message_timer = 0
        
        # Areas where cards are played on table
        self.play_areas = [
            (self.width // 2, self.height // 2 + 80),     # Bottom (human)
            (self.width // 2 - 100, self.height // 2),    # Left
            (self.width // 2, self.height // 2 - 80),     # Top
            (self.width // 2 + 100, self.height // 2),    # Right
        ]
        
        # Keep track of animations/state
        self.waiting_time = 0
        self.ai_thinking = False
        self.trick_collection_time = 0
        self.trick_complete_delay = 0
        self.trick_winner_idx = None
        
    def load_card_images(self):
        """Load card images."""
        self.card_back = None
        try:
            # Try to load from assets folder
            cards_path = os.path.join("assets", "cards")
            for suit in Card.SUITS:
                for rank in Card.RANKS:
                    img_path = os.path.join(cards_path, f"{rank}_of_{suit}.png")
                    if os.path.exists(img_path):
                        img = pygame.image.load(img_path)
                        img = pygame.transform.scale(img, (80, 116))
                        self.card_images[(suit, rank)] = img
            
            # Load card back
            card_back_path = os.path.join(cards_path, "card_back.png")
            if os.path.exists(card_back_path):
                self.card_back = pygame.image.load(card_back_path)
                self.card_back = pygame.transform.scale(self.card_back, (80, 116))
        except:
            # If loading fails, create placeholder colored rectangles
            print("Failed to load card images, using placeholder rectangles")
            colors = {
                "clubs": (0, 0, 0),       # Black
                "diamonds": (255, 0, 0),  # Red
                "hearts": (255, 0, 0),    # Red
                "spades": (0, 0, 0)       # Black
            }
            
            for suit in Card.SUITS:
                for rank in Card.RANKS:
                    # Create a surface for this card
                    img = pygame.Surface((80, 116))
                    img.fill(WHITE)  # White background
                    
                    # Draw a colored border
                    pygame.draw.rect(img, colors[suit], pygame.Rect(0, 0, 80, 116), 2)
                    
                    # Draw the rank and suit
                    font = pygame.font.SysFont('Arial', 20)
                    text_color = colors[suit]
                    rank_text = font.render(rank, True, text_color)
                    suit_text = font.render(Card.SUIT_SYMBOLS[suit], True, text_color)
                    
                    img.blit(rank_text, (5, 5))
                    img.blit(suit_text, (5, 30))
                    img.blit(rank_text, (60, 90))
                    img.blit(suit_text, (60, 65))
                    
                    self.card_images[(suit, rank)] = img
        
        # Always create card back if it wasn't loaded from file
        if self.card_back is None:
            # Create card back
            self.card_back = pygame.Surface((80, 116))
            self.card_back.fill((180, 0, 0))  # Red background
            pygame.draw.rect(self.card_back, BLACK, pygame.Rect(5, 5, 70, 106), 2)
            
            # Create a pattern on the card back
            for i in range(0, 80, 10):
                for j in range(0, 116, 10):
                    if (i + j) % 20 == 0:
                        pygame.draw.rect(self.card_back, (150, 0, 0), pygame.Rect(i, j, 5, 5))
    
    def create_player_areas(self):
        """Define areas where player info and cards are displayed."""
        center_x, center_y = self.width // 2, self.height // 2
        return [
            pygame.Rect(center_x - 200, self.height - 150, 400, 150),  # Bottom (human)
            pygame.Rect(0, center_y - 100, 150, 200),                  # Left
            pygame.Rect(center_x - 200, 0, 400, 150),                  # Top
            pygame.Rect(self.width - 150, center_y - 100, 150, 200),   # Right
        ]
    
    def create_bid_buttons(self):
        """Create buttons for bidding."""
        button_width = 70
        button_height = 70
        start_x = (self.width - button_width * 3) // 2
        start_y = self.height // 2 - button_height * 2
        
        # Create buttons from 7 to 13
        self.bid_buttons = []
        for i in range(7, 14):
            row = (i - 7) // 3
            col = (i - 7) % 3
            x = start_x + col * button_width
            y = start_y + row * button_height
            self.bid_buttons.append((i, pygame.Rect(x, y, button_width, button_height)))
        
        # Add pass button (0)
        self.bid_buttons.append((0, pygame.Rect(start_x + button_width, start_y + 3 * button_height, button_width, button_height)))
    
    def create_trump_buttons(self):
        """Create buttons for selecting trump suit."""
        button_width = 70
        button_height = 70
        start_x = (self.width - button_width * 2) // 2
        start_y = self.height // 2 + 20
        
        suits = ["clubs", "diamonds", "hearts", "spades"]
        self.trump_buttons = []
        
        for i, suit in enumerate(suits):
            row = i // 2
            col = i % 2
            x = start_x + col * button_width
            y = start_y + row * button_height
            self.trump_buttons.append((suit, pygame.Rect(x, y, button_width, button_height)))
    
    def draw(self):
        """Draw the game screen."""
        # Draw background
        self.screen.fill(DARK_GREEN)
        
        # Draw card table (rounded rectangle)
        table_rect = pygame.Rect(self.width // 6, self.height // 6, 
                                self.width * 2 // 3, self.height * 2 // 3)
        pygame.draw.rect(self.screen, GREEN, table_rect, border_radius=50)
        pygame.draw.rect(self.screen, DARKER_GREEN, table_rect, 5, border_radius=50)
        
        # Draw scores
        self.draw_scores()
        
        # Draw player areas, hands and played cards
        self.draw_players()
        
        # Draw current trick cards
        self.draw_current_trick()
        
        # Draw bidding UI if in bidding phase
        if self.game.bidding_phase:
            self.draw_bidding_ui()
        
        # Draw messages
        self.draw_message()
        
        # Draw trump indicator if trump has been selected
        if self.game.trump_suit:
            self.draw_trump_indicator()
    
    def draw_scores(self):
        """Draw the score display."""
        # Draw team scores at the top
        team1_text = f"Team 1: {self.game.scores[0]}"
        team2_text = f"Team 2: {self.game.scores[1]}"
        
        team1_surf = self.font.render(team1_text, True, WHITE)
        team2_surf = self.font.render(team2_text, True, WHITE)
        
        self.screen.blit(team1_surf, (20, 20))
        self.screen.blit(team2_surf, (self.width - 20 - team2_surf.get_width(), 20))
        
        # Draw current trick count if in trick phase
        if self.game.trick_phase:
            tricks_text = f"Tricks - Team 1: {self.game.tricks_won[0]} | Team 2: {self.game.tricks_won[1]}"
            tricks_surf = self.small_font.render(tricks_text, True, WHITE)
            self.screen.blit(tricks_surf, (self.width // 2 - tricks_surf.get_width() // 2, 60))
            
            # Draw the bid information
            bid_text = f"Bid: {self.game.highest_bid} by {self.game.players[self.game.highest_bidder].name}"
            bid_surf = self.small_font.render(bid_text, True, GOLD)
            self.screen.blit(bid_surf, (self.width // 2 - bid_surf.get_width() // 2, 30))
    
    def draw_players(self):
        """Draw player areas and hands."""
        for i, player in enumerate(self.game.players):
            area = self.player_areas[i]
            
            # Highlight current player
            if i == self.game.current_player:
                pygame.draw.rect(self.screen, GOLD, area, 3, border_radius=10)
            else:
                pygame.draw.rect(self.screen, WHITE, area, 1, border_radius=10)
            
            # Draw player name
            name_surf = self.small_font.render(player.name, True, WHITE)
            if i == 0:  # Bottom
                self.screen.blit(name_surf, (area.centerx - name_surf.get_width() // 2, area.y + 5))
                self.draw_player_hand(player, area, True)
            elif i == 1:  # Left
                self.screen.blit(name_surf, (area.x + 5, area.y + 5))
                self.draw_player_hand(player, area, False)
            elif i == 2:  # Top
                self.screen.blit(name_surf, (area.centerx - name_surf.get_width() // 2, area.y + 5))
                self.draw_player_hand(player, area, False)
            elif i == 3:  # Right
                self.screen.blit(name_surf, (area.x + 5, area.y + 5))
                self.draw_player_hand(player, area, False)
            
            # Draw bid if in bidding phase
            if self.game.bidding_phase and self.game.bids[i] > 0:
                bid_surf = self.font.render(str(self.game.bids[i]), True, GOLD)
                if i == 0:  # Bottom
                    self.screen.blit(bid_surf, (area.centerx - bid_surf.get_width() // 2, area.y + 35))
                elif i == 1:  # Left
                    self.screen.blit(bid_surf, (area.x + 5, area.y + 35))
                elif i == 2:  # Top
                    self.screen.blit(bid_surf, (area.centerx - bid_surf.get_width() // 2, area.y + 35))
                elif i == 3:  # Right
                    self.screen.blit(bid_surf, (area.x + 5, area.y + 35))
    
    def draw_player_hand(self, player, area, is_human):
        """Draw a player's hand of cards."""
        hand = player.hand
        
        if not hand:
            return
        
        if is_human:  # Bottom player (human)
            # Calculate card spacing and position
            card_width = self.card_width
            spacing = min(card_width, (area.width - card_width) / max(1, len(hand) - 1))
            start_x = area.centerx - (spacing * (len(hand) - 1) + card_width) // 2
            
            # Draw each card
            for i, card in enumerate(hand):
                x = start_x + i * spacing
                y = area.y + 30
                
                # Draw card
                if self.card_images.get((card.suit, card.rank)):
                    img = self.card_images[(card.suit, card.rank)]
                    self.screen.blit(img, (x, y))
                else:
                    # Fallback if image not found
                    card_rect = pygame.Rect(x, y, card_width, self.card_height)
                    pygame.draw.rect(self.screen, WHITE, card_rect)
                    pygame.draw.rect(self.screen, BLACK, card_rect, 2)
                    
                    # Determine the color based on suit
                    text_color = RED if card.suit in ["hearts", "diamonds"] else BLACK
                    
                    # Render the card text
                    text = self.small_font.render(str(card), True, text_color)
                    self.screen.blit(text, (x + 5, y + 5))
                
                # If it's player's turn in trick phase, highlight valid cards
                if is_human and self.game.current_player == 0 and self.game.trick_phase:
                    valid_indices = player.get_valid_cards(self.game.leading_suit)
                    if i in valid_indices:
                        highlight_rect = pygame.Rect(x, y, card_width, self.card_height)
                        pygame.draw.rect(self.screen, GOLD, highlight_rect, 3)
        else:  # AI players
            # Draw card backs
            if player.id == 1:  # Left
                # Vertical arrangement
                spacing = min(30, (area.height - self.card_height) / max(1, len(hand) - 1))
                start_y = area.centery - (spacing * (len(hand) - 1) + self.card_height) // 2
                
                for i in range(len(hand)):
                    x = area.x + 40
                    y = start_y + i * spacing
                    self.screen.blit(self.card_back, (x, y))
            
            elif player.id == 2:  # Top
                # Horizontal arrangement
                card_width = self.card_width
                spacing = min(card_width, (area.width - card_width) / max(1, len(hand) - 1))
                start_x = area.centerx - (spacing * (len(hand) - 1) + card_width) // 2
                
                for i in range(len(hand)):
                    x = start_x + i * spacing
                    y = area.y + 30
                    self.screen.blit(self.card_back, (x, y))
            
            elif player.id == 3:  # Right
                # Vertical arrangement
                spacing = min(30, (area.height - self.card_height) / max(1, len(hand) - 1))
                start_y = area.centery - (spacing * (len(hand) - 1) + self.card_height) // 2
                
                for i in range(len(hand)):
                    x = area.right - 40 - self.card_width
                    y = start_y + i * spacing
                    self.screen.blit(self.card_back, (x, y))
    
    def draw_current_trick(self):
        """Draw cards played in the current trick."""
        if not self.game.trick_phase:
            return
        
        # Draw a hint circle in the center of the table
        center_x, center_y = self.width // 2, self.height // 2
        pygame.draw.circle(self.screen, DARKER_GREEN, (center_x, center_y), 150, 2)
        
        # Small offset to prevent card overlap
        offsets = [(0, 5), (-5, 0), (0, -5), (5, 0)]  # Bottom, Left, Top, Right
        
        for i, card in enumerate(self.game.current_trick):
            if card is None:
                continue
            
            # Get position for this player's card
            x, y = self.play_areas[i]
            
            # Apply the offset
            x += offsets[i][0]
            y += offsets[i][1]
            
            # Highlight card with a glow effect
            highlight_rect = pygame.Rect(x - self.card_width // 2 - 2, y - self.card_height // 2 - 2, 
                                     self.card_width + 4, self.card_height + 4)
            pygame.draw.rect(self.screen, GOLD, highlight_rect, border_radius=3)
            
            # Draw card
            if self.card_images.get((card.suit, card.rank)):
                img = self.card_images[(card.suit, card.rank)]
                rect = img.get_rect(center=(x, y))
                self.screen.blit(img, rect)
            else:
                # Fallback
                card_rect = pygame.Rect(x - self.card_width // 2, y - self.card_height // 2, 
                                      self.card_width, self.card_height)
                pygame.draw.rect(self.screen, WHITE, card_rect)
                pygame.draw.rect(self.screen, BLACK, card_rect, 2)
                
                # Determine the color based on suit
                text_color = RED if card.suit in ["hearts", "diamonds"] else BLACK
                
                # Render the card text
                text = self.small_font.render(str(card), True, text_color)
                self.screen.blit(text, (x - self.card_width // 2 + 5, y - self.card_height // 2 + 5))
    
    def draw_bidding_ui(self):
        """Draw the bidding UI when in bidding phase."""
        # Only show bidding UI if it's the human player's turn
        if self.game.current_player != 0:
            waiting_text = f"Waiting for {self.game.players[self.game.current_player].name} to bid..."
            waiting_surf = self.font.render(waiting_text, True, WHITE)
            self.screen.blit(waiting_surf, (self.width // 2 - waiting_surf.get_width() // 2, 
                                         self.height // 2 - waiting_surf.get_height() // 2))
            return
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Black with 150 alpha (semi-transparent)
        self.screen.blit(overlay, (0, 0))
        
        # Draw bid selection UI
        title_surf = self.font.render("Choose your bid", True, WHITE)
        self.screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 
                                    self.height // 2 - 150))
        
        # Draw bid buttons
        for bid, rect in self.bid_buttons:
            # Choose color based on selection and validity
            if bid == self.bid_selected:
                color = GOLD
            else:
                color = LIGHT_GRAY
            
            # Make button red if bid is too low
            if bid != 0 and bid <= self.game.highest_bid:
                color = RED
            
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            pygame.draw.rect(self.screen, BLACK, rect, 2, border_radius=10)
            
            # Draw bid value
            text = str(bid) if bid > 0 else "Pass"
            text_surf = self.font.render(text, True, BLACK)
            self.screen.blit(text_surf, (rect.centerx - text_surf.get_width() // 2, 
                                       rect.centery - text_surf.get_height() // 2))
        
        # Draw highest bid
        if self.game.highest_bid > 0:
            highest_text = f"Highest bid: {self.game.highest_bid} by {self.game.players[self.game.highest_bidder].name}"
            highest_surf = self.small_font.render(highest_text, True, WHITE)
            self.screen.blit(highest_surf, (self.width // 2 - highest_surf.get_width() // 2, 
                                         self.height // 2 - 180))
        
        # If a bid is selected and it's higher than current highest bid, show trump selection
        if self.bid_selected > 0 and self.bid_selected > self.game.highest_bid:
            trump_title = self.font.render("Choose Trump Suit", True, WHITE)
            self.screen.blit(trump_title, (self.width // 2 - trump_title.get_width() // 2, 
                                        self.height // 2 - 10))
            
            # Draw trump buttons
            for suit, rect in self.trump_buttons:
                # Choose color based on selection
                if suit == self.trump_selected:
                    color = GOLD
                else:
                    color = WHITE
                
                pygame.draw.rect(self.screen, color, rect, border_radius=10)
                pygame.draw.rect(self.screen, BLACK, rect, 2, border_radius=10)
                
                # Draw suit symbol
                symbol = Card.SUIT_SYMBOLS[suit]
                symbol_color = RED if suit in ["hearts", "diamonds"] else BLACK
                symbol_surf = self.font.render(symbol, True, symbol_color)
                self.screen.blit(symbol_surf, (rect.centerx - symbol_surf.get_width() // 2, 
                                            rect.centery - symbol_surf.get_height() // 2))
            
            # Draw confirm button if both bid and trump are selected
            if self.trump_selected is not None:
                confirm_rect = pygame.Rect(self.width // 2 - 75, self.height // 2 + 180, 150, 40)
                pygame.draw.rect(self.screen, GREEN, confirm_rect, border_radius=10)
                pygame.draw.rect(self.screen, BLACK, confirm_rect, 2, border_radius=10)
                
                confirm_text = self.font.render("Confirm", True, WHITE)
                self.screen.blit(confirm_text, (confirm_rect.centerx - confirm_text.get_width() // 2, 
                                              confirm_rect.centery - confirm_text.get_height() // 2))
    
    def draw_trump_indicator(self):
        """Draw the trump suit indicator."""
        if not self.game.trump_suit:
            return
        
        # Draw a badge showing the trump suit
        trump_rect = pygame.Rect(20, 70, 60, 60)
        pygame.draw.rect(self.screen, WHITE, trump_rect, border_radius=30)
        
        # Draw the suit symbol
        symbol = Card.SUIT_SYMBOLS[self.game.trump_suit]
        symbol_color = RED if self.game.trump_suit in ["hearts", "diamonds"] else BLACK
        symbol_surf = self.font.render(symbol, True, symbol_color)
        self.screen.blit(symbol_surf, (trump_rect.centerx - symbol_surf.get_width() // 2, 
                                      trump_rect.centery - symbol_surf.get_height() // 2))
        
        # Draw "Trump" text
        trump_text = self.tiny_font.render("Trump", True, BLACK)
        self.screen.blit(trump_text, (trump_rect.centerx - trump_text.get_width() // 2, 
                                     trump_rect.bottom + 5))
    
    def draw_message(self):
        """Draw message to player."""
        if self.message and self.message_timer > 0:
            # Create a semi-transparent background
            msg_surf = self.font.render(self.message, True, WHITE)
            bg_rect = msg_surf.get_rect(center=(self.width // 2, self.height - 50))
            bg_rect.inflate_ip(20, 10)
            
            # Draw background and text
            pygame.draw.rect(self.screen, (0, 0, 0, 150), bg_rect)
            self.screen.blit(msg_surf, msg_surf.get_rect(center=(self.width // 2, self.height - 50)))
    
    def handle_event(self, event):
        """Handle pygame events."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Handle mouse clicks
            pos = pygame.mouse.get_pos()
            
            # Human player's turn
            if self.game.current_player == 0:
                if self.game.bidding_phase:
                    self.handle_bidding_click(pos)
                elif self.game.trick_phase:
                    self.handle_card_click(pos)
        
        # Update timers
        if event.type == pygame.USEREVENT:
            if self.message_timer > 0:
                self.message_timer -= 1
            
            # Handle AI turns - but don't run AI if we're in a delay
            if self.game.current_player != 0 and not self.ai_thinking and self.trick_complete_delay == 0:
                self.waiting_time += 1
                if self.waiting_time >= 10:  # Wait a bit before AI makes its move
                    result = self.game.ai_turn()
                    self.waiting_time = 0
                    
                    # Check if trick is complete after AI plays
                    if result == "trick_complete":
                        self.trick_complete_delay = 30  # Wait for about 3 seconds before completing the trick
            
            # Handle trick completion delay
            if self.trick_complete_delay > 0:
                self.trick_complete_delay -= 1
                if self.trick_complete_delay == 0:
                    # Now complete the trick
                    self.game.complete_trick()
            
            # Handle trick collection
            if self.trick_collection_time > 0:
                self.trick_collection_time -= 1
                if self.trick_collection_time == 0 and self.trick_winner_idx is not None:
                    # Resume game after trick collection animation
                    self.trick_winner_idx = None
    
    def handle_bidding_click(self, pos):
        """Handle clicks during bidding phase."""
        # Check bid buttons
        for bid, rect in self.bid_buttons:
            if rect.collidepoint(pos):
                # Can't select a bid lower than current highest (except pass)
                if bid != 0 and bid <= self.game.highest_bid:
                    self.show_message("Bid must be higher than current highest bid")
                    return
                
                self.bid_selected = bid
                
                # If Pass is selected, immediately pass without requiring trump selection
                if bid == 0:
                    self.game.place_bid(0, None)
                    self.bid_selected = 0
                    self.trump_selected = None
                    return
                
                # Clear trump selection if a new bid is selected
                self.trump_selected = None
                return
        
        # Check trump buttons if a valid bid is selected
        if self.bid_selected > 0 and self.bid_selected > self.game.highest_bid:
            for suit, rect in self.trump_buttons:
                if rect.collidepoint(pos):
                    self.trump_selected = suit
                    return
            
            # Check confirm button
            if self.trump_selected is not None:
                confirm_rect = pygame.Rect(self.width // 2 - 75, self.height // 2 + 180, 150, 40)
                if confirm_rect.collidepoint(pos):
                    # Place bid
                    self.game.place_bid(self.bid_selected, self.trump_selected)
                    self.bid_selected = 0
                    self.trump_selected = None
                    return
    
    def handle_card_click(self, pos):
        """Handle clicks during trick phase."""
        # Only handle clicks if it's human player's turn
        if self.game.current_player != 0 or not self.game.trick_phase:
            return
        
        player = self.game.players[0]
        hand = player.hand
        
        if not hand:
            return
        
        # Calculate card spacing and position
        area = self.player_areas[0]
        card_width = self.card_width
        spacing = min(card_width, (area.width - card_width) / max(1, len(hand) - 1))
        start_x = area.centerx - (spacing * (len(hand) - 1) + card_width) // 2
        
        # Check for clicks in reverse order (to prioritize cards rendered on top)
        # This helps when cards overlap slightly due to tight spacing
        for i in range(len(hand) - 1, -1, -1):
            x = start_x + i * spacing
            y = area.y + 30
            
            # Define hitbox - slightly narrower on the sides to prevent overlap issues
            # Keep left edge accurate but reduce right edge width for overlapped cards
            edge_margin = 15 if i < len(hand) - 1 else 0  # Reduce width except for rightmost card
            card_rect = pygame.Rect(x, y, card_width - edge_margin, self.card_height)
            
            if card_rect.collidepoint(pos):
                # Try to play this card
                valid_indices = player.get_valid_cards(self.game.leading_suit)
                if i in valid_indices:
                    result = self.game.play_card(i)
                    # Check if trick is complete
                    if result == "trick_complete":
                        self.trick_complete_delay = 30  # About 3 seconds
                else:
                    # Card is not valid, show message
                    if self.game.leading_suit:
                        self.show_message(f"You must follow the leading suit ({self.game.leading_suit})")
                return
    
    def show_message(self, msg, duration=180):
        """Display a message to the player."""
        self.message = msg
        # If duration is 0, message stays until explicitly cleared
        self.message_timer = duration if duration > 0 else float('inf') 