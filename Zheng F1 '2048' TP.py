from cmu_graphics import *
import random
from PIL import Image
import os, pathlib
import csv

#draw background by setting rectangle to app.width and height
class gameBoard:
    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.boardLeft = 75
        self.boardTop = 150
        self.boardWidth = 400
        self.boardHeight = 400
        self.cellBorderWidth = 4
        self.board = [([None] * self.cols) for row in range(self.rows)]
    
    def game_redrawAllBoard(self):
        self.game_drawBoard()
        self.game_drawBoardBorder()
        self.game_drawCell

    def game_drawBoard(self):
        for row in range(self.rows):
            for col in range(self.cols):
                color = self.board[row][col]
                self.game_drawCell(row, col, color)

    def game_drawBoardBorder(self):
        drawRect(self.boardLeft, self.boardTop, self.boardWidth, self.boardHeight,
                fill = None, border = 'white',
                borderWidth = 2*self.cellBorderWidth)

    def game_drawCell(self, row, col, teamIndex):
        cellLeft, cellTop = self.getCellLeftTop(row, col)
        cellWidth, cellHeight = self.getCellSize()
        drawRect(cellLeft, cellTop, cellWidth, cellHeight,
                 fill=None, border='white', borderWidth=self.cellBorderWidth)


    def getCellLeftTop(self, row, col):
        cellWidth, cellHeight = self.getCellSize()
        cellLeft = self.boardLeft + col * cellWidth
        cellTop = self.boardTop + row * cellHeight
        return (cellLeft, cellTop)

    def getCellSize(self):
        cellWidth = self.boardWidth/self.cols
        cellHeight = self.boardHeight/self.rows
        return(cellWidth, cellHeight)

    def resetBoard(self):
        self.board = [([None] * self.cols) for row in range(self.rows)]

