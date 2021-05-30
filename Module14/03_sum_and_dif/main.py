# TODO здесь писать код

def summ(n):
    summ_n = 0
    while n != 0:
        summ_n += n % 10
        n //= 10
    return summ_n


def count(n):
    count_n = 0
    while n != 0:
        n //= 10
        count_n += 1
    return count_n


n = int(input('Введите число:'))
print('Сумма цифр:', summ(n))
print('Кол-во цифр в числе:', count(n))
print('Разность суммы и кол-ва цифр:', summ(n) - count(n))
