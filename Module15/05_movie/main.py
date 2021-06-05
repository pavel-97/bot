films = ['Крепкий орешек', 'Назад в будущее', 'Таксист',
         'Леон', 'Богемская рапсодия', 'Город грехов',
         'Мементо', 'Отступники', 'Деревня']

# TODO здесь писать код

list_favorite_films = []
count_films = int(input('Сколько ищете фильмов?: '))

for i in range(count_films):
    film = input('Введите название фильма: ')

    if film in films:
        list_favorite_films.append(film)

    else:
        print('Такого фильма нет в списке...')

print('\nСписок любимых фильмов: ', end = '')

for favorite_film in list_favorite_films:
    print(f'{favorite_film}', end = ', ')
