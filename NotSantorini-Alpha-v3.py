class Tile:
    '''
    An ingame tile.
    '''
    def __init__(self, x, y, grid):
        '''
        Initializes an ingame tile.
        '''
        self.level = 0
        self.dome = False
        self.position = (x, y)
        self.grid = grid
        self.occupied = False
        self.occupier = None

    def build(self):
        '''
        Builds a new level on the tile. If the tile already has three
        levels, it builds a dome.
        '''
        if(self.level < 3):
            self.level += 1
            self.grid.tileUsed(self.level)
        elif(self.dome is False):
            self.dome = True
        else:
            raise Exception

    def getLevel(self):
        '''
        Returns the level of the building on the tile.
        '''
        return self.level

    def getOccupier(self):
        '''
        Returns which player is currently occupying the tile.
        '''
        return self.occupier

    def isDomed(self):
        '''
        Returns whether the building on the tile is domed.
        '''
        return self.dome

    def isOccupied(self):
        '''
        Returns whether the tile is occupied by a builder.
        '''
        return self.occupied

    def getX(self):
        '''
        Returns the x-coordinate of the tile.
        '''
        return self.position[0]

    def getY(self):
        '''
        Returns the y-coordinate of the tile.
        '''
        return self.position[1]

    def getGrid(self):
        '''
        Returns the grid on which the tile on.
        '''
        return self.grid

    def occupy(self, builder):
        '''
        Sets the tile to be occupied.
        '''
        self.occupied = True
        self.occupier = builder

    def unoccupy(self):
        '''
        Removes the tile being occupied.
        '''
        self.occupied = False
        self.occupier = None

class Grid:
    '''
    An ingame 5 by 5 grid of tiles.
    '''
    def __init__(self):
        '''
        Initiates the 5 by 5 grid of tiles.
        '''
        self.matrix = []
        for i in range(5):
            row = []
            for j in range(5):
                t = Tile(i + 1, j + 1, self)
                row.append(t)
            self.matrix.append(row)

        #self.levelUsed remembers how many pieces have already been "used" (of l1, l2, l3, and dome)
        self.levelUsed = [0, 0, 0, 0]

        self.levelCap = [16, 14, 12, 14]

    def __str__(self):
        '''
        Returns a seven string representation (with axes labels)
        of the grid of tiles. Tiles are indexed according to
        Cartesian Coordinates.
        '''
        buildLine = ""
        for j in range(5, -2, -1):
            if j is 5:
                buildLine += "  y  "
            else:
                for i in range(-1, 5):
                    if j is not -1 and i is -1:
                        buildLine += "  " + str(j + 1) + "  "
                    elif j is -1 and i is not -1:
                        buildLine += "  " + str(i + 1) + "  "
                    elif j is -1 and i is -1:
                        buildLine += "     "
                    else:
                        enclosingChar = "  "
                        if self.matrix[i][j].isOccupied():
                            occupant = self.matrix[i][j].getOccupier()
                            if occupant.player == 1:
                                if occupant.num == 1:
                                    enclosingChar = "()"
                                else:
                                    enclosingChar = "[]"
                            else:
                                if occupant.num == 1:
                                    enclosingChar = "{}"
                                else:
                                    enclosingChar = "<>"
                                    
                        buildLine += " " + enclosingChar[0] + ("D" if self.matrix[i][j].isDomed() else str(self.matrix[i][j].getLevel())) + enclosingChar[1] + " "
            if j is -1:
                buildLine += "  x  "
            else:
                buildLine += "\n"
        return buildLine

    def getTile(self, x, y):
        '''
        Returns the tile with specified x and y coordinates.
        '''
        return self.matrix[x - 1][y - 1]

    def getUsed(self):
        '''
        Return a list of the total number of used tile pieces
        in the game in the format:
        [L1, L2, L3, Dome]
        '''
        return self.levelUsed;

    def getCap(self):
        '''
        Return a list of the total number of tile pieces
        in the game in the format:
        [L1, L2, L3, Dome]
        '''
        return self.levelCap;

    def printRemainingTiles(self):
        '''
        Prints the number of remaining pieces of each
        tile piece type.
        '''
        buildStr = "Remaining Tiles: "
        for i in range(3):
            buildStr += "Level " + str(i + 1) + "-" + str(self.levelCap[i] - self.levelUsed[i]) + " "
        buildStr += "Dome-" + str(self.levelCap[3] - self.levelUsed[3])
        print(buildStr)

    def tileUsed(self, level):
        '''
        Uses one tile of a specific level from the
        unused tile pieces.
        '''
        self.levelUsed[level - 1] += 1
    
