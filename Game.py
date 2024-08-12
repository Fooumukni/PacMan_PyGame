import pygame, copy, math, random
from Board import boardPattern
from Pacman1 import Pacman
from Ghost1 import Ghost
from Menu import displayMenu
from random import randrange

BoardPath = "Assets/Sprites/BoardSprites/"
IntermissionPath = "Assets/Sprites/WhiteBoardSprites/"
ElementPath = "Assets/Sprites/ElementSprites/"
TextPath = "Assets/Sprites/TextSprites/"
DataPath = "Assets/HighScoreSaved/"
SoundPath = "Assets/Sounds/"

pygame.mixer.init()
pygame.init()
print(pygame.mixer.music.get_busy())

gameBoard = copy.deepcopy(boardPattern)

spriteRatio = 1.5
tile = 25 # Size of each unit tile
spriteOffset = tile * (1 - 1.5) * (1/2)
musicPlaying = 0 # 0: Chomp | 1: Important | 2: Siren
pelletColor = (222, 161, 133)

(width, height) = (len(gameBoard[0]) * tile, len(gameBoard) * tile) # Game screen (700, 900)
screen = pygame.display.set_mode((width, height))
pygame.display.flip()


COMMAND_KEYS = {
    "UP":[pygame.K_w, pygame.K_UP],
    "DOWN":[pygame.K_s, pygame.K_DOWN],
    "RIGHT":[pygame.K_d, pygame.K_RIGHT],
    "LEFT":[pygame.K_a, pygame.K_LEFT]
}

