# TODO здесь писать код

list_numbers = [1, 2, 3, 4, 5]
new_list = list(list_numbers)
shift = int(input('Сдвиг: '))

for index in range(len(list_numbers) - shift):
    new_list[index + shift] = list_numbers[index]

new_index = 0
for index in range(shift, 0, -1):
    new_list[new_index] = list_numbers[-index]
    new_index += 1

print(list_numbers)
print(new_list)
