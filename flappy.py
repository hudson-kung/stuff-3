# flappy.py
# Simple Flappy Bird clone using pygame (single-file, no images required)
# Controls: SPACE to flap / restart, ESC to quit

import pygame
import sys
import random

# ---------- Config ----------
WIDTH, HEIGHT = 400, 600
FPS = 60

BIRD_X = 80
BIRD_RADIUS = 12

GRAVITY = 0.45
FLAP_STRENGTH = -8.5
MAX_DROP_SPEED = 12

PIPE_WIDTH = 70
PIPE_GAP = 150
PIPE_DISTANCE = 220  # horizontal distance between successive pipes
PIPE_SPEED = 2.6

GROUND_HEIGHT = 80

FONT_NAME = None  # default font
# ----------------------------

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
font = pygame.font.Font(FONT_NAME, 32)

def draw_text(surf, text, size, x, y, center=True):
    f = pygame.font.Font(FONT_NAME, size)
    text_surf = f.render(text, True, (255,255,255))
    text_rect = text_surf.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surf.blit(text_surf, text_rect)

class Bird:
    def __init__(self):
        self.x = BIRD_X
        self.y = HEIGHT // 2
        self.vel = 0.0
        self.radius = BIRD_RADIUS
        self.alive = True
        self.angle = 0.0  # visual tilt

    def flap(self):
        self.vel = FLAP_STRENGTH

    def update(self):
        self.vel += GRAVITY
        if self.vel > MAX_DROP_SPEED:
            self.vel = MAX_DROP_SPEED
        self.y += self.vel
        
        # angle for visuals
        self.angle = max(-25, min(60, -self.vel * 3))

    def draw(self, surf):
        # simple body: circle + beak
        bird_center = (int(self.x), int(self.y))
        pygame.draw.circle(surf, (255, 220, 0), bird_center, self.radius)  # body
        # eye
        pygame.draw.circle(surf, (0,0,0), (int(self.x+4), int(self.y-3)), 2)
        # beak (triangle)
        beak = [(self.x + self.radius, self.y), (self.x + self.radius + 10, self.y - 4), (self.x + self.radius + 10, self.y + 4)]
        pygame.draw.polygon(surf, (255,100,0), beak)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = PIPE_WIDTH
        self.gap = PIPE_GAP
        # vertical position of the gap's top
        margin = 40
        max_top = HEIGHT - GROUND_HEIGHT - margin - self.gap
        self.gap_top = random.randint(margin, max_top)
        self.scored = False

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self, surf):
        top_rect = pygame.Rect(self.x, 0, self.width, self.gap_top)
        bottom_rect = pygame.Rect(self.x, self.gap_top + self.gap, self.width, HEIGHT - (self.gap_top + self.gap) - GROUND_HEIGHT)
        pygame.draw.rect(surf, (34,139,34), top_rect)   # top pipe
        pygame.draw.rect(surf, (34,139,34), bottom_rect) # bottom pipe
        # pipe rim (simple)
        pygame.draw.rect(surf, (20,100,20), top_rect, 4)
        pygame.draw.rect(surf, (20,100,20), bottom_rect, 4)

    def offscreen(self):
        return self.x + self.width < 0

    def collides_with(self, rect):
        # check collision between bird rect and the two pipe rects
        top_rect = pygame.Rect(self.x, 0, self.width, self.gap_top)
        bottom_rect = pygame.Rect(self.x, self.gap_top + self.gap, self.width, HEIGHT - (self.gap_top + self.gap) - GROUND_HEIGHT)
        return rect.colliderect(top_rect) or rect.colliderect(bottom_rect)

def draw_background(surf):
    surf.fill((112, 197, 255))  # sky blue
    # simple sun
    pygame.draw.circle(surf, (255, 240, 100), (WIDTH - 60, 60), 30)
    # ground
    ground_rect = pygame.Rect(0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT)
    pygame.draw.rect(surf, (222, 184, 135), ground_rect)
    pygame.draw.rect(surf, (205, 133, 63), ground_rect, 4)

def splash_screen(surf, score=None):
    draw_background(surf)
    draw_text(surf, "FLAPPY PY", 48, WIDTH//2, HEIGHT//4)
    draw_text(surf, "SPACE to flap", 24, WIDTH//2, HEIGHT//2)
    draw_text(surf, "ESC to quit", 18, WIDTH//2, HEIGHT//2 + 30)
    if score is not None:
        draw_text(surf, f"Score: {score}", 32, WIDTH//2, HEIGHT//2 + 80)
    pygame.display.flip()

def game_over_screen(surf, score):
    draw_background(surf)
    draw_text(surf, "GAME OVER", 48, WIDTH//2, HEIGHT//3)
    draw_text(surf, f"Score: {score}", 36, WIDTH//2, HEIGHT//2)
    draw_text(surf, "Press SPACE to play again", 20, WIDTH//2, HEIGHT//2 + 60)
    draw_text(surf, "ESC to quit", 16, WIDTH//2, HEIGHT//2 + 90)
    pygame.display.flip()

def main():
    bird = Bird()
    pipes = []
    frame_since_last_pipe = 0
    score = 0
    high_score = 0
    running = True
    started = False
    game_over = False

    # Pre-generate a first pipe a bit off-screen right
    pipes.append(Pipe(WIDTH + 40))

    while running:
        dt = clock.tick(FPS)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
                if event.key == pygame.K_SPACE:
                    if not started:
                        started = True
                        bird = Bird()
                        pipes = [Pipe(WIDTH + 40)]
                        frame_since_last_pipe = 0
                        score = 0
                        game_over = False
                    elif game_over:
                        # restart
                        bird = Bird()
                        pipes = [Pipe(WIDTH + 40)]
                        frame_since_last_pipe = 0
                        score = 0
                        game_over = False
                    else:
                        bird.flap()  # This makes the bird flap when space is pressed

        if not running:
            break

        if not started:
            splash_screen(screen, high_score)
            continue

        if not game_over:
            # update bird
            bird.update()

            # create pipes periodically
            frame_since_last_pipe += 1
            if frame_since_last_pipe > PIPE_DISTANCE / PIPE_SPEED:
                frame_since_last_pipe = 0
                pipes.append(Pipe(WIDTH))

            # update pipes
            for p in pipes:
                p.update()

            # remove offscreen pipes
            pipes = [p for p in pipes if not p.offscreen()]

            # collision detection
            bird_rect = bird.get_rect()

            # ground collision
            if bird.y + bird.radius >= HEIGHT - GROUND_HEIGHT:
                game_over = True

            # ceiling collision
            if bird.y - bird.radius <= 0:
                bird.y = bird.radius
                bird.vel = 0

            # pipes collision & scoring
            for p in pipes:
                if p.collides_with(bird_rect):
                    game_over = True
                # scoring: count when bird passes center of pipe
                if not p.scored and p.x + p.width < bird.x:
                    score += 1
                    p.scored = True
                    if score > high_score:
                        high_score = score

        # drawing
        draw_background(screen)

        # pipes
        for p in pipes:
            p.draw(screen)

        # bird
        bird.draw(screen)

        # HUD: score
        draw_text(screen, str(score), 48, WIDTH//2, 40)

        pygame.display.flip()

        if game_over:
            game_over_screen(screen, score)
            # wait for input to restart or quit; loop continues handling events
            # but avoid spinning too tight
            pygame.time.wait(150)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
