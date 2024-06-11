import pygame, copy, math
from Board import boardPattern

ElementPath = "Assets/Sprites/ElementSprites/"
gameBoard = copy.deepcopy(boardPattern)
screen = pygame.display.set_mode((700, 900))

tile = 25
spriteOffset = tile * (1 - 1.5) * (1/2)

def canMove(row, col):
    """
    Kiểm tra xem có thể di chuyển đến vị trí (row, col) trên bảng game hay không.
    """
    if col == -1 or col == len(gameBoard[0]):
        return True
    if gameBoard[int(row)][int(col)] != 3:
        return True
    return False
    

class Pacman:
    """
    Lớp đại diện cho đối tượng Pacman.
    """
    def __init__(self, row, col, game):
        """
        Khởi tạo đối tượng Pacman.
        
        Tham số:
        - row: hàng ban đầu của Pacman trên bảng game.
        - col: cột ban đầu của Pacman trên bảng game.
        - game: tham chiếu đến đối tượng trò chơi.
        """
        self.game = game
        self.row = row
        self.col = col
        self.mouthOpen = False
        self.pacSpeed = 1/4
        self.mouthChangeDelay = 5
        self.mouthChangeCount = 0
        self.dir = 0 # 0: North, 1: East, 2: South, 3: West
        self.newDir = 0
        self.rest = True
        
    def update(self):
        """
        Cập nhật vị trí của Pacman trên bảng game.
        """
        if self.newDir == 0:
            if canMove(math.floor(self.row - self.pacSpeed), self.col) and self.col % 1.0 == 0:
                self.row -= self.pacSpeed
                self.dir = self.newDir
                return
        elif self.newDir == 1:
            if canMove(self.row, math.ceil(self.col + self.pacSpeed)) and self.row % 1.0 == 0:

                self.col += self.pacSpeed
                self.dir = self.newDir
                return
        elif self.newDir == 2:
            if canMove(math.ceil(self.row + self.pacSpeed), self.col) and self.col % 1.0 == 0:
                self.row += self.pacSpeed
                self.dir = self.newDir
                return
        elif self.newDir == 3:
            if canMove(self.row, math.floor(self.col - self.pacSpeed)) and self.row % 1.0 == 0:
                self.col -= self.pacSpeed
                self.dir = self.newDir
                return

        if self.dir == 0:
            if canMove(math.floor(self.row - self.pacSpeed), self.col) and self.col % 1.0 == 0:
                self.row -= self.pacSpeed
        elif self.dir == 1:
            if canMove(self.row, math.ceil(self.col + self.pacSpeed)) and self.row % 1.0 == 0:
                self.col += self.pacSpeed
        elif self.dir == 2:
            if canMove(math.ceil(self.row + self.pacSpeed), self.col) and self.col % 1.0 == 0:
                self.row += self.pacSpeed
        elif self.dir == 3:
            if canMove(self.row, math.floor(self.col - self.pacSpeed)) and self.row % 1.0 == 0:
                self.col -= self.pacSpeed

    # Draws pacman based on his current state
    def draw(self, game):
        """
        Vẽ hình ảnh của Pacman trên màn hình game.

        Tham số:
        - game: tham chiếu đến đối tượng trò chơi.
        """
        if not game.started:
            pacmanImage = pygame.image.load(ElementPath + "element112.png")
            pacmanImage = pygame.transform.scale(pacmanImage, (int(tile * 1.5), int(tile * 1.5)))
            screen.blit(pacmanImage, (self.col * tile + spriteOffset, self.row * tile + spriteOffset, tile, tile))
            return

        if self.mouthChangeCount == self.mouthChangeDelay:
            self.mouthChangeCount = 0
            self.mouthOpen = not self.mouthOpen
        self.mouthChangeCount += 1
        # pacmanImage = pygame.image.load("Sprites/element049.png")
        if self.dir == 0:
            if self.mouthOpen:
                pacmanImage = pygame.image.load(ElementPath + "element049.png")
            else:
                pacmanImage = pygame.image.load(ElementPath + "element051.png")
        elif self.dir == 1:
            if self.mouthOpen:
                pacmanImage = pygame.image.load(ElementPath + "element052.png")
            else:
                pacmanImage = pygame.image.load(ElementPath + "element054.png")
        elif self.dir == 2:
            if self.mouthOpen:
                pacmanImage = pygame.image.load(ElementPath + "element053.png")
            else:
                pacmanImage = pygame.image.load(ElementPath + "element055.png")
        elif self.dir == 3:
            if self.mouthOpen:
                pacmanImage = pygame.image.load(ElementPath + "element048.png")
            else:
                pacmanImage = pygame.image.load(ElementPath + "element050.png")

        pacmanImage = pygame.transform.scale(pacmanImage, (int(tile * 1.5), int(tile * 1.5)))
        screen.blit(pacmanImage, (self.col * tile + spriteOffset, self.row * tile + spriteOffset, tile, tile))


