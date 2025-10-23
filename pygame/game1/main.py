import pygame  # importing pygame
import os

# Initialize pygame
pygame.init()

# Setting screen dimensions
screen_width = 2000
screen_height = 1070

# Setting up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game")

# Colors
WHITE = (255, 255, 255)

# Load the background image
try:
    game_dir = os.path.dirname(os.path.abspath(__file__))
    bg_image_path = os.path.join(game_dir, "img", "yfruds.png")
    background = pygame.image.load(bg_image_path).convert()
    # Scale the background to match the screen size
    background = pygame.transform.scale(background, (screen_width, screen_height))
    bg_loaded = True
except pygame.error as e:
    print(f"Error loading background image: {e}")
    bg_loaded = False

# Load the player image
try:
    # Using absolute path to the image
    game_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(game_dir, "img", "avatar.png")
    image = pygame.image.load(image_path).convert_alpha()  # convert_alpha for transparency
    # Scale the image for the larger screen
    image = pygame.transform.scale(image, (300, 300))  # Larger size for bigger screen
    
    # Get the rectangle for positioning and center it
    rect = image.get_rect()
    # Center the sprite on screen
    rect.centerx = screen_width // 2  # Center horizontally
    rect.centery = screen_height // 2  # Center vertically
    
    # Print the position for debugging
    print(f"Sprite position - X: {rect.centerx}, Y: {rect.centery}")
    print(f"Screen size - Width: {screen_width}, Height: {screen_height}")
    
    image_loaded = True
except pygame.error as e:
    print(f"Error loading image: {e}")
    image_loaded = False

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Get the state of all keyboard keys
    keys = pygame.key.get_pressed()
    # Arrow key movement has been removed
    
    # Draw the background
    if bg_loaded:
        screen.blit(background, (0, 0))
    else:
        screen.fill(WHITE)  # Fallback to white background if image fails to load
    
    # Draw the player image if it was loaded successfully
    if image_loaded:
        screen.blit(image, rect)
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()