class Game2048:
    highestScore = 0

    def __init__(self, rows, cols, width, height):
        self.gameBoard = gameBoard(rows, cols, width, height)
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.board = [([None] * self.cols) for row in range(self.rows)]
        self.currScoreLeft = 130
        self.currScoreTop = 110
        self.currScoreWidth = 110
        self.currScoreHeight = 22
        self.hiScoreLeft = 305
        self.hiScoreTop = 110
        self.hiScoreWidth = 110
        self.hiScoreHeight = 22
        self.gameOver = False
        self.currentTileRow = self.rows - 1
        self.currentTileCol = 0

        #seasons
        self.season2021 = False
        self.season2022 = False
        self.season2023 = False
        self.teamSeason = range(10)
        self.tileTeams= ['images/haasLogo.jpg',
                        'images/alfaRomeoLogo.png',
                        'images/williamsLogog.jpg',
                        'images/asMLogo.png',
                        'images/alphaTauriLogo.jpg',
                        'images/alpineLogo.png',
                        'images/mclarenLogo.jpg',
                        'images/ferrariLogo.png',
                        'images/redBullLogo.png', 
                        'images/mercedesLogo.png',

                        'images/williamsLogog.jpg',
                        'images/alphaTauriLogo.jpg',
                        'images/haasLogo.jpg',
                        'images/asMLogo.png', 
                        'images/alfaRomeoLogo.png',
                        'images/mclarenLogo.jpg',
                        'images/alpineLogo.png',
                        'images/mercedesLogo.png',
                        'images/ferrariLogo.png', 
                        'images/redBullLogo.png',

                        "images/haasLogo.jpg", 
                        "images/alfaRomeoLogo.png", 
                        "images/alphaTauriLogo.jpg", 
                        "images/williamsLogog.jpg", 
                        "images/alpineLogo.png",
                        "images/asMLogo.png", 
                        "images/mclarenLogo.jpg", 
                        "images/ferrariLogo.png", 
                        "images/mercedesLogo.png", 
                        "images/redBullLogo.png" ]
        
        self.tileTeamScores= {'images/haasLogo.jpg':0,
                          'images/alfaRomeoLogo.png':13,
                          'images/williamsLogog.jpg':23,
                          'images/asMLogo.png':77,
                          'images/alphaTauriLogo.jpg':142,
                          'images/alpineLogo.png':155,
                          'images/mclarenLogo.jpg':275,
                          'images/ferrariLogo.png':323,
                          'images/redBullLogo.png':585, 
                          'images/mercedesLogo.png':613,

                          'images/williamsLogog.jpg':8,
                          'images/alphaTauriLogo.jpg':35,
                          'images/haasLogo.jpg':37,
                          'images/asMLogo.png':55, 
                          'images/alfaRomeoLogo.png':55,
                          'images/mclarenLogo.jpg':159,
                          'images/alpineLogo.png':173,
                          'images/mercedesLogo.png':515,
                          'images/ferrariLogo.png':554, 
                          'images/redBullLogo.png':759,

                          "images/haasLogo.jpg":12, 
                          "images/alfaRomeoLogo.png":16, 
                          "images/alphaTauriLogo.jpg":25, 
                          "images/williamsLogog.jpg":28, 
                          "images/alpineLogo.png":120,
                          "images/asMLogo.png":280, 
                          "images/mclarenLogo.jpg":302, 
                          "images/ferrariLogo.png":406, 
                          "images/mercedesLogo.png":409, 
                          "images/redBullLogo.png":860}
    
        self.currentScore = 0

        #for hint button
        self.showHint = True
        self.hintTop = 18
        self.hintLeft = 438
        self.hintWidth = 55
        self.hintHeight = 33

        #for hint on board
        self.hintStartRow = None
        self.hintStartCol = None
        self.hintEndRow = None
        self.hintEndCol = None

        #difficulty levels
        self.moves = []
        self.easyLevel = False
        self.normalLevel = False
        self.hardLevel = False
        self.hardLeft = 85
        self.hardTop = 400
        self.normalLeft = 205
        self.normalTop = 400
        self.easyLeft = 365
        self.easyTop = 400
        self.homeTop = 10
        self.homeLeft = 50
        self.homeWidth = 40
        self.homeHeight = 45

        # tile Images
        self.image = "images/f1logo.png"
        self.imageWidth = 0
        self.imageHeight = 0
        
        self.infoLeft = 190
        self.infoTop = 505

    
    def game_resetGame(self):
        self.__init__(self.rows, self.cols, self.width, self.height)
        setActiveScreen('season')
        self.updateScores()
        
    
    def game_drawLabels(self):
        drawRect(self.currScoreLeft, self.currScoreTop, self.currScoreWidth, self.currScoreHeight,
                    fill = 'crimson', opacity = 30, border ='black', borderWidth = 4)
        drawRect(self.hiScoreLeft, self.hiScoreTop, self.hiScoreWidth, self.hiScoreHeight,
                    fill = 'paleGreen', opacity = 30, border ='black', borderWidth = 4)
        drawLabel(self.currentScore, 180, 118, size = 16, bold = True, fill = 'white', font = 'orbitron')
        drawLabel(Game2048.highestScore, 357, 118, size = 16, fill = 'white', bold = True, font= 'orbitron')
       
        if self.hardLevel == True:
            drawLabel('Hard Level ON', 72, 135, size = 16, fill = 'royalBlue', bold = True)
        elif self.normalLevel:
            drawLabel('Normal Level ON', 70, 136, size = 16, fill = 'lightSkyBlue', bold = True)
        elif self.easyLevel:
            drawLabel('Easy Level ON', 72, 135, size = 16, fill = 'powderBlue', bold = True)

    def getCellLeftTop(self, row, col):
        return self.gameBoard.getCellLeftTop(row, col)
    
    def getCellSize(self):
        return self.gameBoard.getCellSize()
    
    def game_onMousePress(self, mouseX, mouseY):
        if (self.hintLeft <= mouseX <= self.hintLeft + self.hintWidth)and(self.hintTop <= mouseY <= self.hintTop + self.hintHeight):
            self.showHint = True
            self.getHint()
        elif ((self.homeLeft <= mouseX <= self.homeLeft + self.homeWidth) 
            and (self.homeTop <= mouseY <= self.homeTop + self.homeHeight)):
            self.game_resetGame()
            setActiveScreen('season')

    def game_draw(self):
        self.drawImageBackground()
        for row in range(self.rows):
            for col in range(self.cols):
                self.drawImageTiles(row, col)
        self.game_drawLabels()      
        self.gameBoard.game_redrawAllBoard()

    def game_onKeyPress(self, key):
        if self.gameOver == True:
            self.game_resetGame()
        elif key == 'r':
            setActiveScreen('welcome')
        elif key == 'left' or key == 'right' or key == 'up' or key == 'down':
            drow, dcol = 0,0
            if key == 'down':
                drow = 1
                self.moveDown()
            elif key == 'up':
                drow = -1
                self.moveUp()
            elif key == 'left':
                dcol = -1
                self.moveLeft()
            elif key == 'right':
                dcol = 1
                self.moveRight()
            self.mergeTiles(drow, dcol)
            self.addTile()

    def moveLeft(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] is not None:
                    newCol = col
                    while newCol > 0 and self.isCellEmpty(row, newCol - 1):
                        newCol -= 1
                    if newCol != col:
                        self.board[row][col], self.board[row][newCol] = self.board[row][newCol], self.board[row][col]
                        self.updateScores()

    def moveRight(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] is not None:
                    newCol = col
                    while newCol < self.cols -1 and self.isCellEmpty(row, newCol + 1):
                        newCol += 1
                    if newCol != col:
                        self.board[row][col], self.board[row][newCol] = self.board[row][newCol], self.board[row][col]
                        self.updateScores()

    def moveUp(self):
        for col in range(self.cols):
            for row in range(self.rows):
                    if self.board[row][col] is not None:
                        newRow = row
                        while newRow > 0 and self.isCellEmpty(newRow - 1, col):
                            newRow -= 1
                        if newRow != row:
                            self.board[row][col], self.board[newRow][col] = self.board[newRow][col], self.board[row][col]
                            self.updateScores()

    def moveDown(self):
        for col in range(self.cols):
            for row in range(self.rows):
                if self.board[row][col] is not None:
                    newRow = row
                    while newRow < self.rows - 1 and self.isCellEmpty(newRow + 1, col):
                        newRow += 1
                    if newRow != row:
                        self.board[row][col], self.board[newRow][col] = self.board[newRow][col], self.board[row][col]
                        self.updateScores()

    def isCellEmpty(self, newRow, newCol):
        return self.board[newRow][newCol] is None

            
    def getTile(self):
        if self.season2021:
            return random.choice(self.tileTeams[:2])
        elif self.season2022:
            return random.choice(self.tileTeams[10:12])
        elif self.season2023:
            return random.choice(self.tileTeams[20:22])
    
    def mergeTiles(self, drow, dcol):
        if drow == 1: #down arrow
            for col in range(self.cols):
                row =self.rows - 1
                while row > 0:
                    if self.board[row][col]==self.board[row-1][col]:
                        currentTile = self.board[row][col]
                        if currentTile is not None:
                            if self.season2021:
                                currTileIndex = (self.tileTeams.index(currentTile)) 
                                nextTileIndex = (currTileIndex + 1) % 10
                                self.board[row][col] = self.tileTeams[nextTileIndex] 
                            elif self.season2022:
                                currTileIndex = (self.tileTeams[10:20].index(currentTile)) 
                                nextTileIndex = (currTileIndex + 1) % 10
                                self.board[row][col] = self.tileTeams[10 + nextTileIndex]
                            elif self.season2023:
                                currTileIndex = (self.tileTeams[20:30].index(currentTile))
                                nextTileIndex = (currTileIndex + 1) % 10
                                self.board[row][col] = self.tileTeams[20 + nextTileIndex]
                            self.board[row-1][col] = None
                            self.currentScore += self.tileTeamScores[self.board[row][col]]
                            self.updateScores()
                        row -=2
                    elif self.board[row][col] is None:
                        break
                    else:
                        row -= 1

        elif drow == -1: #up arrow
            for col in range(self.cols):
                row = 0
                while row < self.rows - 1:
                    if self.board[row][col]==self.board[row+1][col]: 
                        currentTile = self.board[row][col]
                        if currentTile is not None:
                            if self.season2021:
                                currTileIndex = (self.tileTeams.index(currentTile))  
                                nextTileIndex = (currTileIndex + 1) % 10
                                self.board[row][col] = self.tileTeams[nextTileIndex] 
                            elif self.season2022:
                                currTileIndex = (self.tileTeams[10:20].index(currentTile)) 
                                nextTileIndex = (currTileIndex + 1) % 10
                                self.board[row][col] = self.tileTeams[10+nextTileIndex] 
                            elif self.season2023:
                                currTileIndex = (self.tileTeams[20:30].index(currentTile))
                                nextTileIndex = (currTileIndex + 1) % 10
                                self.board[row][col] = self.tileTeams[20 + nextTileIndex]
                            self.board[row][col] = self.tileTeams[nextTileIndex]
                            self.board[row+1][col] = None
                            self.currentScore += self.tileTeamScores[self.board[row][col]]
                            self.updateScores()
                        row +=2
                    elif self.board[row][col] is None:
                        break
                    else:
                        row += 1

        elif dcol == 1: # move right
            for row in range(self.rows):
                col = self.cols - 1
                while col > 0:
                    if self.board[row][col]==self.board[row][col-1]:
                        currentTile = self.board[row][col]
                        if currentTile is not None:
                            if self.season2021:
                                currTileIndex = (self.tileTeams.index(currentTile))  
                                nextTileIndex = (currTileIndex + 1) % 10
                                self.board[row][col] = self.tileTeams[nextTileIndex] 
                            elif self.season2022:
                                currTileIndex = (self.tileTeams[10:20].index(currentTile)) 
                                nextTileIndex = (currTileIndex + 1) % 10
                                self.board[row][col] = self.tileTeams[10+nextTileIndex] 
                            elif self.season2023:
                                currTileIndex = (self.tileTeams[20:30].index(currentTile))
                                nextTileIndex = (currTileIndex + 1) % 10
                                self.board[row][col] = self.tileTeams[20 + nextTileIndex]
                            self.board[row][col-1] = None
                            self.currentScore += self.tileTeamScores[self.board[row][col]]
                            self.updateScores()
                        col -=2
                    elif self.board[row][col] is None:
                        break
                    else:
                        col -= 1

        elif dcol == -1: # move left
            for row in range(self.rows):
                col = 0
                while col < self.cols - 1:
                    if self.board[row][col]==self.board[row][col+1]:
                        currentTile = self.board[row][col]
                        if currentTile is not None:
                            if self.season2021:
                                currTileIndex = (self.tileTeams.index(currentTile))  
                                nextTileIndex = (currTileIndex + 1) % 10
                                self.board[row][col] = self.tileTeams[nextTileIndex] 
                            elif self.season2022:
                                currTileIndex = (self.tileTeams[10:20].index(currentTile)) 
                                nextTileIndex = (currTileIndex + 1) % 10
                                self.board[row][col] = self.tileTeams[10+nextTileIndex] 
                            elif self.season2023:
                                currTileIndex = (self.tileTeams[20:30].index(currentTile))
                                nextTileIndex = (currTileIndex + 1) % 10
                                self.board[row][col] = self.tileTeams[20 + nextTileIndex]
                            self.board[row][col+1] = None
                            self.currentScore += self.tileTeamScores[self.board[row][col]]
                            self.updateScores()
                        col+=2
                    elif self.board[row][col] is None:
                        break
                    else:
                        col += 1

    def updateScores(self):
        Game2048.highestScore = max(self.currentScore, Game2048.highestScore)

    def game_isGameOver(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] is None:
                    return self.gameOver == False
        self.gameOver = True
        drawLabel('GAME OVER', 275, 300, size=30, bold = True, fill = 'lightGreen')
   
    def getHint(self):
       result = self.mostOptimalMove(self.currentTileRow, self.currentTileCol)
       if result is not None:
           self.hintStartRow, self.hintStartCol, self.hintEndRow, self.hintEndCol = result
           self.showHint = True

    def game_drawHint(self):
        if self.hintStartRow is not None:
            cellWidth, cellHeight = self.getCellSize()
            hintLeft, hintTop = self.getCellLeftTop(self.hintStartRow, self.hintStartCol)
            hintWidth = (self.hintEndCol - self.hintStartCol + 1) * cellWidth
            hintHeight = (self.hintEndRow - self.hintStartRow + 1) * cellHeight

            if self.showHint == True:
                drawRect(hintLeft, hintTop, hintWidth, hintHeight, fill = None, border = 'red', borderWidth = 4)
                self.showHint = False

        #by using backtracking, find out the most optimal move(up, down, left, or right) that would allow for the highest score

    def mostOptimalMove(self, currRow, currCol):
       result = self.mostOptimalMoveHelper(currRow, currCol, None)
       if result is not None:
           return result[0]
       return None
  
    def mostOptimalMoveHelper(self, currRow, currCol, currBestMove):
        if currBestMove is None:
            currBestMove = ((currRow, currCol, currRow, currCol), 0)

        currTile = self.board[currRow][currCol]
        for scalar in range(1, len(self.board)):
            for drow, dcol in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                nextRow = currRow + drow * scalar
                nextCol = currCol + dcol * scalar


                if self.isLegalMove(currRow, currCol, nextRow, nextCol):
                    nextTile = self.board[nextRow][nextCol]


                    if (currTile in self.tileTeams and nextTile in self.tileTeamScores) and (currTile == nextTile):
                        newRow, newCol = nextRow, nextCol
                        currMove = (currRow, currCol, newRow, newCol)
                        moveScore = self.moveScoreHelper(currMove)
                        if moveScore > currBestMove[1]:
                            currBestMove = (currMove, moveScore)
                        currBestMove = self.mostOptimalMoveHelper(newRow, newCol, currBestMove)
        return currBestMove
    
    def isLegalMove(self, rows, cols, nextRow, nextCol):
        return 0 <= nextRow < rows and 0 <= nextCol < cols

    def movesAvailable(self, row, col):
        self.moves = []
        for drow, dcol in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nextRow, nextCol = row +drow, col +dcol
            if  self.isLegalMove(row, col, nextRow, nextCol):
                self.canMove(drow, dcol, row, col)
        return len(self.moves)
    
    def canMove(self, drow, dcol, currRow, currCol):
        nextRow, nextCol = currRow + drow, currCol + dcol
        if self.isLegalMove(currRow, currCol, nextRow, nextCol):
            nextTile = self.board[nextRow][nextCol]
            if nextTile is not None and self.board[currRow][currCol] in self.tileTeams == nextTile:
                self.moves.append((nextRow, nextCol))
            if nextTile is not None:
                self.canMove(drow, dcol, nextRow, nextCol)
           
    def addTile(self):
        if self.hardLevel:
            possibleMoves = self.movesAvailable(self.currentTileRow, self.currentTileCol)
            if possibleMoves > 0:
                moveIndex = random.randint(0, len(self.moves))
                (row, col) = self.moves[moveIndex]
                newTile = self.getTile()
                self.board[row][col] = newTile
                self.currentScore += self.tileTeamScores[newTile]
                self.updateScores()
            else:
                emptyCells = [(row, col) for row in range(self.rows) for col in range(self.cols) if self.board[row][col] is None]
                if emptyCells:
                    randomIndex = random.randint(0, len(emptyCells)-1)
                    row, col = emptyCells[randomIndex]
                    if self.season2021:
                        newTile =random.choice(self.tileTeams[:2])
                    elif self.season2022:
                        newTile =random.choice(self.tileTeams[10:12])
                    elif self.season2023:
                        newTile =random.choice(self.tileTeams[20:22])
                    else:
                        newTile = self.getTile()
                    if newTile is not None:
                        self.board[row][col] = newTile
                        self.currentScore += self.tileTeamScores[newTile]
                        self.updateScores()
                    else:
                        self.gameOver = True

        elif self.normalLevel == True:
            emptyCells = [(row, col) for row in range(self.rows) for col in range(self.cols) if self.board[row][col] is None]
            if emptyCells:
                randomIndex = random.randint(0, len(emptyCells)-1)
                row, col = emptyCells[randomIndex]
                if self.season2021:
                    newTile =random.choice(self.tileTeams[:2])
                elif self.season2022:
                    newTile =random.choice(self.tileTeams[10:12])
                elif self.season2023:
                    newTile =random.choice(self.tileTeams[20:22])
                else:
                    newTile = self.getTile()
                if newTile is not None:
                    self.board[row][col] = newTile
                    self.currentScore += self.tileTeamScores[newTile]
                    self.updateScores()
                else:
                    self.gameOver = True
        
        elif self.easyLevel == True:
            emptyCellsEasy = [(row, col) for row in range(self.rows) for col in range(self.cols) if self.board[row][col] is None]
            if emptyCellsEasy:
                randomIndex = random.randint(0, len(emptyCellsEasy)-1)
                row, col = emptyCellsEasy[randomIndex]
                possibleMoves = self.movesAvailable(row, col)
                if possibleMoves > 0:
                    for (row, col) in self.moves:
                        if (row, col) in self.moves:
                            emptyCellsEasy.pop((row, col))
                        else:
                            newTile = self.getTile()
                            self.board[row][col] = newTile
                            self.currentScore += self.tileTeamScores[newTile]
                            self.updateScores()
                else:
                    emptyCells = [(row, col) for row in range(self.rows) for col in range(self.cols) if self.board[row][col] is None]
                    if emptyCells:
                        randomIndex = random.randint(0, len(emptyCells)-1)
                        row, col = emptyCells[randomIndex]
                        if self.season2021:
                            newTile =random.choice(self.tileTeams[:2])
                        elif self.season2022:
                            newTile =random.choice(self.tileTeams[10:12])
                        elif self.season2023:
                            newTile =random.choice(self.tileTeams[20:22])
                        else:
                            newTile = self.getTile()
                        if newTile is not None:
                            self.board[row][col] = newTile
                            self.currentScore += self.tileTeamScores[newTile]
                            self.updateScores()
                        else:
                            self.gameOver = True
            else:
                self.gameOver = True
    
    def onAppStart(self, newTile):
        self.image = Image.open(os.path.join(pathlib.Path(__file__).parent,self.tileTeams[newTile]))
        self.imageWidth, self.imageHeight = self.image.width, self.image.height

        def openImage(fileName):
            return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))
        self.image = openImage(self.tileTeams[newTile])  
    
    def drawImageBackground(self):
    # drawPILImage takes in a PIL image object and the left-top coordinates
        drawImage("images/gameTemp.png",0,0)

    def drawImageTiles(self, row, col):
        if self.board[row][col] is not None:
            tileImage = self.board[row][col]
            cellLeft, cellTop = self.getCellLeftTop(row, col)
            imageLeft = cellLeft + 4
            imageTop = cellTop + 4
            drawImage(tileImage, imageLeft, imageTop)


    def welcome_redrawAll(self):
        drawLabel("Welcome to F1 '2048'", self.width/2, self.height/2 -75, font='Comic Sans MS',size = 40)
        drawLabel('Choose a Difficulty Level:', self.width/2, self.height/2 + 10, size = 24)
        drawRect(self.hardLeft, self.hardTop, 170, 35, border = 'black', borderWidth = 3, fill = None)
        drawRect(self.normalLeft, self.normalTop, 170, 35, border = 'black', borderWidth = 3, fill = None)
        drawRect(self.easyLeft, self.easyTop, 170, 35, border = 'black', borderWidth = 3, fill = None)
        drawLabel('HARD', 95, 372.5, size = 24)
        drawLabel('NORMAL', 275, 372.5, size = 24)
        drawLabel('EASY', 455, 372.5, size = 22)
        drawRect(self.infoLeft, self.infoTop, 165, 50, border = 'black', fill = 'red')
        drawLabel('Game Info', 275, 500, size = 18, bold = True)

    def welcome_onAppStart(self):
        self.image = Image.open(os.path.join(pathlib.Path(__file__).parent,"images/welcome.jpg"))

        def openImage(fileName):
            return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))
        self.image = openImage("images/welcome.jpg")  
    
    def welcome_drawImage(self):
        drawImage("images/welcome.jpg", 0 ,0)
    
    def isBoardEmpty(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] is not None:
                    return False
        return True
    
    def welcome_onMousePress(self, mouseX, mouseY):
        if (self.hardLeft <= mouseX <= self.hardLeft + 170) and (self.hardTop <= mouseY <= self.hardTop + 35):
            setActiveScreen('game')
            self.hardLevel = True
            self.easyLevel = False
            self.normalLevel = False
            if self.isBoardEmpty():
                self.addTile()
                self.addTile()
            
        elif (self.normalLeft <= mouseX <= self.normalLeft + 170) and (self.normalTop <= mouseY <= self.normalTop + 35):
            setActiveScreen('game')
            self.normalLevel = True
            self.easyLevel = False
            self.hardLevel = False
            if self.isBoardEmpty():
                self.addTile()
                self.addTile()
        elif (self.easyLeft <= mouseX <= self.easyLeft + 170) and (self.easyTop <= mouseY <= self.easyTop + 35):
            setActiveScreen('game')
            self.easyLevel = True
            self.normalLevel = False
            self.hardLevel = False
            if self.isBoardEmpty():
                self.addTile()
                self.addTile()
        elif (self.infoLeft <= mouseX <= self.infoLeft +165) and (self.infoTop <= mouseY <= self.infoTop + 50):
            setActiveScreen('info')

    def season_onAppStart(self):
        self.image = Image.open(os.path.join(pathlib.Path(__file__).parent,"images/introSeason.PNG.jpg"))

        def openImage(fileName):
            return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))
        self.image = openImage("images/introSeason.PNG.jpg")  

    def season_redrawAll(self):
        drawLabel("Welcome to F1 '2048'", self.width/2, self.height/2 -75, font='Comic Sans MS',size = 40)
        drawLabel('Choose a Season:', self.width/2, self.height/2 + 10, size = 24)
        drawRect(self.hardLeft, self.hardTop, 170, 35, border = 'black', borderWidth = 3, fill = None)
        drawRect(self.normalLeft, self.normalTop, 170, 35, border = 'black', borderWidth = 3, fill = None)
        drawRect(self.easyLeft, self.easyTop, 170, 35, border = 'black', borderWidth = 3, fill = None)
        drawLabel('2021', 95, 372.5, size = 24)
        drawLabel('2022', 275, 372.5, size = 24)
        drawLabel('2023', 455, 372.5, size = 22)

    def season_drawImage(self):
        drawImage("images/introSeason.PNG.jpg", 0,0)

    def season_onMousePress(self, mouseX, mouseY):
        if (self.hardLeft <= mouseX <= self.hardLeft + 170) and (self.hardTop <= mouseY <= self.hardTop + 35):
            self.season2021 = True
            self.teamSeason = range(10)
            setActiveScreen('welcome')
        elif (self.normalLeft <= mouseX <= self.normalLeft + 170) and (self.normalTop <= mouseY <= self.normalTop + 35):
            self.season2022 = True
            self.teamSeason = range(10,20)
            setActiveScreen('welcome')
        elif (self.easyLeft <= mouseX <= self.easyLeft + 170) and (self.easyTop <= mouseY <= self.easyTop + 35):
            self.season2023 = True
            self.teamSeason = range(20, 30)
            setActiveScreen('welcome')


class InfoScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.text = 'Welcome to F1 2048.'
        self.homeLeft = 50
        self.homeTop = 12
        self.homeWidth = 44
        self.homeHeight = 40

    def info_onAppStart(self):
        self.image = Image.open(os.path.join(pathlib.Path(__file__).parent,"images/infoPage.jpg"))

        def openImage(fileName):
            return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))
        self.image = openImage("images/infoPage.jpg")  

    def info_drawImage(self):
        drawImage("images/infoPage.jpg", 0,0)
            
    def info_onMousePress(self, mouseX, mouseY):
        if (self.homeLeft <= mouseX <= self.homeLeft + self.homeWidth) and (self.homeTop <= mouseY <= self.homeTop + self.homeHeight):
            setActiveScreen('welcome')

def season_onAppStart(app):
    app.game.season_onAppStart()

def season_redrawAll(app):
    app.game.season_redrawAll()
    app.game.season_drawImage()

def season_onMousePress(app, mouseX, mouseY):
    app.game.season_onMousePress(mouseX, mouseY)

def welcome_redrawAll(app):
    app.game.welcome_redrawAll()
    app.game.welcome_drawImage()

def welcome_onMousePress(app, mouseX, mouseY):
   app.game.welcome_onMousePress(mouseX, mouseY)

