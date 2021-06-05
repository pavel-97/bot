# TODO здесь писать код

list_number = []
bad_cells = []
count_cells = int(input('Введите кол-во клеток: '))

for i in range(1, count_cells + 1):
    efficiency = int(input('Введите эффективность клетки: '))
    list_number.append(efficiency)

for index in range(len(list_number)):
    print(f'Эффективность {index + 1} клетки: {list_number[index]}')

    if list_number[index] < (index + 1):
        bad_cells.append(list_number[index])

print('\nНеподходящие значения: ', end = '')

for bad_cell in bad_cells:
    print(bad_cell, end = ' ')
