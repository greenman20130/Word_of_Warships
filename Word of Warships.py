import random
import time

class Dot:
    type = 'dot'
    empty_dot = "O"
    ship_dot = "■" 
    destroyed_ship_dot = "X" 
    missed_dot = "M"
    contour_dot = "*" 
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Board:
    def __init__(self, board=None, ships=None, hid=False, live_ships=0):
        if ships is None:
            ships = []
        if board is None:
            board = [[Dot.empty_dot] * 6 for _ in range(6)]
        self.board = board
        self.ships = ships
        self.ship_contours = []
        self.live_ships = live_ships
        self.unique_ships = []
        self.shot_points = []
        self.hid = hid
    
    def print_board(self):
        if not self.hid:
            for i in range(7):
                if i == 0:
                    i = " "
                print(i, end=" | ")
            print()
            for i in range(6):
                for j in range(6):
                    if j == 0:
                        print(i + 1, "|", self.board[i][j], end=" | ")
                    else:
                        print(self.board[i][j], end=" | ")
                print()
                
        else:
            print(f"\n{self.live_ships} работоспособных кораблей\n")
    
    def add_ship(self, ship_dots, ship_contour, hid, ship):
        try:
            for i in ship_dots:
                if i in self.ships or i in self.ship_contours or i.x < 0 or i.x > 5 or i.y < 0 or i.y > 5:
                    raise IndexError
            self.ships = self.ships + ship_dots  
            self.unique_ships = self.unique_ships + [ship]
            if hid is False:
                for i in ship_dots:
                    self.board[i.x][i.y] = i.ship_dot
            for i in ship_contour:
                self.ship_contours = self.ship_contours + [i]
            self.live_ships = self.live_ships + 1
            return self.board, self.ships, self.ship_contours, self.live_ships
        
        except IndexError:
            if hid is False:
                print("Клетки заняты либо ввдены не правильно")
    
    def shot(self, shot_point, hid=False):
        try:
            if shot_point in self.shot_points or shot_point.x < 0 or shot_point.x > 6 or shot_point.y < 0 or shot_point.y > 6:
                raise IndexError
            self.shot_points = self.shot_points + [shot_point]
            if shot_point in self.ships:
                self.board[shot_point.x][shot_point.y] = shot_point.destroyed_ship_dot
                unique_ship_counter = -1
                for i in self.unique_ships:
                    unique_ship_counter = unique_ship_counter + 1
                    for j in i.ship_dots:
                        if shot_point == j:
                            self.unique_ships[unique_ship_counter].hp = self.unique_ships[unique_ship_counter].hp - 1
                            if i.hp == 0:
                                self.live_ships = self.live_ships - 1
                                for k in i.ship_contour:
                                    self.board[k.x][k.y] = k.contour_dot
                                if hid is False:
                                    print("Корабль уничтожен")
                                    break
                            elif hid is False:
                                print("Есть пробитие")
                                break
            else:
                print("Мимо")
                self.board[shot_point.x][shot_point.y] = shot_point.missed_dot
            return self.board

        except IndexError:
            if hid is False:
                print("Точка выстрела не верная либо повторная")

class Ship:
    def __init__(self, size, x, y, direction=0, ship_dots=None):
            self.size = size
            if ship_dots is None:
                ship_dots = []
            self.direction = direction
            self.x = x
            self.y = y
            self.hp = size
            self.ship_dots = ship_dots
            self.ship_contour = []
            
    def dots(self): 
        self.ship_dots = []  
        if self.direction == "H":
            for i in range(self.size):
                self.ship_dots = self.ship_dots + [Dot(self.x - 1, self.y + i - 1)]
        else:  
            for i in range(self.size):
                self.ship_dots = self.ship_dots + [Dot(self.x + i - 1, self.y - 1)]
        return self.ship_dots
        
            
    def contour(self, ship_dots):  
        for i in ship_dots:  
            for a in range((i.x - 1), (i.x + 2)):
                for b in range(i.y - 1, i.y + 2):
                    if Dot(a, b) not in self.ship_contour and Dot(a, b) not in ship_dots and 0 <= a < 6 and 0 <= b < 6:
                        self.ship_contour = self.ship_contour + [Dot(a, b)]  
        return self.ship_contour