class Game:
    """
    Lớp đại diện cho trò chơi Pacman.

    Thuộc tính:
        paused (bool): Biến chỉ ra xem trò chơi có đang tạm dừng không.
        ghostUpdateDelay (int): Độ trễ trong việc cập nhật chuyển động của Ghost.
        ghostUpdateCount (int): Bộ đếm cho việc cập nhật Ghost.
        pacmanUpdateDelay (int): Độ trễ trong việc cập nhật chuyển động của Pacman.
        pacmanUpdateCount (int): Bộ đếm cho việc cập nhật Pacman.
        tictakChangeDelay (int): Độ trễ trong việc thay đổi màu Tic-Tak.
        tictakChangeCount (int): Bộ đếm cho việc thay đổi màu Tic-Tak.
        ghostsAttacked (bool): Biến chỉ ra xem các Ghost có bị tấn công không.
        highScore (int): Điểm cao nhất đạt được trong trò chơi.
        score (int): Điểm hiện tại của người chơi.
        level (int): Cấp độ hiện tại của trò chơi.
        lives (int): Số mạng còn lại.
        ghosts (list): Danh sách các đối tượng Ghost trong trò chơi.
        pacman (Pacman): Đối tượng Pacman đại diện cho người chơi.
        total (int): Tổng số hạt trong trò chơi.
        ghostScore (int): Điểm được thưởng cho việc ăn một Ghost.
        levels (list): Danh sách các cấp độ với các tham số tương ứng cho hành vi của Ghost.
        ghostStates (list): Danh sách các trạng thái cho mỗi Ghost (chase hoặc scatter).
        collected (int): Số hạt đã thu thập bởi Pacman.
        started (bool): Biến chỉ ra xem trò chơi đã bắt đầu chưa.
        gameOver (bool): Biến chỉ ra xem trò chơi đã kết thúc chưa.
        gameOverCounter (int): Bộ đếm cho hoạt ảnh kết thúc trò chơi.
        points (list): Danh sách các điểm được hiển thị trên màn hình.
        pointsTimer (int): Bộ đếm thời gian cho việc hiển thị điểm.
        intermission (bool): Biến chỉ ra xem trò chơi có đang trong chế độ chờ giữa các màn không.
        berryState (list): Danh sách biểu thị trạng thái của các quả dâu trong trò chơi.
        berryLocation (list): Vị trí của quả dâu trong trò chơi.
        berries (list): Danh sách các sprite quả dâu.
        berriesCollected (list): Danh sách các quả dâu đã được thu thập.
        levelTimer (int): Bộ đếm thời gian cho cấp độ hiện tại.
        lockedInTimer (int): Bộ đếm thời gian cho trạng thái bị khóa.
        lockedIn (bool): Biến chỉ ra xem trò chơi có đang ở trạng thái bị khóa không.
        extraLifeGiven (bool): Biến chỉ ra xem một mạng bổ sung đã được trao không.
        musicPlaying (int): Chỉ số cho biết loại nhạc đang phát.
    """

    def __init__(self, level, score):
        """
        Khởi tạo một đối tượng Game mới.

        Args:
            level (int): Cấp độ bắt đầu của trò chơi.
            score (int): Điểm ban đầu của trò chơi.
        """
        self.paused = True
        self.ghostUpdateDelay = 1
        self.ghostUpdateCount = 0
        self.pacmanUpdateDelay = 1
        self.pacmanUpdateCount = 0
        self.tictakChangeDelay = 10
        self.tictakChangeCount = 0
        self.ghostsAttacked = False
        self.highScore = self.getHighScore()
        self.score = score
        self.level = level
        self.lives = 3
        self.ghosts = [Ghost(self, 14.0, 13.5, "red", 0), Ghost(self, 17.0, 11.5, "blue", 1), Ghost(self, 17.0, 13.5, "pink", 2), Ghost(self, 17.0, 15.5, "orange", 3)]
        self.pacman = Pacman(26.0, 13.5, self) # Center of Second Last Row
        self.total = self.getCount()
        self.ghostScore = 200
        self.levels = [[350, 250], [150, 450], [150, 450], [0, 600]]
        random.shuffle(self.levels)
        # Level index and Level Progress
        self.ghostStates = [[1, 0], [0, 0], [1, 0], [0, 0]]
        index = 0
        for state in self.ghostStates:
            state[0] = randrange(2)
            state[1] = randrange(self.levels[index][state[0]] + 1)
            index += 1
        self.collected = 0
        self.started = False
        self.gameOver = False
        self.gameOverCounter = 0
        self.points = []
        self.pointsTimer = 10
        self.intermission = False
        
        # Berry Spawn Time, Berry Death Time, Berry Eaten
        self.berryState = [200, 400, False]
        self.berryLocation = [20.0, 13.5]
        self.berries = ["element080.png", "element081.png", "element082.png", "element083.png", "element084.png", "element085.png", "element086.png", "element087.png"]
        self.berriesCollected = []
        self.levelTimer = 0
        self.berryScore = 100
        self.lockedInTimer = 100
        self.lockedIn = True
        self.extraLifeGiven = False
        self.musicPlaying = 0

    def update(self):
        """
        Cập nhật trạng thái của trò chơi.
        """
        print(self.ghostStates)
        if self.gameOver:
            self.gameOverFunc()
            return
        
        if self.paused or not self.started and onLaunchScreen:
            self.drawTilesAround(21, 10)
            self.drawTilesAround(21, 11)
            self.drawTilesAround(21, 12)
            self.drawTilesAround(21, 13)
            self.drawTilesAround(21, 14)
            self.drawReady() 
            pygame.display.update()
            return

        self.levelTimer += 1
        self.ghostUpdateCount += 1
        self.pacmanUpdateCount += 1
        self.tictakChangeCount += 1
        self.ghostsAttacked = False

        if self.score >= 10000 and not self.extraLifeGiven:
            self.lives += 1
            self.extraLifeGiven = True
            self.forcePlayMusic("pacman_extrapac.wav")

        # Draw tiles around ghosts and pacman
        self.clearBoard()
        for ghost in self.ghosts:
            if ghost.attacked:
                self.ghostsAttacked = True

        # Check if the ghost should chase pacman
        index = 0
        for state in self.ghostStates:
            state[1] += 1
            if state[1] >= self.levels[index][state[0]]:
                state[1] = 0
                state[0] += 1
                state[0] %= 2
            index += 1

        index = 0
        for ghost in self.ghosts:
            if not ghost.attacked and not ghost.dead and self.ghostStates[index][0] == 0:
                ghost.target = [self.pacman.row, self.pacman.col]
            index += 1

        if self.levelTimer == self.lockedInTimer:
            self.lockedIn = False

        self.checkSurroundings
        if self.ghostUpdateCount == self.ghostUpdateDelay:
            for ghost in self.ghosts:
                ghost.update()
            self.ghostUpdateCount = 0

        if self.tictakChangeCount == self.tictakChangeDelay:
            #Changes the color of special Tic-Taks
            self.flipColor()
            self.tictakChangeCount = 0

        if self.pacmanUpdateCount == self.pacmanUpdateDelay:
            self.pacmanUpdateCount = 0
            self.pacman.update()
            self.pacman.col %= len(gameBoard[0])
            if self.pacman.row % 1.0 == 0 and self.pacman.col % 1.0 == 0:
                if gameBoard[int(self.pacman.row)][int(self.pacman.col)] == 2:
                    self.playMusic("munch_1.wav")
                    gameBoard[int(self.pacman.row)][int(self.pacman.col)] = 1
                    self.score += 10
                    self.collected += 1
                    # Fill tile with black
                    pygame.draw.rect(screen, (0, 0, 0), (self.pacman.col * tile, self.pacman.row * tile, tile, tile))
                elif gameBoard[int(self.pacman.row)][int(self.pacman.col)] == 5 or gameBoard[int(self.pacman.row)][int(self.pacman.col)] == 6:
                    self.forcePlayMusic("power_pellet.wav")
                    gameBoard[int(self.pacman.row)][int(self.pacman.col)] = 1
                    self.collected += 1
                    # Fill tile with black
                    pygame.draw.rect(screen, (0, 0, 0), (self.pacman.col * tile, self.pacman.row * tile, tile, tile))
                    self.score += 50
                    self.ghostScore = 200
                    for ghost in self.ghosts:
                        ghost.attackedCount = 0
                        ghost.setAttacked(True)
                        ghost.setTarget()
                        self.ghostsAttacked = True
        self.checkSurroundings()
        self.highScore = max(self.score, self.highScore)

        global running
        if self.collected == self.total:
            self.forcePlayMusic("credit.wav")
            for ghost in self.ghosts:
                ghost.draw()
            self.drawTilesAround(self.pacman.row, self.pacman.col)
            pacmanImage = pygame.image.load(ElementPath + "element112.png")
            pacmanImage = pygame.transform.scale(pacmanImage, (int(tile * 1.5), int(tile * 1.5)))
            
            # screen.blit(source, destination)
            # The first argument is pacmanImage, which is the image that we want to draw
            # The second argument is a tuple containing position and size of the pacmanImage (x, y, width (pixel), height(pixel))
            screen.blit(pacmanImage, ((self.pacman.col * tile) + spriteOffset, self.pacman.row * tile + spriteOffset, tile, tile)) 

        # Draws new image
            
            pygame.display.update()
            pygame.time.wait(1500)
            self.intermission = True
            # Blink board from white to blues
            blinkDuration = 2000  # Total duration of blinking
            blinkInterval = 200   # Time interval for each blink
            startTime = pygame.time.get_ticks()
            while pygame.time.get_ticks() - startTime < blinkDuration:
                self.renderIntermission()
                pygame.display.update()
                pygame.time.wait(blinkInterval // 2)
                
                self.render()
                pygame.display.update()
                pygame.time.wait(blinkInterval // 2)
            self.intermission = False
            
            pygame.time.wait(1500)

            print("New Level")
            self.forcePlayMusic("intermission.wav")
            self.level += 1
            self.newLevel()

        if self.level - 1 == 8: #(self.levels[0][0] + self.levels[0][1]) // 50:
            global onExitScreen
            print("You win", self.level, len(self.levels))
            onExitScreen = True
            screen.fill((0, 0, 0))
            currentScreen.displayYouWonMenu()
        else:     
            self.softRender()

    def renderIntermission(self):
        """
        Vẽ màn hình chờ giữa các màn.
        """
        screen.fill((0, 0, 0)) # Create a black screen
        # Draw map
        currentTile = 0
        self.displayLives()
        self.displayScore()
        for i in range(3, len(gameBoard) - 2):
            for j in range(len(gameBoard[0])):
                if gameBoard[i][j] == 3: # Draw wall
                    imageName = str(currentTile)
                    if len(imageName) == 1:
                        imageName = "00" + imageName
                    elif len(imageName) == 2:
                         imageName = "0" + imageName
                    # Get image of desired tile
                    imageName = "intermission" + imageName + ".png"
                    tileImage = pygame.image.load(IntermissionPath + imageName)
                    tileImage = pygame.transform.scale(tileImage, (tile, tile)) # scale each tile image from 70x70 to 25x25


                    screen.blit(tileImage, (j * tile, i * tile, tile, tile))
                currentTile += 1
        pacmanImage = pygame.image.load(ElementPath + "element112.png")
        pacmanImage = pygame.transform.scale(pacmanImage, (int(tile * 1.5), int(tile * 1.5)))
        screen.blit(pacmanImage, (self.pacman.col * tile + spriteOffset, self.pacman.row * tile + spriteOffset, tile, tile))    
        pygame.display.update()
        
        
    # Render method
    def render(self):
        """
        Vẽ màn hình trò chơi.
        """
        screen.fill((0, 0, 0))  # Create a black screen
        # Draw map
        currentTile = 0
        self.displayLives()
        self.displayScore()
        for i in range(3, len(gameBoard) - 2):
            for j in range(len(gameBoard[0])):
                if gameBoard[i][j] == 3:  # Draw wall
                    imageName = str(currentTile)
                    if len(imageName) == 1:
                        imageName = "00" + imageName
                    elif len(imageName) == 2:
                        imageName = "0" + imageName
                    # Get image of desired tile
                    imageName = "map" + imageName + ".png"
                    tileImage = pygame.image.load(BoardPath + imageName)
                    tileImage = pygame.transform.scale(tileImage, (tile, tile))  # scale each tile image from 70x70 to 25x25
                    screen.blit(tileImage, (j * tile, i * tile, tile, tile))

                    # (x, y, width, height)
                elif gameBoard[i][j] == 2 and not self.intermission:  # Draw Tic-Tak
                    pygame.draw.circle(screen, pelletColor, (j * tile + tile // 2, i * tile + tile // 2), tile // 4)
                elif gameBoard[i][j] == 5 and not self.intermission:  # Draw Special Tik-Tak
                    pygame.draw.circle(screen, pelletColor, (j * tile + tile // 2, i * tile + tile // 2), tile // 2)
                elif gameBoard[i][j] == 6 and not self.intermission:  # Black Special Tik-Tak
                    pygame.draw.circle(screen, (0, 0, 0), (j * tile + tile // 2, i * tile + tile // 2), tile // 2)

                currentTile += 1
        # Draw Sprites
        if not self.intermission:
            for ghost in self.ghosts:
                ghost.draw()
        # Updates the screen
        if self.intermission:
            pacmanImage = pygame.image.load(ElementPath + "element112.png")
            pacmanImage = pygame.transform.scale(pacmanImage, (int(tile * 1.5), int(tile * 1.5)))
            screen.blit(pacmanImage, (self.pacman.col * tile + spriteOffset, self.pacman.row * tile + spriteOffset, tile, tile))  
        else:
            self.pacman.draw(self)
        pygame.display.update()



    def softRender(self):
        """
        Vẽ màn hình trò chơi với các hiệu ứng khác.
        """
        pointsToDraw = []
        for point in self.points:
            if point[3] < self.pointsTimer:
                pointsToDraw.append([point[2], point[0], point[1]])
                point[3] += 1
            else:
                self.points.remove(point)
                self.drawTilesAround(point[0], point[1])

        for point in pointsToDraw:
            self.drawPoints(point[0], point[1], point[2])

        # Draw Sprites
        for ghost in self.ghosts:
            ghost.draw()
        self.pacman.draw(self)
        self.displayScore()
        self.displayBerries()
        self.displayLives()
        # for point in pointsToDraw:
        #     self.drawPoints(point[0], point[1], point[2])
        self.drawBerry()
        # Updates the screen
        pygame.display.update()

    def playMusic(self, music):
        """
        Phát nhạc được chỉ định.

        Args:
            music (str): Tên tệp nhạc cần phát.
        """
        global musicPlaying
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.unload()
            pygame.mixer.music.load(SoundPath + music)
            pygame.mixer.music.queue(SoundPath + music)
            pygame.mixer.music.play()
            if music == "munch_1.wav":
                musicPlaying = 0
            elif music == "siren_1.wav":
                musicPlaying = 2
            else:
                musicPlaying = 1

    def forcePlayMusic(self, music):
        """
        Bắt buộc phát nhạc được chỉ định.

        Args:
            music (str): Tên tệp nhạc cần phát.
        """
        pygame.mixer.music.unload()
        pygame.mixer.music.load(SoundPath + music)
        pygame.mixer.music.play()
        global musicPlaying
        musicPlaying = 1

    def clearBoard(self):
        """
        Xóa bảng trò chơi.
        """
        # Draw tiles around ghosts and pacman
        for ghost in self.ghosts:
            self.drawTilesAround(ghost.row, ghost.col)
        self.drawTilesAround(self.pacman.row, self.pacman.col)
        self.drawTilesAround(self.berryLocation[0], self.berryLocation[1])
        # Clears Ready! Label
        self.drawTilesAround(20, 10)
        self.drawTilesAround(20, 11)
        self.drawTilesAround(20, 12)
        self.drawTilesAround(20, 13)
        self.drawTilesAround(20, 14)

    def checkSurroundings(self):
        """
        Kiểm tra xung quanh của Pacman và các Ghost để phát hiện va chạm.
        """
        # Check if pacman got killed
        for ghost in self.ghosts:
            if self.touchingPacman(ghost.row, ghost.col) and not ghost.attacked:
                
                if self.lives == 1:
                    print("Game Over") 
                    self.forcePlayMusic("death_1.wav")
                    self.gameOver = True
                    # Remove the ghosts from the screen
                    for ghost in self.ghosts:
                        self.drawTilesAround(ghost.row, ghost.col)
                    self.drawTilesAround(self.pacman.row, self.pacman.col)
                    self.pacman.draw(self)
                    pygame.display.update()
                    pause(10000000)
                    return
                
                self.started = False
                self.forcePlayMusic("pacman_death.wav")
                pygame.time.wait(2000)
                reset()
            elif self.touchingPacman(ghost.row, ghost.col) and ghost.isAttacked() and not ghost.isDead():
                ghost.setDead(True)
                ghost.setTarget()
                ghost.ghostSpeed = 1
                ghost.row = math.floor(ghost.row)
                ghost.col = math.floor(ghost.col)
                self.score += self.ghostScore
                self.points.append([ghost.row, ghost.col, self.ghostScore, 0])
                self.ghostScore *= 2
                self.forcePlayMusic("eat_ghost.wav")
                pause(10000000)
        if self.touchingPacman(self.berryLocation[0], self.berryLocation[1]) and not self.berryState[2] and self.levelTimer in range(self.berryState[0], self.berryState[1]):
            self.berryState[2] = True
            self.score += self.berryScore
            self.points.append([self.berryLocation[0], self.berryLocation[1], self.berryScore, 0])
            self.berriesCollected.append(self.berries[(self.level - 1) % 8])
            self.forcePlayMusic("eat_fruit.wav")
    # Displays the current score
    def displayScore(self):
        """
        Hiển thị điểm hiện tại trên màn hình.
        """
        textOneUp = ["text033.png", "text021.png", "text016.png"]
        textHighScore = ["text007.png", "text008.png", "text006.png", "text007.png", "text015.png", "text019.png", "text002.png", "text014.png", "text018.png", "text004.png"]
        index = 0
        scoreStart = 4
        highScoreStart = 11
        for i in range(scoreStart, scoreStart+len(textOneUp)):
            tileImage = pygame.image.load(TextPath + textOneUp[index])
            tileImage = pygame.transform.scale(tileImage, (tile, tile))
            screen.blit(tileImage, (i * tile, 4, tile, tile))
            index += 1
        score = str(self.score)
        if score == "0":
            score = "00"
        index = 0
        for i in range(0, len(score)):
            digit = int(score[i])
            tileImage = pygame.image.load(TextPath + "text0" + str(32 + digit) + ".png")
            tileImage = pygame.transform.scale(tileImage, (tile, tile))
            screen.blit(tileImage, ((scoreStart + 2 + index) * tile, tile + 4, tile, tile))
            index += 1

        index = 0
        for i in range(highScoreStart, highScoreStart+len(textHighScore)):
            tileImage = pygame.image.load(TextPath + textHighScore[index])
            tileImage = pygame.transform.scale(tileImage, (tile, tile))
            screen.blit(tileImage, (i * tile, 4, tile, tile))
            index += 1

        highScore = str(self.highScore)
        if highScore == "0":
            highScore = "00"
        index = 0
        for i in range(0, len(highScore)):
            digit = int(highScore[i])
            tileImage = pygame.image.load(TextPath + "text0" + str(32 + digit) + ".png")
            tileImage = pygame.transform.scale(tileImage, (tile, tile))
            screen.blit(tileImage, ((highScoreStart + 6 + index) * tile, tile + 4, tile, tile))
            index += 1

    def drawBerry(self):
        """
        Vẽ trái cây trên màn hình.
        """
        if self.levelTimer in range(self.berryState[0], self.berryState[1]) and not self.berryState[2]:
            # print("here")
            berryImage = pygame.image.load(ElementPath + self.berries[(self.level - 1) % 8])
            berryImage = pygame.transform.scale(berryImage, (int(tile * 1.5), int(tile * 1.5)))
            screen.blit(berryImage, (self.berryLocation[1] * tile, self.berryLocation[0] * tile, tile, tile))

    def drawPoints(self, points, row, col):
        """
        Vẽ điểm trên màn hình.

        Args:
            points (int): Số điểm cần hiển thị.
            row (int): Tọa độ dòng.
            col (int): Tọa độ cột.
        """
        pointStr = str(points)
        index = 0
        for i in range(len(pointStr)):
            digit = int(pointStr[i])
            tileImage = pygame.image.load(TextPath + "text" + str(224 + digit) + ".png")
            tileImage = pygame.transform.scale(tileImage, (tile//2, tile//2))
            screen.blit(tileImage, ((col) * tile + (tile//2 * index), row * tile - 20, tile//2, tile//2))
            index += 1

    def drawReady(self):
        """
        Hiển thị văn bản "READY!" trên màn hình.
        """
        ready = ["text274.png", "text260.png", "text256.png", "text259.png", "text281.png", "text283.png"]
        for i in range(len(ready)):
            char = pygame.image.load(TextPath + ready[i])
            char = pygame.transform.scale(char, (int(tile), int(tile)))
            screen.blit(char, ((11 + i) * tile, 20 * tile, tile, tile))
    
    def gameOverFunc(self):
        """
        Thực hiện chức năng khi thua trò chơi.
        """
        global running, onExitScreen
        
        if self.gameOverCounter == 12:
            pygame.time.wait(2000)
            self.recordHighScore()
            screen.fill((0, 0, 0))
            onExitScreen = True
            currentScreen.displayGameOverMenu()
 
            return

        # Resets the screen around pacman
        
        for ghost in self.ghosts:
            self.drawTilesAround(ghost.row, ghost.col)
        self.drawTilesAround(self.pacman.row, self.pacman.col)
        self.pacman.draw(self) 
        self.drawTilesAround(self.pacman.row, self.pacman.col)

        # Draws new image
        pacmanImage = pygame.image.load(ElementPath + "element" + str(116 + self.gameOverCounter) + ".png")
        pacmanImage = pygame.transform.scale(pacmanImage, (int(tile * 1.5), int(tile * 1.5)))
        screen.blit(pacmanImage, (self.pacman.col * tile + spriteOffset, self.pacman.row * tile + spriteOffset, tile, tile))
        pygame.display.update()
        
        
        pause(5000000)
        self.gameOverCounter += 1
        

    def displayLives(self):
        """
        Hiển thị số mạng còn lại trên màn hình.
        """
        livesLoc = [[34, 1], [34, 3], [34, 5]]
        for i in range(self.lives - 1):
            lifeImage = pygame.image.load(ElementPath + "element054.png")
            lifeImage = pygame.transform.scale(lifeImage, (int(tile * 1.5), int(tile * 1.5)))
            screen.blit(lifeImage, (livesLoc[i][1] * tile, livesLoc[i][0] * tile - spriteOffset, tile, tile))

    def displayBerries(self):
        """
        Hiển thị các quả dâu đã thu thập trên màn hình.
        """
        firstBerrie = [34, 26]
        for i in range(len(self.berriesCollected)):
            berrieImage = pygame.image.load(ElementPath + self.berriesCollected[i])
            berrieImage = pygame.transform.scale(berrieImage, (int(tile * 1.5), int(tile * 1.5)))
            screen.blit(berrieImage, ((firstBerrie[1] - (2*i)) * tile, firstBerrie[0] * tile + 5, tile, tile))

    def touchingPacman(self, row, col):
        """
        Kiểm tra xem một vị trí cụ thể có tiếp xúc với Pacman không.

        Args:
            row (float): Tọa độ dòng.
            col (float): Tọa độ cột.

        Returns:
            bool: True nếu vị trí đó tiếp xúc với Pacman, False nếu không.
        """
        if row - 0.5 <= self.pacman.row and row >= self.pacman.row and col == self.pacman.col:
            return True
        elif row + 0.5 >= self.pacman.row and row <= self.pacman.row and col == self.pacman.col:
            return True
        elif row == self.pacman.row and col - 0.5 <= self.pacman.col and col >= self.pacman.col:
            return True
        elif row == self.pacman.row and col + 0.5 >= self.pacman.col and col <= self.pacman.col:
            return True
        elif row == self.pacman.row and col == self.pacman.col:
            return True
        return False

    def newLevel(self):
        """
        Bắt đầu một cấp độ mới của trò chơi.
        """
        reset()
        if self.lives == 1:
            self.lives 
        self.lives += 1
        self.collected = 0
        self.started = False
        self.berryState = [200, 400, False]
        self.levelTimer = 0
        self.lockedIn = True
        for level in self.levels:
            level[0] = min((level[0] + level[1]) - 100, level[0] + 50)
            level[1] = max(100, level[1] - 50)
        random.shuffle(self.levels)
        index = 0
        for state in self.ghostStates:
            state[0] = randrange(2)
            state[1] = randrange(self.levels[index][state[0]] + 1)
            index += 1
        global gameBoard
        gameBoard = copy.deepcopy(boardPattern)
        self.render()

    def drawTilesAround(self, row, col):
        """
        Vẽ các ô xung quanh một vị trí cụ thể.

        Args:
            row (int): Tọa độ dòng.
            col (int): Tọa độ cột.
        """
        row = math.floor(row)
        col = math.floor(col)
        for i in range(row-2, row+3):
            for j in range(col-2, col+3):
                if i >= 3 and i < len(gameBoard) - 2 and j >= 0 and j < len(gameBoard[0]):
                    imageName = str(((i - 3) * len(gameBoard[0])) + j)
                    if len(imageName) == 1:
                        imageName = "00" + imageName
                    elif len(imageName) == 2:
                         imageName = "0" + imageName
                    # Get image of desired tile
                    imageName = "map" + imageName + ".png"
                    tileImage = pygame.image.load(BoardPath + imageName)
                    tileImage = pygame.transform.scale(tileImage, (tile, tile))
                    # Display image of tile
                    screen.blit(tileImage, (j * tile, i * tile, tile, tile))

                    if gameBoard[i][j] == 2: # Draw Tic-Tak
                        pygame.draw.circle(screen, pelletColor,(j * tile + tile//2, i * tile + tile//2), tile//4)
                    elif gameBoard[i][j] == 5: #Draw Special Tic-Tak
                        pygame.draw.circle(screen, pelletColor,(j * tile + tile//2, i * tile + tile//2), tile//2)
                    elif gameBoard[i][j] == 6: #Black Special Tic-Tak
                        pygame.draw.circle(screen, (0, 0, 0),(j * tile + tile//2, i * tile + tile//2), tile//2)

    # Flips Color of Special Tic-Taks
    def flipColor(self):
        """
        Tạo hiệu ứng nháy nháy của viên thuốc đặc biệt.
        """
        global gameBoard
        for i in range(3, len(gameBoard) - 2):
            for j in range(len(gameBoard[0])):
                if gameBoard[i][j] == 5:
                    gameBoard[i][j] = 6
                    pygame.draw.circle(screen, (0, 0, 0),(j * tile + tile//2, i * tile + tile//2), tile//2)
                elif gameBoard[i][j] == 6:
                    gameBoard[i][j] = 5
                    pygame.draw.circle(screen, (pelletColor),(j * tile + tile//2, i * tile + tile//2), tile//2)


    def checkSurroundings(self):
        """
        Kiểm tra xung quanh của Pacman và các Ghost để phát hiện va chạm.
        """
        # Check if pacman got killed
        for ghost in self.ghosts:
            if self.touchingPacman(ghost.row, ghost.col) and not ghost.attacked:
                if self.lives == 1:
                    print("Game Over") 
                    self.forcePlayMusic("death_1.wav")
                    self.gameOver = True
                    # Remove the ghosts from the screen
                    for ghost in self.ghosts:
                        self.drawTilesAround(ghost.row, ghost.col)
                    self.drawTilesAround(self.pacman.row, self.pacman.col)
                    self.pacman.draw(self)
                    pygame.display.update()
                    pause(10000000)
                    return
                
                self.started = False
                self.forcePlayMusic("pacman_death.wav")
                pygame.time.wait(2000)
                reset()

            elif self.touchingPacman(ghost.row, ghost.col) and ghost.isAttacked() and not ghost.isDead():
                ghost.setDead(True)
                ghost.setTarget()
                ghost.ghostSpeed = 1
                ghost.row = math.floor(ghost.row)
                ghost.col = math.floor(ghost.col)
                self.score += self.ghostScore
                self.points.append([ghost.row, ghost.col, self.ghostScore, 0])
                self.ghostScore *= 2
                self.forcePlayMusic("eat_ghost.wav")
                
                # Pausar el juego y mostrar ejercicio de derivadas
                self.pauseAndShowExercise()
                
                pygame.display.update()

    def pauseAndShowExercise(self):
        """
        Pausa el juego, muestra un ejercicio de derivadas, y verifica la respuesta del jugador.
        """
        # Pausar el juego
        self.paused = True

        # Ejercicio de derivadas
        exercise = "¿Cuál es la derivada de f(x) = 3x^2 + 5x + 2?"
        correct_answer = "6x + 5"

        font = pygame.font.Font(None, 36)
        input_box = pygame.Rect(50, height // 2, 600, 50)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = True
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            if text == correct_answer:
                                done = True
                            else:
                                text = ''
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            screen.fill((0, 0, 0))
            txt_surface = font.render(exercise, True, pygame.Color('white'))
            screen.blit(txt_surface, (input_box.x + 5, input_box.y - 30))
            txt_surface = font.render(text, True, color)
            width = max(600, txt_surface.get_width() + 10)
            input_box.w = width
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, color, input_box, 2)
            pygame.display.update()

            pygame.display.flip()

        # Reanudar el juego
        self.paused = False
        pygame.display.update()
        game.render()

    
    def displayDerivativeExercise(self):
        """
        Mostrar un ejercicio de derivadas en la pantalla.
        """
        font = pygame.font.Font(None, 36)
        text = font.render("Resuelve: d/dx (3x^2 + 2x + 1)", True, (255, 255, 255))
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
        pygame.display.update()

    

    def getCount(self):
        """
        Đếm xem Pacman đã ăn được bao nhiêu viên thuốc.
        """
        total = 0
        for i in range(3, len(gameBoard) - 2):
            for j in range(len(gameBoard[0])):
                if gameBoard[i][j] == 2 or gameBoard[i][j] == 5 or gameBoard[i][j] == 6:
                    total += 1
        return total

    def getHighScore(self):
        """
        Lấy thông tin điểm số cao nhất từ file HighScore.txt được lưu ở Folder HighScoreSaved.
        """
        file = open(DataPath + "HighScore.txt", "r")
        highScore = int(file.read())
        file.close()
        return highScore

    def recordHighScore(self):
        """
        Ghi nhận điểm số cao nhất vào file HighScore.txt được lưu ở Folder HighScoreSaved.
        """
        file = open(DataPath + "HighScore.txt", "w").close()
        file = open(DataPath + "HighScore.txt", "w+")
        file.write(str(self.highScore))
        file.close()
        
game = Game(1, 0)
ghostsafeArea = [15, 13] # The location the ghosts escape to when attacked
ghostGate = [[15, 13], [15, 14]]

# Reset after death
def reset():
    """
        Reset vị trí đối tượng và tiếp tục màn chơi khi bị ma bắt (Vẫn còn mạng nên chưa thua).
    """
    global game
    game.ghosts = [Ghost(game, 14.0, 13.5, "red", 0), Ghost(game, 17.0, 11.5, "blue", 1), Ghost(game, 17.0, 13.5, "pink", 2), Ghost(game, 17.0, 15.5, "orange", 3)]
    for ghost in game.ghosts:
        ghost.setTarget()
    game.pacman = Pacman(26.0, 13.5, game)
    game.lives -= 1
    game.paused = True
    game.render()

def hardReset():
    """
        Reset lại màn chơi thành từ đầu (Đã sử dụng hết mạng và thua).
    """
    global game, gameBoard
    game.ghosts = [Ghost(game, 14.0, 13.5, "red", 0), Ghost(game, 17.0, 11.5, "blue", 1), Ghost(game, 17.0, 13.5, "pink", 2), Ghost(game, 17.0, 15.5, "orange", 3)]
    for ghost in game.ghosts:
        ghost.setTarget()
    game.pacman = Pacman(26.0, 13.5, game)
    game.lives += 2
    game.paused = True
    game.collected = 0
    game.score = 0
    game.gameOverCounter = 0
    gameBoard = copy.deepcopy(boardPattern)
    game.berriesCollected = []
    game.render()
    

currentScreen = displayMenu()
currentScreen.displayLaunchMenu()
running = True
onLaunchScreen = True
onExitScreen = False

clock = pygame.time.Clock()

def pause(time):
    """
        Một khoảng nghỉ nhỏ giữa các sự kiện xảy ra trong trò chơi.
    """
    cur = 0
    while not cur == time:
        cur += 1

while running:
    clock.tick(40)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            game.recordHighScore()
        elif event.type == pygame.KEYDOWN:
            game.paused = False
            game.started = True
            if event.key in COMMAND_KEYS["UP"]:
                if not onLaunchScreen and not onExitScreen:
                    game.pacman.newDir = 0
            elif event.key in COMMAND_KEYS["RIGHT"]:
                if not onLaunchScreen and not onExitScreen:
                    game.pacman.newDir = 1
            elif event.key in COMMAND_KEYS["DOWN"]:
                if not onLaunchScreen and not onExitScreen:
                    game.pacman.newDir = 2
            elif event.key in COMMAND_KEYS["LEFT"]:
                if not onLaunchScreen and not onExitScreen:
                    game.pacman.newDir = 3
            elif event.key == pygame.K_SPACE:
                if onLaunchScreen:
                    onLaunchScreen = False
                    game.paused = True
                    game.started = False
                    game.render()
                    pygame.mixer.music.load(SoundPath + "pacman_beginning.wav")
                    pygame.mixer.music.play()
                    musicPlaying = 1
                elif onExitScreen:
                    onExitScreen = False
                    game.paused = True
                    game.started = False
                    game.render()
                    game.gameOver = False
                    hardReset()
                    pygame.mixer.music.load(SoundPath + "pacman_beginning.wav")
                    musicPlaying = 1
                    pygame.mixer.music.play()
            elif event.key == pygame.K_RETURN:
                running = False
                game.recordHighScore()                                                                                

    if not onLaunchScreen and not onExitScreen:
        game.update()