def info_redrawAll(app):
    app.info.info_drawImage()

def info_onMousePress(app, mouseX, mouseY):
    app.info.info_onMousePress(mouseX, mouseY)
    
def game_redrawAll(app):
    app.game.game_draw()
    app.game.game_isGameOver()
    app.board.game_redrawAllBoard()
    possibleMoves = app.game.movesAvailable(app.game.currentTileRow, app.game.currentTileCol)
    drawLabel(f'possible moves: {possibleMoves}', 50, 100)
    app.game.game_drawHint()

def game_onMousePress(app, mouseX, mouseY):
    app.game.game_onMousePress(mouseX, mouseY)

def game_onKeyPress(app, key):
    app.game.game_onKeyPress(key)

def main():
   app.board = gameBoard(rows=5, cols=5, width = 550, height = 600)
   app.game = Game2048(rows=5, cols=5, width = 550, height = 600)
   app.info = InfoScreen(width = 550, height = 600)
   runAppWithScreens(initialScreen='season', width = 550, height = 600)

main()

#citations:
#for f1 tileTeams
# https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.si.com%2Ffannation%2Fracing%2Fauto-racing-digest%2Fformula-one%2Fformula-1-preseason-report-haas-f1&psig=AOvVaw0a8F0FNlGYr5HrLt_UNWwY&ust=1701546959019000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCODcvMOC74IDFQAAAAAdAAAAABAD
# https://www.google.com/imgres?imgurl=https%3A%2F%2Fs1.cdn.autoevolution.com%2Fimages%2Fnews%2Fforget-alfa-romeo-sauber-f1-team-heres-alfa-romeo-racing-132108_1.jpg&tbnid=KoN2rVjrpCmh7M&vet=12ahUKEwjP0IHPgu-CAxUXF1kFHX_WAaEQMygIegQIARBD..i&imgrefurl=https%3A%2F%2Fwww.autoevolution.com%2Fnews%2Fforget-alfa-romeo-sauber-f1-team-heres-alfa-romeo-racing-132108.html&docid=r5yi_p3FXUrM7M&w=862&h=862&q=alfa%20romeo%20f1%20logo&ved=2ahUKEwjP0IHPgu-CAxUXF1kFHX_WAaEQMygIegQIARBD
# https://www.google.com/url?sa=i&url=https%3A%2F%2Fscuderia.alphatauri.com%2Fen%2F&psig=AOvVaw3V63u947SaBF_sR4Hv7GdO&ust=1701547024528000&source=images&cd=vfe&ved=0CBIQjRxqFwoTCNjz4ueC74IDFQAAAAAdAAAAABAE
# https://www.google.com/imgres?imgurl=https%3A%2F%2Fcdn.williamsf1.tech%2Fimages%2Ffnx611yr%2Fproduction%2Fff454bb2b4adb541b66477adcb49088f8de0fb4a-2400x2400.jpg%3Frect%3D0%2C572%2C2400%2C1256%26w%3D1200%26h%3D628%26auto%3Dformat&tbnid=ulonelUPaeugxM&vet=12ahUKEwj3hsX6gu-CAxXJMVkFHVZOAvEQMygBegQIARBa..i&imgrefurl=https%3A%2F%2Fwww.williamsf1.com%2F&docid=dCP92rOkEhcpSM&w=1200&h=628&itg=1&q=williams%20racing%20logo&ved=2ahUKEwj3hsX6gu-CAxXJMVkFHVZOAvEQMygBegQIARBa
# https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Alpine_F1_Team_Logo.svg/2233px-Alpine_F1_Team_Logo.svg.png
# https://www.google.com/imgres?imgurl=https%3A%2F%2Fseeklogo.com%2Fimages%2FA%2Faston-martin-formula-one-race-logo-0D6CEA5C3B-seeklogo.com.png&tbnid=w57ZV0NGL0x3wM&vet=12ahUKEwjmlZSVg--CAxV-E1kFHSu_CeUQMygFegQIARA-..i&imgrefurl=https%3A%2F%2Fseeklogo.com%2Fvector-logo%2F412651%2Faston-martin-formula-one-race&docid=pBSs-WrSXHw_QM&w=300&h=300&q=aston%20martin%20f1%20logo&ved=2ahUKEwjmlZSVg--CAxV-E1kFHSu_CeUQMygFegQIARA-
# https://www.pinterest.com/pin/222928250297742566/
# https://banner2.cleanpng.com/20180831/jkq/kisspng-scuderia-ferrari-ferrari-s-p-a-car-5b88d55f0e4c93.8198830515356941750586.jpg
# https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRcOG7T4uyNqcqQiB1PChdK6ujOKVY3Oqjo78SpqKOYCw&s
# https://pbs.twimg.com/media/CX4HI1rW8AAc4dS.png