class Player:
    def __init__(self, player, my_board, enemy_board, shot_point=None, hid=True):
        self.player = player
        self.my_board = my_board
        self.enemy_board = enemy_board
        self.shot_point = shot_point
        self.hid = hid
        
    def move(self, hid=False):
        self.enemy_board.shot(self.shot_point, self.hid)
        if hid is False:
            print("Ваше поле:", "\n")
        else:
            print("Поле противника:", "\n")
        self.enemy_board.print_board()
        if self.enemy_board.live_ships == 0:
            print(f"\nПобедил игрок {self.player}")
            
    def ask(self):
        return self.shot_point


class User(Player):
    def __init__(self, my_board, enemy_board, player='"Вы"', hid=False):
        super().__init__(player, my_board, enemy_board, shot_point=None, hid=True)
        self.player = player
        self.hid = hid
    
    def ask(self): 
        try:
            x = int(input("Введите точку выстрела X:")) - 1
            y = int(input("Введите точку выстрела Y:")) - 1
            self.shot_point = Dot(x, y)
            return self.shot_point
        except ValueError:
            print("Точка введена неверно")
            pl = User(my_board=g.player_board, enemy_board=g.ai_board)
            pl.ask()

class AI(Player): 
    def __init__(self, my_board, enemy_board, player='"ПК"', hid=True):
        super().__init__(player, my_board, enemy_board, shot_point=None, hid=True)
        self.player = player
        self.hid = hid
        
    def ask(self):
        self.shot_point = Dot(random.randint(0, 5), random.randint(0, 5))
        return self.shot_point

class Game:
    def __init__(self, player=None, ai=None):
        self.player = player
        self.player_board = Board()
        self.ai = ai
        self.ai_board = Board()
        self.ships_sizes = (3, 2, 2, 1, 1, 1, 1)
        self.ship_names = ('3х клеточный', "2х клеточный", "Второй 2х клеточный",
                           "одноклеточный", "Второй одноклеточный", "Третий одноклеточный", "Четвертый одноклеточный")
        
    def gen_player_board(self):
        self.player_board.print_board()
        print()
        ship_count = 0 
        ship_name_count = -1  
        for ship_size in self.ships_sizes:
            ship_count = ship_count + 1  
            ship_name_count = ship_name_count + 1  
            while True:
                try:
                    print(f"Ставим {self.ship_names[ship_name_count]} корабль")
                    ship = Ship(ship_size, int(input("Введите точку X:")), int(input("Введите точку Y:")), (input("""Введите H для горизонтального размещения
Или просто нажмите Enter для вертикального размещения:""") if ship_size > 1 else "H"))
                    self.player_board.add_ship(ship.dots(), ship.contour(ship.dots()), False, ship)
                    if self.player_board.live_ships == ship_count:
                        self.player_board.print_board()
                        break
                except ValueError:
                    print("Клетки заняты либо ввдены не правильно")
        return self.player_board
    
    def gen_ai_board(self):  
        attempt_count = 0
        while self.ai_board.live_ships != 7:
            ship_count = 0
            for ship_size in self.ships_sizes:
                ship_count = ship_count + 1
                if attempt_count > 100:
                    attempt_count = 0
                    break
                while True:
                    ship = Ship(ship_size, random.randint(1, 6), random.randint(1, 6), random.randint(0, 1))
                    self.ai_board.add_ship(ship.dots(), ship.contour(ship.dots()), True, ship)
                    attempt_count = attempt_count + 1
                    if attempt_count > 100:
                        self.ai_board = Board()
                        break
                    if self.ai_board.live_ships == ship_count:
                        attempt_count = 0
                        break
        #self.ai_board.print_board()
        return self.ai_board

    def gameplay(self):
        pl = User(my_board=g.player_board, enemy_board=g.ai_board)
        ai = AI(my_board=g.ai_board, enemy_board=g.player_board)
        move_count = 1
        while True:
            print("Ход ", move_count, "\n")
            move_count = move_count + 1
            pl.ask()
            pl.move(hid=True)
            time.sleep(5)
            ai.ask()
            ai.move(hid=False)
            time.sleep(5)
            if pl.enemy_board.live_ships == 0 or ai.enemy_board.live_ships == 0:
                break
    
    def greet(self):
        print(f"""Приветствую тебя в игре морской бой!
Правила очень просты
Тебе нужно спрятать свои корабли от ПК и попытаться найти его корабли
Главное слушаться подсказок, удачи
""")
        
g = Game()
g.greet()
g.gen_player_board()
g.gen_ai_board()
g.gameplay()