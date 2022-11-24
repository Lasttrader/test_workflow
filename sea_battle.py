from random import randint

###################
# 1 Создаем класс точки
###################
class Dot:
    def __init__(self, x, y):
        '''
        координаты точки
        '''
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        '''
        проверка равенства этой точки с другим точкам
        '''
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        '''
        возвращаем точку ввиде строки
        '''
        return f"Dot({self.x},{self.y})"

###################
# 2 опишем исключения
###################
class BoardException(Exception):
    pass
class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"
class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"
class BoardWrongShipException(BoardException):
    pass

###################
# 3 создаём класс корабля
###################
class Ship:
    def __init__(self, bow, l, o):
        '''
        парамеры корабля
        '''
        self.bow= bow #нос
        self.l =l #длина
        self.o = o #ориентация
        self.lives = l 

    @property # дкоратор свойств корабля 
    def dots(self):
        '''
        список точек корабля
        '''
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x 
            cur_y = self.bow.y        
            if self.o == 0: #если оринетация горизонтальная
                cur_x += i      
            elif self.o == 1: #если ориентация вертикальная
                cur_y += i
            #добавляем координаты с учетом ориентации корабля
            ship_dots.append(Dot(cur_x, cur_y))   
        return ship_dots #возвращаем координаты корабля

    def shooten(self, shot):
        '''
        првоеряем попал ли выстрел в тело корабля
        '''
        return shot in self.dots

###################
# 4 создаем класс игровое поле - доска
###################
class Board:
    def __init__(self, hid = False, size = 6):
        '''
        параметры доски
        '''
        self.size = size #размер поля
        self.hid = hid #нужно ли оле скрывать hidden
        self.count = 0 #кол-во пораженных кораблей
        self.field = [ ["O"]*size for _ in range(size) ] #сетка size X size
        self.busy = [] #занятые точки или точки куда стреляли
        self.ships = [] #корабли на доске

    def __str__(self):
        '''
        проходимся в целке по строкам доски
        и рисуем доску
        '''
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i+1} | " + " | ".join(row) + " |"
        
        if self.hid: #если скрытый
            res = res.replace("■", "O")
        return res
    
    def out(self, d):
        '''
        проверка точки за пределами доски
        '''
        return not((0<= d.x < self.size) and (0<= d.y < self.size))

    def contour(self, ship, verb = False):
        '''
        все точки вокруг точки в которой мы находимся
        поимаем, куда нельзя ставить корабли
        '''
        near = [
            (-1, -1), (-1, 0) , (-1, 1),
            (0, -1), (0, 0) , (0 , 1),
            (1, -1), (1, 0) , (1, 1)
        ] #все сдвиги

        for d in ship.dots: #все точки корабля
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur) #показываем что точка занята
    
    def add_ship(self, ship):
        '''
        метод доабвления корабля
        '''
        for d in ship.dots:
            if self.out(d) or d in self.busy: #проверяем занятость клетки
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)
        self.ships.append(ship) #добавляем в список корабль
        self.contour(ship)
            
    def shot(self, d):
        '''
        Стреляем по доске
        '''
        if self.out(d):
            raise BoardOutException()
        if d in self.busy:
            raise BoardUsedException()
        self.busy.append(d)
        
        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb = True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True
        
        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []

###################
# 5 создаем класс игрока
###################
class Player:
    def __init__(self, board, enemy):
        '''
        две доски одна противника, одна игрока
        '''
        self.board = board
        self.enemy = enemy

    def ask(self):
        '''
        этот метод должен быть у потокмков этого класса
        '''
        raise NotImplementedError()

    def move(self):
        '''
        в бесконечном цикле просим сделать выстрел
        '''
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

    def begin(self):
        self.busy = []

###################
# 6 создаем класс игрока ИИ
###################
class AI(Player):

    def ask(self):
        '''
        формируем код компьютера
        '''
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x+1} {d.y+1}")
        return d


###################
# 7 создаем класс пользователь
###################
class User(Player):
    def ask(self):
        '''
        запрос координат проверка, что координаты числовые
        '''
        while True:
            cords = input("Ваш ход: ").split()
            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue    
            x, y = cords
            if not(x.isdigit()) or not(y.isdigit()):
                print(" Введите числа! ")
                continue
            x, y = int(x), int(y)  
            return Dot(x-1, y-1)

###################
# 8 создаем класс игры
###################
class Game:
    def __init__(self, size = 6):
        self.size = size
        pl = self.random_board() #доска для игрока
        co = self.random_board() #доска для компьютера
        co.hid = True 
        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        '''
        создаем рандомную доску
        '''
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        '''
        создаем поле боя и размещаем карабли
        '''
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size = self.size)
        attempts = 0
        for l in lens:
            #расстановка кораблей в бесконечном цикле
            while True:
                attempts += 1
                if attempts > 2000: #макисмальное кол-во попыток
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0,1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")
    
    
    def loop(self):
        num = 0
        while True:
            print("-"*20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-"*20)
            print("Доска компьютера:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-"*20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-"*20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1
            
            if self.ai.board.count == 7:
                print("-"*20)
                print("Пользователь выиграл!")
                break
            
            if self.us.board.count == 7:
                print("-"*20)
                print("Компьютер выиграл!")
                break
            num += 1
            
    def start(self):
        self.greet()
        self.loop()

game = Game()
game.start()