class Builder:
    '''
    Represents the builder who belongs to a player. Every builder is numbered,
    starting from 1, to differentiate them.
    '''
    def __init__(self, tile, player, num):
        '''
        Initializes an instance of a builder.
        '''
        self.player = player
        #num is how I differentiate between the two builders.
        self.num = num
        self.tile = tile
        self.tile.occupy(self)

    def canMoveTo(self, x, y):
        '''
        Checks whether this builder can move to the tile on the grid with
        specified x and y coordinates.
        '''
        #Things to check
        #First, make sure that it's actually adjacent and within bounds
        #Next, check whether the tile being moved to is occupied and/or is domed
        #Finally, check whether the height lets you move
        if(x > 0 and x <= 5) and (y > 0 and y <= 5):
            valid = True
        else:
            valid = False

        if(valid):
            if(self.tile.getX() > x + 1 or self.tile.getX() < x - 1):
                valid = False

            if(self.tile.getY() > y + 1 or self.tile.getY() < y - 1):
                valid = False

            if(self.tile.getX() == x and self.tile.getY() == y):
                valid = False

            if(valid):
                if self.tile.getGrid().getTile(x, y).isDomed() or self.tile.getGrid().getTile(x, y).isOccupied():
                    valid = False

                if(valid):
                    if self.tile.getGrid().getTile(x, y).getLevel() - self.tile.getLevel() > 1:
                        valid = False

        return valid

    def canBuildOn(self, x, y):
        '''
        Checks whether this builder can build on the tile on the grid with
        specified x and y coordinates.
        '''
        #Things to check
        #First, make sure that it's actually adjacent and within bounds
        #Next, check whether the tile being moved to is occupied and/or is domed
        #Lastly, check if we actually have a piece available
        if(x > 0 and x <= 5) and (y > 0 and y <= 5):
            valid = True
        else:
            valid = False

        if(valid):
            if(self.tile.getX() > x + 1 or self.tile.getX() < x - 1):
                valid = False

            if(self.tile.getY() > y + 1 and self.tile.getY() < y - 1):
                valid = False

            if(self.tile.getX() == x and self.tile.getY() == y):
                valid = False

            if(valid):
                target = self.tile.getGrid().getTile(x, y)
                if target.isDomed() or target.isOccupied():
                    valid = False

                if(valid):
                    #Note to future self. This part WILL BREAK when we add heroes so we'll revise it then
                    if self.tile.getGrid().getUsed()[target.getLevel()] == self.tile.getGrid().getCap()[target.getLevel()]:
                        valid = False

        return valid
    
    def move(self, x, y):
        '''
        Moves the builder to the tile on the grid with
        specified x and y coordinates.
        '''
        #I'm not making 8 different move functions
        if x <= 5 and x > 0 and y <=5 and y > 0 and self.canMoveTo(x, y):
            self.tile.unoccupy()
            self.tile = self.tile.getGrid().getTile(x, y)
            self.tile.occupy(self)
        else:
            raise Exception

    def getTile(self):
        '''
        Returns the grid tile that the builder is currently on.
        '''
        return self.tile

    def getPlayer(self):
        '''
        Returns the player number.
        '''
        #This property can be later edited to use names instead of numbers.
        #Nevertheless, this change would need to ensure that no two names
        #are the same.
        return self.player

class Player:
    '''
    Represents the player. Players are numbered to differentiate them.
    '''
    def __init__(self, grid, num, builderOne, builderTwo):
        '''
        Initializes the player instance.
        '''
        self.grid = grid
        self.num = num
        self.builder = [builderOne, builderTwo]

    def move(self):
        '''
        Prompts the player to move a builder. Returns a number indicating which
        builder was moved.
        '''
        validInput = False
        while validInput is False:
            try:
                    x, y = input("Where would you like to move to? ").strip().split()
                    x = int(x)
                    y = int(y)
                    if x <= 5 and x > 0 and y <=5 and y > 0:
                        if self.grid.getTile(x, y).isDomed():
                            print("That tile had been domed!")
                        else:
                            b1move = self.builder[0].canMoveTo(x, y)
                            b2move = self.builder[1].canMoveTo(x, y)
                            
                            if b1move == False and b2move == False:
                                print("Neither of your builders can reach that.")
                            else:
                                validInput = True    
                    else:
                        raise ValueError
            except ValueError:
                print("Please input only two integers from 1 and 5, separated with a space.")
                continue

        if b1move and b2move:
            inp = 0
            while (inp == 1) is False and (inp == 2) is False:
                try:
                    inp = int(input("Which builder would you like to move? (1 or 2) "))
                    if inp == 1 is False and inp == 2 is False:
                        raise ValueError
                except ValueError:
                    print("Please type only 1 or 2")
                    
            if inp == 1:
                self.builder[0].move(x, y)
                return 1
            elif inp == 2:
                self.builder[1].move(x, y)
                return 2
            else:
                raise ValueError
        elif b1move:
            self.builder[0].move(x, y)
            return 1
        else:
            self.builder[1].move(x, y)
            return 2

    def build(self, builderNum):
        '''
        Prompts the player to have a builder build on a tile.
        '''
        validInput = False
        while validInput is False:
            try:
                    x, y = input("Where would you like to build? (x y) ").strip().split()
                    x = int(x)
                    y = int(y)
                    if x <= 5 and x > 0 and y <=5 and y > 0:
                        if self.grid.getTile(x, y).isDomed():
                            print("That tile had been domed!")
                        else:
                            if builderNum == 1:
                                bmove = self.builder[0].canBuildOn(x, y)
                            else:
                                bmove = self.builder[1].canBuildOn(x, y)

                            if bmove:
                                validInput = True    
                            else:
                                print("Your builder can't do that.")
                    else:
                        raise ValueError
            except ValueError:
                print("Please input only two integers from 1 and 5, separated with a space.")
                continue

        self.grid.getTile(x, y).build()

    def checkWin(self):
        '''
        Checks if the player won.
        '''
        #Needless to say, change the code when we add heroes.
        return self.builder[0].getTile().getLevel() == 3 or self.builder[1].getTile().getLevel() == 3

    def checkLose(self):
        '''
        Checks if the player lost.
        '''
        canMove = False
        x = []
        y = []
        for i in self.builder:
            x.append(i.getTile().getX())
            y.append(i.getTile().getY())
            
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                for k in range(len(self.builder)):
                    canMove = canMove or self.builder[k].canMoveTo(x[k] + i, y[k] + j)
                if canMove is True:
                    break
            if canMove is True:
                break
        return (canMove is False)
    
