import pickle
from random import randrange
from typing import Optional

class Game: pass
class GameState:
    def setup(self): pass
    def execute(self): pass

class InclusionBlock:
    '''
    Хранит количество вклучений чисел от 0 до size
    '''
    
    def __init__(self, size: int) -> None:
        self.__size = size
        self.reset()

    def reset(self) -> None:
        self.__inclusionList = [0 for i in range(self.__size + 1)]

    def __isGoodNum(self, num: int) -> bool:
        return num >= 0 and num <= self.__size

    def inclusionCount(self, num: int) -> None:
        if (self.__isGoodNum(num)):
            return self.__inclusionList[num]
        else:
            raise ValueError

    def include(self, num: int) -> None:
        if (self.__isGoodNum(num)):
            self.__inclusionList[num] += 1
        else:
            raise ValueError

    def exclude(self, num: int) -> bool:
        if (self.__isGoodNum(num)):
            if (self.__inclusionList[num] > 0):
                self.__inclusionList[num] -= 1
                return True
            return False

        raise ValueError
        

    @property
    def size(self) -> int:
        return self.__size
    
class Game:
    __currentState: GameState

    def __init__(self) -> None:
        self.rebuildField(0, 0)
        self.__currentState = GameState(Game)

    def execute(self) -> None:
        self.currentState.execute()

    def drawField(self) -> None:
        h, w = self.fieldSize
        field: list[list[str]] = [[' ' for j in range(2 * w + 1)] for i in range(2 * h + 1)]

        field[0][0] = '┏'
        field[0][2 * w] = '┓'
        field[2 * h][0] = '┗'
        field[2 * h][2 * w] = '┛'

        for i in range(1, 2 * w):
            field[0][i] = '━'
            field[2 * h][i] = '━'
        
        for i in range(1, 2 * h):
            field[i][0] = '┃'
            field[i][2 * w] = '┃'

        for i in range(1, 2 * h):
            for j in range(1, 2 * w):
                field[i][j] = self.boundList[i - 1][j - 1]

        for i in range(h):
            for j in range(w):
                if (self.valueList[i][j] == None):
                    field[2 * i + 1][2 * j + 1] = ' '
                else:
                    field[2 * i + 1][2 * j + 1] = self.valueList[i][j]

        for row in field:
            for cl in row:
                print(cl, end = '')
            print()

    def rebuildField(self, newHeight: int, newWidth: int):
        self.__fieldHeight = newHeight
        self.__fieldWidth = newWidth
        self.boundList = [[' ' for j in range(2 * newWidth + 1)] for i in range(2 * newHeight + 1)]
        self.clearValueList()

    @property
    def fieldHeight(self) -> int:
        return self.__fieldHeight

    '''
    @fieldHeight.setter
    def fieldHeight(self, h: int) -> None:
        if (h >= 0):
            self.__fieldHeight = h
        else:
            raise ValueError
    '''

    @property
    def fieldWidth(self) -> int:
        return self.__fieldWidth

    '''
    @fieldWidth.setter
    def fieldWidth(self, w: int) -> None:
        if (w >= 0):
            self.__fieldWidth = w
        else:
            raise ValueError
    '''

    @property
    def currentState(self) -> GameState:
        return self.__currentState

    @currentState.setter
    def currentState(self, state) -> None:
        if (state == None):
            raise ValueError('currentState can\'t be None')
        self.__currentState = state

    @property
    def fieldSize(self) -> tuple[int]:
        '''
        returns (fieldHeight, fieldWidth)
        '''
        return (self.__fieldHeight, self.__fieldWidth)

    @property
    def valueList(self) -> list[list[int]]:
        return self.__valueList

    @valueList.setter
    def valueList(self, list: list[list[int]]) -> None:
        self.__valueList = list

    def clearValueList(self) -> None:
        self.valueList = [[None for j in range(self.fieldWidth)] for i in range(self.fieldHeight)]

    @property
    def boundList(self) -> list[str]:
        '''
        returns (2 * height - 1)x(2 * width - 1) str list
        '''
        return self.__boundList
    
    @boundList.setter
    def boundList(self, list: list[str]) -> None:
        def copy(list, i, j):
            if (i < len(list) and j < len(list[i])):
                return list[i][j]
            return ' '
                
        self.__boundList = [[copy(list, i, j) for j in range(2 * self.fieldWidth - 1)] for i in range(2 * self.fieldHeight - 1)]

class GameState:
    def __init__(self, game: Game) -> None:
        self.__game = game

    def setup(self, game: Game) -> None:
        pass

    def execute(self) -> None:
        raise NotImplementedError

    @property
    def game(self) -> Game:
        return self.__game

    @game.setter
    def game(self, newGame) -> None:
        self.__game = newGame

