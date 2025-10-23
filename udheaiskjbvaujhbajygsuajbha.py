import pygame, sys
from pygame.locals import  *
import random

class Puzzle_box:
    def __init__(self, num, x, y):
        self.original_position = (x, y)  # Original grid position (1-4, 1-4)
        self.position = (x, y)           # Current grid position
        self.target_position = (x, y)     # Target position for animation
        self.num = num
        self.animate = False
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0


    def get_screen_pos(self, pos=None):
        """Convert grid position to screen coordinates"""
        if pos is None:
            pos = self.position
        # 800 / 5 = 160 pixels per tile
        return ((pos[0]-1) * 160, (pos[1]-1) * 160)

    def get_rect(self):
        """Get the rectangle for collision detection"""
        x, y = self.get_screen_pos()
        return pygame.Rect(x, y, 150, 150)  # Smaller tiles with gaps

    def display(self):
        # Only draw if it's not the blank space
        if self.num == 16:  # Skip drawing the blank space
            return
            
        # Calculate position with animation offset if dragging
        x, y = self.get_screen_pos()
        if self.dragging:
            x, y = pygame.mouse.get_pos()
            x -= self.offset_x
            y -= self.offset_y
        
        # Draw the tile (smaller tiles with gaps)
        pygame.draw.rect(SURFACE, TILECOLOR, (x, y, 150, 150))
        text_surf = FONT.render(str(self.num), True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(x + 75, y + 75))
        SURFACE.blit(text_surf, text_rect)


    def pos_update(self, last):
        if self.position == (blankx, blanky):
            self.position = last




def find_path_to_target(start, target, blocks):
    """BFS to find path from start to target, avoiding blocks"""
    from collections import deque
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    visited = set()
    queue = deque([(start, [])])  # (position, path)
    
    while queue:
        pos, path = queue.popleft()
        if pos == target:
            return path
            
        if pos in visited:
            continue
            
        visited.add(pos)
        
        for dx, dy in directions:
            new_pos = (pos[0] + dx, pos[1] + dy)
            if (1 <= new_pos[0] <= 4 and 1 <= new_pos[1] <= 4 and 
                new_pos not in blocks and new_pos not in visited):
                queue.append((new_pos, path + [(dx, dy)]))
    return []

