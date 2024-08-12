import pygame

TextPath = "Assets/Sprites/TextSprites/"
tile = 25
screen = pygame.display.set_mode((700, 900))

class MenuElements:
    """
        Lớp đại diện cho các hình ảnh và dữ liệu cho menu của trò chơi.
    """
    def __init__(self):
        """
        Khởi tạo các hình ảnh và dữ liệu cho menu của trò chơi.
        """
        self.gameTitle = ["text016.png", "text000.png", "text448.png", "text012.png", "text000.png", "text013.png"]
        self.characterTitle = [
            # Character
            "text002.png", "text007.png", "text000.png", "text018.png", "text000.png", "text002.png", "text020.png", "text004.png", "text018.png",
            # /
            "text015.png", "text042.png", "text015.png",
            # Nickname
            "text013.png", "text008.png", "text002.png", "text010.png", "text013.png", "text000.png", "text012.png", "text004.png"
        ]
        self.characters = [
            # Red Ghost
            [
                "text449.png", "text015.png", "text107.png", "text015.png", "text083.png", "text071.png", "text064.png", "text067.png", "text078.png", "text087.png",
                "text015.png", "text015.png", "text015.png", "text015.png",
                "text108.png", "text065.png", "text075.png", "text072.png", "text077.png", "text074.png", "text089.png", "text108.png"
            ],
            # Pink Ghost
            [
                "text450.png", "text015.png", "text363.png", "text015.png", "text339.png", "text336.png", "text324.png", "text324.png", "text323.png", "text345.png",
                "text015.png", "text015.png", "text015.png", "text015.png",
                "text364.png", "text336.png", "text328.png", "text333.png", "text330.png", "text345.png", "text364.png"
            ],
            # Blue Ghost
            [
                "text452.png", "text015.png", "text363.png", "text015.png", "text193.png", "text192.png", "text211.png", "text199.png", "text197.png", "text213.png", "text203.png",
                "text015.png", "text015.png", "text015.png",
                "text236.png", "text200.png", "text205.png", "text202.png", "text217.png", "text236.png"
            ],
            # Jala U 
            [
                "text453.png", "text015.png", "text235.png", "text015.png", "text201.png", "text192.png", "text203.png", "text192.png", "text015.png" , "text213.png"

            ]
        ]
        # Draw Pacman & Ghosts
        self.event = ["text449.png", "text015.png", "text452.png", "text015.png", "text015.png", "text448.png", "text453.png", "text015.png", "text015.png", "text015.png", "text453.png"]
        # Draw Platform Line
        self.wall = ["text454.png", "text454.png", "text454.png", "text454.png", "text454.png", "text454.png", "text454.png", "text454.png", "text454.png", "text454.png", "text454.png", "text454.png", "text454.png", "text454.png", "text454.png"]
        # "Calculo"     
        self.credit = ["text440.png", "text440.png", "text066.png", "text064.png", "text075.png", "text066.png", "text085.png", "text075.png", "text078.png","text440.png", "text418.png", "text440.png"]
        # "Press Space to Play"
        self.toplay = ["text016.png", "text018.png", "text004.png", "text019.png", "text019.png", "text015.png", "text019.png", "text016.png", "text000.png", "text002.png", "text004.png", "text015.png", "text020.png", "text014.png", "text015.png", "text016.png", "text011.png", "text000.png", "text025.png"]
        # "Press Enter to Exit"
        self.toexit = ["text016.png", "text018.png", "text004.png", "text019.png", "text019.png", "text015.png", "text004.png", "text013.png", "text020.png", "text004.png", "text018.png", "text015.png", "text020.png", "text014.png", "text015.png", "text004.png", "text024.png", "text008.png", "text020.png"]
        # "Game Over"
        self.gameover = ["text070.png", "text064.png", "text076.png", "text068.png", "text079.png", "text078.png", "text086.png", "text068.png", "text082.png"]
        # "You Won"
        self.youwon = ["text217.png", "text206.png", "text213.png", "text207.png", "text215.png", "text206.png", "text205.png"]
        
    def drawGameTitle(self):
        """
        Vẽ tiêu đề của game.
        """
        for i in range(len(self.gameTitle)):
            char = pygame.image.load(TextPath + self.gameTitle[i])
            char = pygame.transform.scale(char, (int(tile * 4), int(tile * 4)))
            screen.blit(char, ((2 + 4 * i) * tile, 2 * tile, tile, tile))

    def drawCharacterTitle(self):
        """
        Vẽ dòng chữ "Character / Nickname".
        """
        for i in range(len(self.characterTitle)):
            char = pygame.image.load(TextPath + self.characterTitle[i])
            char = pygame.transform.scale(char, (int(tile), int(tile)))
            screen.blit(char, ((4 + i) * tile, 10 * tile, tile, tile))

    def drawCharactersAndNicknames(self):
        """
        Vẽ tên và nickname của những con ma.
        """
        for i in range(len(self.characters)):
            for j in range(len(self.characters[i])):
                if j == 0:
                    char = pygame.image.load(TextPath + self.characters[i][j])
                    char = pygame.transform.scale(char, (int(tile * 1.5), int(tile * 1.5)))
                    screen.blit(char, ((2 + j) * tile - tile//2, (12 + 2 * i) * tile - tile//3, tile, tile))
                else:
                    char = pygame.image.load(TextPath + self.characters[i][j])
                    char = pygame.transform.scale(char, (int(tile), int(tile)))
                    screen.blit(char, ((2 + j) * tile, (12 + 2 * i) * tile, tile, tile))

    def drawPacmanAndGhosts(self):
        """
        Vẽ hình ảnh của Pacman và các con ma trên màn hình.
        """
        for i in range(len(self.event)):
            ele = pygame.image.load(TextPath + self.event[i])
            ele = pygame.transform.scale(ele, (int(tile * 2), int(tile * 2)))
            screen.blit(ele, ((4 + i * 2) * tile, 24 * tile, tile, tile))

    def drawPlatformLine(self):
        """
        Vẽ vệt đường đi ngang qua màn hình Menu.
        """
        for i in range(len(self.wall)):
            platform = pygame.image.load(TextPath + self.wall[i])
            platform = pygame.transform.scale(platform, (int(tile * 2), int(tile * 2)))
            screen.blit(platform, ((i * 2) * tile, 26 * tile, tile, tile))

    def drawCredit(self):
        """
        Vẽ tên người làm trò chơi.
        """
        for i in range(len(self.credit)):
            char = pygame.image.load(TextPath + self.credit[i])
            char = pygame.transform.scale(char, (int(tile*1.5), int(tile*1.5)))
            screen.blit(char, ((4.3 + 1.5 * i) * tile, 28.75 * tile, tile, tile))

    def drawGameOver(self):
        """
        Vẽ dòng kí tự "Game Over"
        """
        for i in range(len(self.gameover)):
            char = pygame.image.load(TextPath + self.gameover[i])
            char = pygame.transform.scale(char, (int(tile*1.5), int(tile*1.5)))
            screen.blit(char, ((7.25 + 1.5 * i) * tile, 28.75 * tile, tile, tile))
    
    def drawYouWon(self):
        """
        Vẽ dòng kí tự "You Won"
        """
        for i in range(len(self.youwon)):
            char = pygame.image.load(TextPath + self.youwon[i])
            char = pygame.transform.scale(char, (int(tile*1.5), int(tile*1.5)))
            screen.blit(char, ((8.5 + 1.5 * i) * tile, 28.75 * tile, tile, tile))

    def drawPressToPlay(self):
        """
        Vẽ dòng kí tự "Press Space to Play"
        """
        for i in range(len(self.toplay)):
                        char = pygame.image.load(TextPath + self.toplay[i])
                        char = pygame.transform.scale(char, (int(tile), int(tile)))
                        screen.blit(char, ((4.5 + i) * tile, 32.5 * tile - 10, tile, tile))
    
    def drawPressToExit(self):
        """
        Vẽ dòng kí tự "Press Enter to Exit"
        """
        for i in range(len(self.toexit)):
            char = pygame.image.load(TextPath + self.toexit[i])
            char = pygame.transform.scale(char, (int(tile), int(tile)))
            screen.blit(char, ((4.5 + i) * tile, 35 * tile - 10, tile, tile))

class displayMenu(MenuElements):
    def displayLaunchMenu(self):
        """
        Hiển thị màn hình menu khi bắt đầu chơi.
        """
        self.drawGameTitle()
        self.drawCharacterTitle()
        self.drawCharactersAndNicknames()
        self.drawPacmanAndGhosts()
        self.drawPlatformLine()
        self.drawCredit()
        self.drawPressToPlay()
        self.drawPressToExit()
        pygame.display.update()  
    def displayGameOverMenu(self):
        """
        Hiển thị màn hình menu khi thua trò chơi.
        """
        self.drawGameTitle()
        self.drawCharacterTitle()
        self.drawCharactersAndNicknames()
        self.drawPacmanAndGhosts()
        self.drawPlatformLine()
        self.drawGameOver()
        self.drawPressToPlay()
        self.drawPressToExit()
        pygame.display.update()  
    def displayYouWonMenu(self):
        """
        Hiển thị màn hình menu khi thắng trò chơi.
        """
        self.drawGameTitle()
        self.drawCharacterTitle()
        self.drawCharactersAndNicknames()
        self.drawPacmanAndGhosts()
        self.drawPlatformLine()
        self.drawYouWon()
        self.drawPressToPlay()
        self.drawPressToExit()
        pygame.display.update()  
livesLoc = [[34, 3], [34, 1]] 
print(livesLoc[1][0])
