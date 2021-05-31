# TODO здесь писать код

def count_year(year):
    count, i = 0, year % 10

    while year > 0:
        if i == year % 10:
            count += 1
            i = year % 10

        year //= 10

    if count == 3:  # TODO А сейчас код читается так "если сравние True, то верни True, а вот если False, то верни
                    #  False" немного избыточно, не находите? Раз результат сравнения и есть булево значние, поэтому
                    #  вместо этих 4х строк достаточно просто указать сравнение в return.
        return True

    else:
        return False


year1 = int(input('Введите первый год: '))
year2 = int(input('Введите второй год: '))

for year in range(year1, (year2 + 1)):
    if count_year(year):
        print(year)
