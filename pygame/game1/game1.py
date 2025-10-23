import pygame
import sys
import os
import random
# Initialize pygame
game_dir = os.path.dirname(os.path.abspath(__file__))
pygame.init()
level = 1
enmAmount = 1
font = pygame.font.SysFont("Ariel", 50)
hit_sound = pygame.mixer.Sound(os.path.join(game_dir, "songs", "die.mp3"))

# Game setup
clock = pygame.time.Clock()
running = True
screen_w = 2000
screen_h = 1080
moving_left = False
moving_right = False
moving_up = False
moving_down = False
spawn_rate = 40
spawn_counter = 0
score = 0  # Initialize score

enemies = pygame.sprite.Group()
allsprites = pygame.sprite.Group()
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("Hudson's game")

sound = os.path.join(game_dir, "songs", "sound.mp3")
pygame.mixer_music.load(sound)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
def draw_background():
    
    bg_img = pygame.image.load(os.path.join(game_dir, "img", "background.png"))
    bg_img = pygame.transform.scale(bg_img, (screen_w, screen_h))
    screen.blit(bg_img, (0, 0))

def createLv(level):
    global allsprites, enemies
    enemies = pygame.sprite.Group()
    allsprites = pygame.sprite.Group()  # Clear all sprites

    if level == 1:
        numEnemies = 5  # Set 5 enemies for level 1
    else:
        numEnemies = (level * 3) + 2  # Keep the original formula for other levels
    print(numEnemies)
    for _ in range(numEnemies):
        newEnemy = enemy_factory(1800)
        enemies.add(newEnemy)
        allsprites.add(newEnemy)
    return enemies
#Enemy class
class enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        image_path = os.path.join(game_dir, "img", "zomB.png")
        img = pygame.image.load(image_path)
        #self.image = pygame.transform.scale(self.image, (125, 125))

        self.image = pygame.transform.scale(img, (int (img.get_width() * scale), int (img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x , y )
        self.rect = self.rect.inflate (-20, -20)
        self.scale = scale
        self.speed = random.randint(3, 8)
    def update(self):
        self.rect.x -= self.speed
        # Remove the enemy if it goes off the left side of the screen
        if self.rect.right < 0:
            self.kill()  # This removes the sprite from all groups


    def draw(self):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
    


#Soldier class
class soldier(pygame.sprite.Sprite):
  #class attributes
    def __init__(self, x, y, scale, speed):
        self.x = x
        self.y = y
        self.scale = scale
        self.speed = speed
        self.flip = False

        
        image_path = os.path.join(game_dir, "img", "avatar.png")
        img = pygame.image.load(image_path)
        self.image = pygame.transform.scale(img, (int (img.get_width() * scale), int (img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
  #class functions  
    def move(self, moving_left, moving_right, moving_up, moving_down):

        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1

        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        if moving_up:
            dy = -self.speed
            self.flip = False
            self.direction = 1

        if moving_down:
            dy = self.speed
            self.flip = False
            self.direction = 1


        self.rect.x += dx
        self.rect.y += dy


    def Draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False),self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)


#game functions

def draw_score():
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    level_text = font.render(f'Level: {level}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 60))  # Display level below score

def check_collision(hudson, enemy1):
    return hudson.rect.colliderect(enemy1.rect)
        

def enemy_factory(x, scale=0.5, speed=5):
    y_pos = random.randint(0, screen_h)
    new_enemy = enemy(x, y_pos, scale)
    new_enemy.speed = speed * random.randint(3, 7)  # Make enemies 5x faster
    return new_enemy
   
hudson = soldier(200, 200, 0.5, 15)  # Increased speed from 5 to 15 (3x)
enemies = createLv(level)


#def enemyFactrory():



# Main game loop
while running:
    # Fill the screen with white
    screen.fill((255, 255, 255))
    draw_background()
    #setup enemy 
    enemies.draw(screen)
    enemies.update()

    if pygame.sprite.spritecollide(hudson, enemies, True):
        hit_sound.set_volume(0.5)
        hit_sound.play()
        pygame.mixer.music.stop()
        pygame.time.wait(1000)
        running = False

    if len(enemies) == 0:
        level += 1
        score += 100 * level  # Bonus points for completing a level
        enemies = createLv(level)
        # Optional: Add a level transition or message
        print(f"Level {level} completed! Starting level {level + 1}")



    """for enemy in enemies:
        enemy.update()
        enemy.draw()"""

    allsprites.draw(screen)
    hudson.Draw()
    draw_score()  # Update to use the new draw_score function without parameters
  
    pygame.display.update()

    hudson.move(moving_left, moving_right, moving_up, moving_down)
    clock.tick(60)
    
    pygame.display.update()

  
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True
                
            if event.key == pygame.K_ESCAPE:
                running = False



        if event.type == pygame.KEYUP:
             if event.key == pygame.K_a:
                moving_left = False
             if event.key == pygame.K_d:
                moving_right = False
             if event.key == pygame.K_w:
                moving_up = False
             if event.key == pygame.K_s:
                moving_down = False
       
       # Update the display
    pygame.display.flip()       



# Quit pygame when the game loop ends
pygame.quit()
sys.exit()

