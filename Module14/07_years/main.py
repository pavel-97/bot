# TODO здесь писать код

def count_year(year):
    count, i = 0, year % 10

    while year > 0:
        if i == year % 10:
            count += 1
            i = year % 10

        year //= 10

    return count == 3

year1 = int(input('Введите первый год: '))
year2 = int(input('Введите второй год: '))

for year in range(year1, (year2 + 1)):
    if count_year(year):
        print(year)