def main():
    global SURFACE, FONT, TILECOLOR, BGCOLOR, blankx, blanky, last, dragging_tile, list_of_boxes

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SURFACE = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('Slide Puzzle - Drag Tiles')
    FONT = pygame.font.Font('freesansbold.ttf', 40)
    num = 1
    BGCOLOR = (3, 54, 73)
    TILECOLOR = (0, 204, 0)
    list_of_boxes = []
    list_of_position = []
    dragging_tile = None
    
    # Create all positions for 5x5 grid (25 positions)
    all_positions = [(j, i) for i in range(1, 6) for j in range(1, 6)]
    
    # Shuffle the positions
    random.shuffle(all_positions)
    
    # The last position will be our blank space
    blankx, blanky = all_positions[-1]
    
    # Create 24 tiles (1-24) and assign positions
    for num in range(1, 25):  # 1 to 24
        x, y = all_positions[num-1]  # Get position for this tile
        new_box = Puzzle_box(num, x, y)
        list_of_boxes.append(new_box)
    
    # Assign positions to tiles from the shuffled list (excluding the last position which is blank)
    for i, box in enumerate(list_of_boxes):
        box.position = all_positions[i]
        box.original_position = all_positions[i]
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_5 and (event.mod & KMOD_SHIFT):  # Shift+5 to auto-solve
                    # Get current positions
                    positions = {box.position: box for box in list_of_boxes}
                    
                    # Solve step by step for 5x5 grid
                    for num in range(1, 25):  # 24 tiles + 1 blank = 25 total
                        target_row = (num - 1) // 5 + 1  # 5 columns now
                        target_col = (num - 1) % 5 + 1   # 5 columns now
                        target_pos = (target_col, target_row)
                        
                        # If already in correct position, skip
                        if target_pos in positions and positions[target_pos].num == num:
                            continue
                            
                        # Find the tile with the target number
                        current_box = None
                        for box in list_of_boxes:
                            if box.num == num:
                                current_box = box
                                break
                        if not current_box:
                            continue
                            
                        # Find path from current position to target position
                        blocks = set(positions.keys()) - {current_box.position}
                        path = find_path_to_target(current_box.position, target_pos, blocks)
                        
                        # Move the tile along the path
                        for dx, dy in path:
                            # Update positions
                            new_pos = (current_box.position[0] + dx, current_box.position[1] + dy)
                            if new_pos == (blankx, blanky):
                                # Move the blank space to the old position
                                blankx, blanky = current_box.position
                                # Move the current box to the blank position
                                current_box.position = new_pos
                                # Update display with grid
                                pygame.time.delay(50)  # Slightly faster for 5x5
                                SURFACE.fill(BGCOLOR)
                                # Draw grid
                                for x in range(0, 800, 160):
                                    for y in range(0, 800, 160):
                                        pygame.draw.rect(SURFACE, (20, 80, 100), (x, y, 160, 160), 1)
                                # Draw tiles
                                for box in list_of_boxes:
                                    box.display()
                                pygame.display.flip()
                                # Update positions dictionary for next iteration
                                positions = {box.position: box for box in list_of_boxes}
                                break
                
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                # Check if clicked on a tile (not the blank space)
                for box in list_of_boxes:
                    if box.get_rect().collidepoint(mouse_pos):
                        # Check if the tile is adjacent to the blank space
                        if (abs(box.position[0] - blankx) == 1 and box.position[1] == blanky) or \
                           (abs(box.position[1] - blanky) == 1 and box.position[0] == blankx):
                            dragging_tile = box
                            # Calculate offset from mouse to top-left of tile
                            tile_x, tile_y = box.get_screen_pos()
                            box.offset_x = mouse_pos[0] - tile_x
                            box.offset_y = mouse_pos[1] - tile_y
                            box.dragging = True
                            break

        # Draw the game
        SURFACE.fill(BGCOLOR)
        
        # Draw the grid background (5x5 grid)
        for x in range(0, 800, 160):
            for y in range(0, 800, 160):
                pygame.draw.rect(SURFACE, (20, 80, 100), (x, y, 160, 160), 1)
        
        # Draw all tiles except the one being dragged
        for box in list_of_boxes:
            if box != dragging_tile:
                box.display()
    
        # Draw the dragging tile last (on top)
        if dragging_tile:
            dragging_tile.display()
            
        # Check for win condition
        win = gamewin(list_of_boxes)
        gamewinAnimation(win)
        
        pygame.display.update()
        FPSCLOCK.tick(60)
        FPSCLOCK.tick(60)
        FPSCLOCK.tick(60)


def isValidMove(blankx, blanky, dire):
    if blankx== 4 and dire =='LEFT':
        return False
    elif blankx == 1 and dire =="RIGHT":
        return  False
    elif blanky == 4 and dire =="UP":
        return False
    elif blanky == 1 and dire =="DOWN":
        return  False
    else:
        return True

def gamewin(list_of_boxes):
    # Sort boxes by their number to check the order
    sorted_boxes = sorted(list_of_boxes, key=lambda box: box.num)
    
    # Check if each box is in its correct position (5x5 grid)
    for i, box in enumerate(sorted_boxes):
        expected_row = (i // 5) + 1  # 5 columns now
        expected_col = (i % 5) + 1   # 5 columns now
        if box.position != (expected_col, expected_row):
            return False
    
    # Check if the blank space is in the bottom-right corner (5,5)
    if (blankx, blanky) != (5, 5):
        return False
        
    return True


def gamewinAnimation(win):
    if win == True:
        FONT2 = pygame.font.Font('freesansbold.ttf', 36)  # Slightly smaller font
        textwin = FONT2.render('You have won the 5x5 puzzle!', True, (255, 220, 100))
        textRect = textwin.get_rect(center=(400, 400))
        
        # Draw a semi-transparent overlay
        s = pygame.Surface((800, 800), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))  # Black with transparency
        SURFACE.blit(s, (0, 0))
        
        # Draw the winning text with a shadow
        shadow_surf = FONT2.render('You have won the 5x5 puzzle!', True, (0, 0, 0))
        SURFACE.blit(shadow_surf, (textRect.x+2, textRect.y+2))
        SURFACE.blit(textwin, textRect)



if __name__ == '__main__':
    main()