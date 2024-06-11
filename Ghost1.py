import pygame, copy, math, random
from Board import boardPattern
from random import randrange

ElementPath = "Assets/Sprites/ElementSprites/"
gameBoard = copy.deepcopy(boardPattern)
screen = pygame.display.set_mode((700, 900))

square = 25
spriteRatio = 3/2
spriteOffset = square * (1 - spriteRatio) * (1/2)

ghostsafeArea = [15, 13] # The location the ghosts escape to when attacked
ghostGate = [[15, 13], [15, 14]]

class Ghost:
    """Lớp đại diện cho một con ma trong trò chơi."""
    def __init__(self, game, row, col, color, changeFeetCount):
        """
        Khởi tạo đối tượng Ghost.

        Tham số:
            game (object): Thể hiện của trò chơi.
            row (int): Hàng của ma.
            col (int): Cột của ma.
            color (str): Màu sắc của ma.
            changeFeetCount (int): Bộ đếm cho việc thay đổi chân khi di chuyển.
        """
        self.game = game 
        self.row = row
        self.col = col
        self.attacked = False
        self.color = color
        self.dir = randrange(4)
        self.dead = False
        self.changeFeetCount = changeFeetCount
        self.changeFeetDelay = 5
        self.target = [-1, -1]
        self.ghostSpeed = 1/4
        self.lastLoc = [-1, -1]
        self.attackedTimer = 240
        self.attackedCount = 0
        self.deathTimer = 120
        self.deathCount = 0

    def update(self):
        """
        Cập nhật trạng thái của con ma.
        """
        if self.target == [-1, -1] or (self.row == self.target[0] and self.col == self.target[1]) or gameBoard[int(self.row)][int(self.col)] == 4 or self.dead:
            self.setTarget()
        self.setDir()
        self.move()

        if self.attacked:
            self.attackedCount += 1

        if self.attacked and not self.dead:
            self.ghostSpeed = 1/8

        if self.attackedCount == self.attackedTimer and self.attacked:
            if not self.dead:
                self.ghostSpeed = 1/4
                self.row = math.floor(self.row)
                self.col = math.floor(self.col)

            self.attackedCount = 0
            self.attacked = False
            self.setTarget()

        if self.dead and gameBoard[self.row][self.col] == 4:
            self.deathCount += 1
            self.attacked = False
            if self.deathCount == self.deathTimer:
                self.deathCount = 0
                self.dead = False
                self.ghostSpeed = 1/4

    def draw(self): # Ghosts states: Alive, Attacked, Dead | Attributes: Color, Direction, Location
        """
        Vẽ con ma lên màn hình.
        """
        ghostImage = pygame.image.load(ElementPath + "element152.png")
        currentDir = ((self.dir + 3) % 4) * 2
        if self.changeFeetCount == self.changeFeetDelay:
            self.changeFeetCount = 0
            currentDir += 1
        self.changeFeetCount += 1
        if self.dead:
            tileNum = 152 + currentDir
            ghostImage = pygame.image.load(ElementPath + "element" + str(tileNum) + ".png")
        elif self.attacked:
            if self.attackedTimer - self.attackedCount < self.attackedTimer//3:
                if (self.attackedTimer - self.attackedCount) % 31 < 26:
                    ghostImage = pygame.image.load(ElementPath + "element0" + str(70 + (currentDir - (((self.dir + 3) % 4) * 2))) + ".png")
                else:
                    ghostImage = pygame.image.load(ElementPath + "element0" + str(72 + (currentDir - (((self.dir + 3) % 4) * 2))) + ".png")
            else:
                ghostImage = pygame.image.load(ElementPath + "element0" + str(72 + (currentDir - (((self.dir + 3) % 4) * 2))) + ".png")
        else:
            if self.color == "blue":
                tileNum = 136 + currentDir
                ghostImage = pygame.image.load(ElementPath + "element" + str(tileNum) + ".png")
            elif self.color == "pink":
                tileNum = 128 + currentDir
                ghostImage = pygame.image.load(ElementPath + "element" + str(tileNum) + ".png")
            elif self.color == "orange":
                tileNum = 144 + currentDir
                ghostImage = pygame.image.load(ElementPath + "element" + str(tileNum) + ".png")
            elif self.color == "red":
                tileNum = 96 + currentDir
                if tileNum < 100:
                    ghostImage = pygame.image.load(ElementPath + "element0" + str(tileNum) + ".png")
                else:
                    ghostImage = pygame.image.load(ElementPath + "element" + str(tileNum) + ".png")

        ghostImage = pygame.transform.scale(ghostImage, (int(square * 1.5), int(square * 1.5)))
        screen.blit(ghostImage, (self.col * square + spriteOffset, self.row * square + spriteOffset, square, square))

    def isValidTwo(self, cRow, cCol, dist, visited):
        """
        Kiểm tra xem một vị trí có hợp lệ để ma di chuyển hay không.

        Tham số:
            cRow (int): Hàng của vị trí cần kiểm tra.
            cCol (int): Cột của vị trí cần kiểm tra.
            dist (int): Khoảng cách đến vị trí.
            visited (list): Danh sách các vị trí đã đi qua.

        Trả về:
            bool: True nếu vị trí hợp lệ, False nếu ngược lại.
        """
    
        if cRow < 3 or cRow >= len(gameBoard) - 5 or cCol < 0 or cCol >= len(gameBoard[0]) or gameBoard[cRow][cCol] == 3:
            return False
        elif visited[cRow][cCol] <= dist:
            return False
        return True

    def isValid(self, cRow, cCol):
        """
        Kiểm tra xem một vị trí có hợp lệ để ma di chuyển hay không.

        Tham số:
            cRow (int): Hàng của vị trí cần kiểm tra.
            cCol (int): Cột của vị trí cần kiểm tra.

        Trả về:
            bool: True nếu vị trí hợp lệ, False nếu ngược lại.
        """
        if cCol < 0 or cCol > len(gameBoard[0]) - 1:
            return True
        for ghost in self.game.ghosts:
            if ghost.color == self.color:
                continue
            if ghost.row == cRow and ghost.col == cCol and not self.dead:
                return False
        if not ghostGate.count([cRow, cCol]) == 0:
            if self.dead and self.row < cRow:
                return True
            elif self.row > cRow and not self.dead and not self.attacked and not self.game.lockedIn:
                return True
            else:
                return False
        if gameBoard[cRow][cCol] == 3:
            return False
        return True

    def setDir(self): 
        """
        Đặt hướng cho ma di chuyển.
        """
        dirs = [[0, -self.ghostSpeed, 0],
                [1, 0, self.ghostSpeed],
                [2, self.ghostSpeed, 0],
                [3, 0, -self.ghostSpeed]
        ]
        random.shuffle(dirs)
        best = 10000
        bestDir = -1
        for newDir in dirs:
            if self.calcDistance(self.target, [self.row + newDir[1], self.col + newDir[2]]) < best:
                if not (self.lastLoc[0] == self.row + newDir[1] and self.lastLoc[1] == self.col + newDir[2]):
                    if newDir[0] == 0 and self.col % 1.0 == 0:
                        if self.isValid(math.floor(self.row + newDir[1]), int(self.col + newDir[2])):
                            bestDir = newDir[0]
                            best = self.calcDistance(self.target, [self.row + newDir[1], self.col + newDir[2]])
                    elif newDir[0] == 1 and self.row % 1.0 == 0:
                        if self.isValid(int(self.row + newDir[1]), math.ceil(self.col + newDir[2])):
                            bestDir = newDir[0]
                            best = self.calcDistance(self.target, [self.row + newDir[1], self.col + newDir[2]])
                    elif newDir[0] == 2 and self.col % 1.0 == 0:
                        if self.isValid(math.ceil(self.row + newDir[1]), int(self.col + newDir[2])):
                            bestDir = newDir[0]
                            best = self.calcDistance(self.target, [self.row + newDir[1], self.col + newDir[2]])
                    elif newDir[0] == 3 and self.row % 1.0 == 0:
                        if self.isValid(int(self.row + newDir[1]), math.floor(self.col + newDir[2])):
                            bestDir = newDir[0]
                            best = self.calcDistance(self.target, [self.row + newDir[1], self.col + newDir[2]])
        self.dir = bestDir

    def calcDistance(self, a, b):
        """
        Tính khoảng cách Euclide giữa hai điểm.

        Tham số:
            a (list): Tọa độ của điểm thứ nhất.
            b (list): Tọa độ của điểm thứ hai.

        Trả về:
            float: Khoảng cách Euclide giữa hai điểm.
        """
        dR = a[0] - b[0]
        dC = a[1] - b[1]
        return math.sqrt((dR * dR) + (dC * dC))

    def setTarget(self):
        """
        Đặt vị trí mục tiêu cho ma di chuyển đến.
        """
        if gameBoard[int(self.row)][int(self.col)] == 4 and not self.dead:
            self.target = [ghostGate[0][0] - 1, ghostGate[0][1]+1]
            return
        elif gameBoard[int(self.row)][int(self.col)] == 4 and self.dead:
            self.target = [self.row, self.col]
        elif self.dead:
            self.target = [14, 13]
            return

        # Records the quadrants of each ghost's target
        quads = [0, 0, 0, 0]
        for ghost in self.game.ghosts:
            # if ghost.target[0] == self.row and ghost.col == self.col:
            #   continue
            if ghost.target[0] <= 15 and ghost.target[1] >= 13:
                quads[0] += 1
            elif ghost.target[0] <= 15 and ghost.target[1] < 13:
                quads[1] += 1
            elif ghost.target[0] > 15 and ghost.target[1] < 13:
                quads[2] += 1
            elif ghost.target[0]> 15 and ghost.target[1] >= 13:
                quads[3] += 1

        # Finds a target that will keep the ghosts dispersed
        while True:
            self.target = [randrange(31), randrange(28)]
            quad = 0
            if self.target[0] <= 15 and self.target[1] >= 13:
                quad = 0
            elif self.target[0] <= 15 and self.target[1] < 13:
                quad = 1
            elif self.target[0] > 15 and self.target[1] < 13:
                quad = 2
            elif self.target[0] > 15 and self.target[1] >= 13:
                quad = 3
            if not gameBoard[self.target[0]][self.target[1]] == 3 and not gameBoard[self.target[0]][self.target[1]] == 4:
                break
            elif quads[quad] == 0:
                break

    def move(self):
        """
        Di chuyển con ma đến vị trí mục tiêu của nó.
        """
        self.lastLoc = [self.row, self.col]
        if self.dir == 0:
            self.row -= self.ghostSpeed
        elif self.dir == 1:
            self.col += self.ghostSpeed
        elif self.dir == 2:
            self.row += self.ghostSpeed
        elif self.dir == 3:
            self.col -= self.ghostSpeed

        # Incase they go through the middle tunnel
        self.col = self.col % len(gameBoard[0])
        if self.col < 0:
            self.col = len(gameBoard[0]) - 0.5



    def setAttacked(self, isAttacked):
        """
        Đặt trạng thái bị tấn công của con ma.

        Tham số:
            isAttacked (bool): True nếu con ma bị tấn công, False nếu ngược lại.
        """
        self.attacked = isAttacked

    def isAttacked(self):
        """
        Kiểm tra xem con ma có bị tấn công không.

        Trả về:
            bool: True nếu con ma bị tấn công, False nếu ngược lại.
        """
        return self.attacked

    def setDead(self, isDead):
        """
        Đặt trạng thái đã chết của con ma.

        Tham số:
            isDead (bool): True nếu con ma đã chết, False nếu ngược lại.
        """
        self.dead = isDead

    def isDead(self):
        """
        Kiểm tra xem con ma có đã chết không.

        Trả về:
            bool: True nếu con ma đã chết, False nếu ngược lại.
        """
        return self.dead
    
