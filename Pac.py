import os
import time
import sys

# Tamaño del tablero
width = 10
height = 6

# Posición inicial de Pac-Man
pacman_x = 1
pacman_y = 1

# Direcciones posibles
directions = {
    'w': (0, -1),  # Arriba
    's': (0, 1),   # Abajo
    'a': (-1, 0),  # Izquierda
    'd': (1, 0)    # Derecha
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board(pacman_x, pacman_y):
    clear_screen()
    for y in range(height):
        for x in range(width):
            if x == pacman_x and y == pacman_y:
                print('C', end='')  # 'C' representa a Pac-Man
            else:
                print('.', end='')  # '.' representa un espacio vacío
        print()
    print('Use WASD para mover a Pac-Man. Presiona "q" para salir.')

while True:
    print_board(pacman_x, pacman_y)
    
    command = input().strip().lower()
    
    if command == 'q':
        break
    
    if command in directions:
        dx, dy = directions[command]
        new_x = pacman_x + dx
        new_y = pacman_y + dy
        
        # Verifica los límites del tablero
        if 0 <= new_x < width and 0 <= new_y < height:
            pacman_x = new_x
            pacman_y = new_y

    time.sleep(0.1)  # Espera para que el movimiento sea visible