class ClassicGameplayState(GameState):
    __blockList = [] #: list[ tuple[ InclusionBlock, function[int, int] ] ]
    __startCount: int
    __addedList: list[ tuple[int, int, int] ]

    def __init__(self, game: Game, startCount: int = 0) -> None:
        super().__init__(game)
        self.__blockList = []
        self.startCount = startCount
        self.__addedList = []

        for k in range(9):
            b: int = k // 3
            r: int = k % 3
            self.__blockList.append((InclusionBlock(9),
                                    lambda i, j, b = b, r = r: 3 * b <= i and i < 3 * (b + 1) and 3 * r <= j and j < 3 * (r + 1)))
            self.__blockList.append((InclusionBlock(9), lambda i, j, k = k: i == k))
            self.__blockList.append((InclusionBlock(9), lambda i, j, k = k: j == k))

        self.setup()

    def setup(self) -> None:
        self.game.rebuildField(9, 9)
        hor1 = '─┼─┼─╂─┼─┼─╂─┼─┼─'
        hor2 = '━┿━┿━╋━┿━┿━╋━┿━┿━'
        ver = ' │ │ ┃ │ │ ┃ │ │ '
        self.game.boundList = [ver[:], hor1[:], ver[:], hor1[:], ver[:], hor2[:],
            ver[:], hor1[:], ver[:], hor1[:], ver[:],
            hor2[:], ver[:], hor1[:], ver[:], hor1[:], ver[:]]
        self.game.clearValueList()
        
        for block, rule in self.__blockList:
            block.reset()
        
        self.generate()

        print('Commands:')
        print('exit: quite the session')
        print('save: save session')
        print('(row: int) (collumn: int) (number: int): add number')

    def execute(self) -> None:
        self.game.drawField()

        if (len(self.__addedList) == 81):
            print('You solved Sudoku! Well done!')
            menu: MenuState = MenuState(self.game)
            self.game.currentState = menu
            return
        
        t = input('Enter query: ').split(' ')

        if (t[0] == 'save'):
            name: str = input('Session name (one word): ')
            try:
                self.saveSession(name + '.pkl')
                print('Game was saved!')
            except Exception as e:
                print('Game wasn\'t saved! Do not use name of another saved game!')
            return

        if (t[0] == 'exit'):
            conf: str = input("Game would not be saved! You sure? (Y/N): ")
            if (conf == 'Y'):
                menu: MenuState = MenuState(self.game)
                self.game.currentState = menu
            return

        i: int = int(t[0])
        j: int = int(t[1])
        x: int = int(t[2])
        
        if (not(self.__goodInput(i, j, x))):
            print("Wrong input...")
            return

        if (not(self.isAddableNumber(i, j, x))):
            print('You can\'t put this number there. Try again')
            return

        self.addNumber(i, j, x)
        self.game.valueList[i][j] = x

    def saveSession(self, fileName: str) -> None:
        file = open(fileName, 'xb')
        print(self.__addedList)
        pickle.dump(self.__addedList, file)
    
    def loadSession(self, fileName: str) -> None:
        file = open(fileName, 'rb')
        savedList = pickle.load(file)

        self.setup()
        for i, j, x in savedList:
            self.addNumber(i, j, x)
            self.game.valueList[i][j] = x
        
        self.__addedList = savedList

    def generate(self):
        field: list[list[Optional[int]]] = [[] for i in range(9)]
        fl: list[int] = [1, 2, 3]
        sl: list[int] = [4, 5, 6]
        tl: list[int] = [7, 8, 9]

        for i in range(3):
            for j in range(3):
                field[i * 3 + j].extend(fl)
                field[i * 3 + j].extend(sl)
                field[i * 3 + j].extend(tl)
                fl, sl, tl = sl, tl, fl

            fl.append(fl[0])
            fl.pop(0)
            sl.append(sl[0])
            sl.pop(0)
            tl.append(tl[0])
            tl.pop(0)
        
        for k in range(randrange(10)):
            q: int =  randrange(2)

            if (q == 0):
                b: int = randrange(3)
                field[3 * b], field[3 * ((b + 1) % 3)] = field[3 * ((b + 1) % 3)], field[3 * b]
                field[3 * b + 1], field[3 * ((b + 1) % 3) + 1] = field[3 * ((b + 1) % 3) + 1], field[3 * b + 1]
                field[3 * b + 2], field[3 * ((b + 1) % 3) + 2] = field[3 * ((b + 1) % 3) + 2], field[3 * b + 2]
            else:
                b: int = randrange(3)
                c: int = randrange(3)
                for i in range(9):
                    field[i][3 * b + c], field[i][3 * b + (c + 1) % 3] = field[i][3 * b + (c + 1) % 3], field[i][3 * b + c]
        
        cnt: int = 81
        while cnt > self.startCount:
            i: int = randrange(9)
            j: int = randrange(9)

            if (field[i][j] == None):
                continue

            field[i][j] = None
            cnt -= 1

        for i in range(9):
            for j in range(9):
                if (not(field[i][j] == None)):
                    self.addNumber(i, j, field[i][j])

        self.game.valueList = field
    

    def addNumber(self, i: int, j: int, x: int) -> None:
        for block, rule in self.__blockList:
            if (not(rule(i, j))):
                continue

            block.include(x)
        self.__addedList.append((i, j, x))

    def isAddableNumber(self, i: int, j: int, x: int) -> bool:
        for block, rule in self.__blockList:
            if (not(rule(i, j))):
                continue
            
            if (block.inclusionCount(x) > 0):
                return False

        return True

    def __goodInput(self, i: int, j: int, x: int) -> bool:
        return 1 <= x and x <= 9 and 0 <= i and i <= 8 and 0 <= j and j <= 8

    @property
    def startCount(self) -> int:
        return self.__startCount
    
    @startCount.setter
    def startCount(self, c) -> None:
        if (c >= 0):
            self.__startCount = c
        else:
            raise ValueError('startCount need to be >= 0')

class MenuState(GameState):
    def execute(self):
        print('Choose one and enter number:')
        print('1. Classic')
        print('2. Load session')

        query: int = int(input())

        if (query == 1):
            startCount: int = int(input('Count of filled cells: '))
            gameplay = ClassicGameplayState(self.game, startCount)
            self.game.currentState = gameplay
        elif(query == 2):
            saveName: str = input('Session name (one word): ')
            try:
                gameplay = ClassicGameplayState(self.game, 0)
                gameplay.loadSession(saveName + '.pkl')
                print('Session was loaded!')
                self.game.currentState = gameplay
            except Exception as e:
                print('Session wasn\'t loaded! Maybe this session does not exist?')
        else:
            print('Wrong input. Try again...')

game = Game()
menu = MenuState(game)
game.currentState = menu

while (True):
    game.execute()
