import pygame
import math
from board import map
pygame.init()


WIDTH = 900
HEIGHT = 950

screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
level = map
pi = math.pi
pacman_motions = []

# pacman:
for i in range(1, 5):
    pacman_motions.append(pygame.transform.scale(pygame.image.load(f'images/pacman/motion{i}.png'), (45, 45)))
    
pacman_x = 350
pacman_y = 660
direction = 0
pace = 0
sparkle = False
valid_turns = [False, False, False, False] # [EAST, WEST, NORTH, SOUTH]
direction_command = 0
pacman_speed = 3



def draw_map(level):
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'orange', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not sparkle:
                pygame.draw.circle(screen, 'orange', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, 'blue', (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, 'blue', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, 'blue', [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, pi / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, 'blue',
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], pi / 2, pi, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, 'blue', [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], pi,
                                3 * pi / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, 'blue',
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * pi / 2,
                                2 * pi, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
    
def draw_pacman():
    # 0: east | 1: west | 2: north | 3: south
    if direction == 0:
        screen.blit(pacman_motions[pace // 5], (pacman_x, pacman_y))
    if direction == 1:
        screen.blit(pygame.transform.flip(pacman_motions[pace // 5], True, False), (pacman_x, pacman_y))
    if direction == 2:
        screen.blit(pygame.transform.rotate(pacman_motions[pace // 5], 90), (pacman_x, pacman_y))
    if direction == 3:
        screen.blit(pygame.transform.rotate(pacman_motions[pace // 5], 270), (pacman_x, pacman_y))

def check_position(center_x, center_y):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30) 
    # check collisions dua tren center_x & center_y cua pacman + khoang trong du (15)
    if center_x // 30 < 29:
        if direction == 0:
            if level[center_y // num1][(center_x - 15) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[center_y // num1][(center_x - 15) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(center_y + 15) // num1][center_x // num2] < 3:
                turns[1] = True
        if direction == 3:
            if level[(center_y - 15) // num1][center_x // num2] < 3:
                turns[1] = True 
        
        if direction == 2 or direction == 3:
            if 12 <= center_x % num2 <= 18:
                if level[(center_y + 15) // num1][center_x // num2] < 3:
                    turns[3] = True
                if level[(center_y - 15) // num1][center_x // num2] < 3:
                    turns[2] = True
            if 12 <= center_y % num1 <= 18:
                if level[center_y // num1][(center_x - num2) // num2] < 3:
                    turns[1] = True
                if level[center_y // num1][(center_x + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= center_x % num2 <= 18:
                if level[(center_y + num1) // num1][center_x // num2] < 3:
                    turns[3] = True
                if level[(center_y - num1) // num1][center_x // num2] < 3:
                    turns[2] = True
            if 12 <= center_y % num1 <= 18:
                if level[center_y // num1][(center_x - 15) // num2] < 3:
                    turns[1] = True
                if level[center_y // num1][(center_x + 15) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns
    
def move_pacman(pacman_x, pacman_y):
    # EAST, WEST, NORTH, SOUTH
    if direction == 0 and valid_turns[0]:
        pacman_x  += pacman_speed
    elif direction == 1 and valid_turns[1]:
        pacman_x -= pacman_speed
    if direction == 2 and valid_turns[2]:
        pacman_y -= pacman_speed
    elif direction == 3 and valid_turns[3]:
        pacman_y += pacman_speed
    return pacman_x, pacman_y
    
run = True
while run:
    timer.tick(fps)
    if pace < 19:
        pace += 1
        if pace > 4:
            sparkle = False
    else:
        pace = 0
        sparkle = True
    screen.fill('black')
    draw_map(level)
    draw_pacman()
    center_x = pacman_x + 23
    center_y = pacman_y + 24
    valid_turns = check_position(center_x, center_y)
    pacman_x, pacman_y = move_pacman(pacman_x, pacman_y)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction    
                
                
        
    if direction_command == 0 and valid_turns[0]:
        direction = 0
    if direction_command == 1 and valid_turns[1]:
        direction = 1
    if direction_command == 2 and valid_turns[2]:
        direction = 2
    if direction_command == 3 and valid_turns[3]:
        direction = 3
           
    if pacman_x > 900:
        pacman_x = -47
    elif pacman_x < -50:
        pacman_x = 897
        
    pygame.display.flip()   
pygame.quit()