class GI:  
    '''
    An instance of the game.
    '''          
    def __init__(self):
        #INSTRUCTIONS. Edit the text accordingly so that the player doesn't get confused.
        print("Welcome!" + "\n"
            "Player one controls builder 1 () and builder 2 []" + "\n"
            "Player two controls builder 1 {} and builder 2 <>" + "\n"
            "The game will now start" )

        #Initialization of builder positions
        builderList = []
        xyList = []
        initBuilders = True
        
        #Game Proper
        runGame = True
        while(runGame):
            #Do we need to initialize?
            if initBuilders:
                self.grid = Grid()
                builderList = []
                xyList = []
                for i in range(4):
                    validInput = False
                    while(validInput is False):                
                        try:
                            x, y = input("Player " + (str)(i//2 + 1) + ": Where would you like to place your " + ("first" if i % 2 == 0 else "second") + " builder? (x y): ").strip().split()
                            x = int(x)
                            y = int(y)
                        except ValueError:
                            print("Please input only two integers from 1 and 5, separated with a space.")
                            continue
                        
                        distinct = True
                        for j in xyList:
                            if j[0] == x and j[1] == y:
                                distinct = False
                                break
                        if distinct is False:
                            print("Please input coordinates different from those of previous builders.")
                        elif x <= 5 and x > 0 and y <=5 and y > 0:
                            validInput = True
                        else:
                            print("Please input an integer from 1 to 5 for both coordinates.")
                    xyList.append((x, y))
                    builderList.append(Builder(self.grid.getTile(x, y), i//2 + 1, (i % 2) + 1))
                self.playerOne = Player(self.grid, 1, builderList[0], builderList[1])
                self.playerTwo = Player(self.grid, 2, builderList[2], builderList[3])
                initBuilders = False

            #Game Proper            
            turnResult = self.turn()
            if turnResult:
                validInput = False
                while validInput is False:
                    try:
                        playAgain = input("Do you want to play again? (Y/N)")
                        if playAgain == "Y":
                            validInput = True
                            initBuilders = True
                        elif playAgain == "N":
                            validInput = True
                            runGame = False
                            print("Thank you for playing!")
                        else:
                            raise ValueError
                    except ValueError:
                        print("Please input only the character \"Y\" or \"N\"")

    def turn(self):
        '''
        Executes an ingame turn by both players. Returns True if a player has won,
        and False otherwise.
        '''
        if(self.playerOne.checkLose()):
            print("Player one can't move.")
            print("A winner is player two!")
            return True
        else:
            print("PLAYER ONE (Move Phase): Builders (1) [2] ")
            print(str(self.grid))
            self.grid.printRemainingTiles()
            outp = self.playerOne.move()
            if(self.playerOne.checkWin()):
                print("A winner is player one!")
                return True
            else:
                print("PLAYER ONE (Build Phase): Builders (1) [2] ")
                print(str(self.grid))
                self.grid.printRemainingTiles()
                self.playerOne.build(outp)

                if(self.playerTwo.checkLose()):
                    print("Player two can't move.")
                    print("A winner is player one!")
                    return True
                else:                    
                    print("PLAYER TWO (Move Phase): Builders {1} <2>")
                    print(str(self.grid))
                    self.grid.printRemainingTiles()
                    outp = self.playerTwo.move()
                    if(self.playerTwo.checkWin()):
                        print("A winner is player two!")
                        return True
                    else:
                        print("PLAYER TWO (Build Phase): Builders {1} <2>")
                        print(str(self.grid))
                        self.grid.printRemainingTiles()
                        self.playerTwo.build(outp)
                        return False
'''
Automatically runs the program.
'''
GI()
