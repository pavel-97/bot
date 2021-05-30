# TODO здесь писать код

def min_dividre(n):
    d = 2

    while n % d != 0:
        d += 1

    return d


number = int(input('Введите число: '))
print('Наименьший делитель, отличный от единицы:', min_dividre(number))
