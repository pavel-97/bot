# TODO здесь писать код


def reverce(n):
    reverce_n = ''
    for symbol in n:
        reverce_n = symbol + reverce_n
    return reverce_n


def get_value_befor_point(n):
    part = ''
    for symbol in n:
        if symbol == '.':
            break

        else:
            part += symbol

    return part


N = input('Введите первое число: ')
K = input('Введите второе число: ')

int_part_n, float_part_n = get_value_befor_point(N), get_value_befor_point(reverce(N))
int_part_k, float_part_k = get_value_befor_point(K), get_value_befor_point(reverce(K))

new_n = float(f'{reverce(int_part_n)}.{float_part_n}')
new_k = float(f'{reverce(int_part_k)}.{float_part_k}')

print('Первое число наоборот:', new_n)
print('Второе число наоборот:', new_k)
print('Сумма:', new_n + new_k)
