import pygame
import sys
from game import TarneebGame
from gui import GUI

def draw_start_screen(screen):
    """Draw the start screen with a start button."""
    width, height = screen.get_size()
    
    # Fill background
    screen.fill((0, 77, 0))  # Dark green
    
    # Draw title
    font_title = pygame.font.SysFont('Arial', 64, bold=True)
    title_text = font_title.render("TARNEEB", True, (255, 215, 0))  # Gold text
    screen.blit(title_text, (width//2 - title_text.get_width()//2, height//4))
    
    # Draw subtitle
    font_subtitle = pygame.font.SysFont('Arial', 24)
    subtitle_text = font_subtitle.render("The Classic Middle Eastern Card Game", True, (255, 255, 255))
    screen.blit(subtitle_text, (width//2 - subtitle_text.get_width()//2, height//4 + 80))
    
    # Draw start button
    button_width, button_height = 200, 60
    button_rect = pygame.Rect(width//2 - button_width//2, height//2 + 50, button_width, button_height)
    pygame.draw.rect(screen, (16, 109, 16), button_rect, border_radius=15)  # Green button
    pygame.draw.rect(screen, (255, 215, 0), button_rect, 3, border_radius=15)  # Gold border
    
    # Draw button text
    font_button = pygame.font.SysFont('Arial', 32, bold=True)
    button_text = font_button.render("START", True, (255, 255, 255))
    screen.blit(button_text, (button_rect.centerx - button_text.get_width()//2, 
                             button_rect.centery - button_text.get_height()//2))
    
    # Draw instruction
    font_instr = pygame.font.SysFont('Arial', 18)
    instr_text = font_instr.render("Click START to begin the game", True, (200, 200, 200))
    screen.blit(instr_text, (width//2 - instr_text.get_width()//2, height//2 + 130))
    
    # Draw game info
    font_info = pygame.font.SysFont('Arial', 16)
    info_texts = [
        "• 4 players (2 teams of 2)",
        "• First team to 31 points wins",
        "• Minimum bid is 7 tricks",
        "• Follow suit if possible"
    ]
    
    for i, text in enumerate(info_texts):
        info_surf = font_info.render(text, True, (220, 220, 220))
        screen.blit(info_surf, (width//2 - 100, height//2 + 170 + i*25))
    
    return button_rect

def main():
    pygame.init()
    pygame.display.set_caption("Tarneeb")
    
    # Set up screen
    screen_width = 800
    screen_height = 600
    if pygame.display.get_desktop_sizes()[0][1] >= 800:
        screen_height = 800
    
    screen = pygame.display.set_mode((screen_width, screen_height))
    
    # Start screen state
    in_start_screen = True
    start_button_rect = None
    
    # Game state
    game = None
    gui = None
    game_over = False
    
    # Set up a timer for AI thinking/animations
    pygame.time.set_timer(pygame.USEREVENT, 100)  # Fire every 100ms
    
    # Game loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle start screen
            if in_start_screen:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if start_button_rect and start_button_rect.collidepoint(event.pos):
                        # Start the game
                        game = TarneebGame()
                        gui = GUI(screen, game)
                        in_start_screen = False
            # Handle game or game over state
            elif game is not None:
                # Only process game events if game is not over
                if not game_over:
                    gui.handle_event(event)
                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    # Start a new game if game is over and player clicks or presses a key
                    game = TarneebGame()
                    gui = GUI(screen, game)
                    game_over = False
        
        # Draw the appropriate screen
        if in_start_screen:
            start_button_rect = draw_start_screen(screen)
        else:
            # Check if game is over
            if game.is_over() and not game_over:
                game_over = True
                winner = game.winner()
                gui.show_message(f"Game Over! Team {winner+1} wins with {game.scores[winner]} points!", 0)
            
            gui.draw()
            
            # Draw game over screen if needed
            if game_over:
                overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))  # Semi-transparent black overlay
                screen.blit(overlay, (0, 0))
                
                # Draw game over message
                font = pygame.font.SysFont('Arial', 48)
                winner = game.winner()
                text = font.render(f"Game Over! Team {winner+1} wins!", True, (255, 215, 0))
                screen.blit(text, (screen_width//2 - text.get_width()//2, screen_height//2 - 50))
                
                # Draw scores
                score_font = pygame.font.SysFont('Arial', 32)
                score_text = score_font.render(f"Team 1: {game.scores[0]} | Team 2: {game.scores[1]}", True, (255, 255, 255))
                screen.blit(score_text, (screen_width//2 - score_text.get_width()//2, screen_height//2 + 20))
                
                # Draw restart instructions
                restart_font = pygame.font.SysFont('Arial', 24)
                restart_text = restart_font.render("Click or press any key to play again", True, (200, 200, 200))
                screen.blit(restart_text, (screen_width//2 - restart_text.get_width()//2, screen_height//2 + 80))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 