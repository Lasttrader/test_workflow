
#приветствие
def get_menu():
    print("Hello, let's playy X & Y")
    print('Нажмите 1 - для начала игры')
    print('Нажмите 0 - для выхода')
    key = input('Введжите значение: ')
    return key

#Функция проверки выйгрыша
def get_check(field):
    #проверям линии
    lines_check_list = []
    for i in field:
        if set(i) == set(['o']):
            print('Пользователь О выйиграл по горизонтали')
        if set(i) == set(['x']):
            print('Пользователь X выйиграл по горизонтали')               
    #Проверяем диагональ
    diag = [ field[i][i] for i in range(len(field))]
    inverse_diag = [ row[-i-1] for i,row in enumerate(field)]
    if set(diag) == set(['o']) or set(inverse_diag) == set(['o']):
            print('Пользователь О выйиграл по диагонали')
    if set(diag) == set(['x']) or set(inverse_diag) == set(['x']):
            print('Пользователь X выйиграл по диагонали')
    #проверяем столбцы
    for i in range(len(field)):
        column = [row[i] for row in field]
        if set(column) == set(['o']):
            print('Пользователь О выйиграл по горизонтали')
        if set(column) == set(['x']):
            print('Пользователь X выйиграл по горизонтали')

#Игра
def get_game():
    if int(get_menu()) == 1:
        print('Игра началась')
        indexes_list = ['0','1','2'] #номера столбцов
        field = [['_', '_', '_'] for i in range(3)] #поля
        print('_', indexes_list)
        for i in range(len(field)):
            print(i, field[i])
    print('введите координаты ячейки')
    game = ' '
    while game == ' ':
        x = int(input('Введите номер строки 0,1,2: '))
        y = int(input('Введите номер столбца 0,1,2: '))
        if x <= 2 and y <= 2:    
            field[x][y] = str(input('Введите (eng) X или О: ')).lower()
            if field[x][y] == 'x' or field[x][y] == 'o':
                print('_', indexes_list)
                for i in range(len(field)):
                    print(i, field[i])
                
                #проверка выйгрыша
                get_check(field)
            else: print('введите x или o')
        else:
            print('введите корректные значения')
        game = input('нажмите пробел и Enter для продолжения, или любую клавишу и Enter дял выхода')

#запускаем игру
get_game()

