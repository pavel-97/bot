# TODO здесь писать код

list_numbers = [1, 4, -3, 0, 10]

print('Изначальный список: ', list_numbers)

for index in range(len(list_numbers)):
    for index_replace in range(index + 1, len(list_numbers)):

        if list_numbers[index] > list_numbers[index_replace]:
            list_numbers[index], list_numbers[index_replace] = list_numbers[index_replace], list_numbers[index]

print('Отсортированный список: ', list_numbers)
