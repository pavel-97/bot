# TODO здесь писать код
word = input('Введите слово: ')
reverce_word = ''

for symbol in word:
    reverce_word = symbol + reverce_word

if word == reverce_word:
    print('Слово является полиндромом')

else:
    print('Слово не является полиндромом')
