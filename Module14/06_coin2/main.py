# TODO здесь писать код

def in_circle(x, y, r):

    if (x ** 2 + y ** 2) <= r ** 2:
        return 'Монетка где-то рядом'

    else:
        return 'Монетки в области нет'


print('Введите координаты монетка:')
x1, y1 = float(input('X: ')), float(input('Y: '))
r1 = float(input('Введите радиус: '))
print(f'\n{in_circle(x1, y1, r1)}')
