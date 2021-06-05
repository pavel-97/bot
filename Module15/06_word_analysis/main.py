# TODO здесь писать код

word = input('Введите слово')
new_list_word, unique_list = [], []

for symbol in word:
    if symbol not in new_list_word:
        new_list_word.append(symbol)

for symbol in new_list_word:
    count = 0

    for symbol_word in word:
        if symbol == symbol_word:
            count += 1

        if count > 1:
            break

    if count == 1:
        unique_list.append(symbol)

print('Кол-во уникальных букв:', len(unique_list))
