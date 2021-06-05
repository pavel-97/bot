# TODO здесь писать код

def append_container(container, list_containers):

    if container <= 200:
        list_containers.append(container)

    else:
        print(f'Вес контейнера не должен превышать 200.')
        return append_container(container, list_containers)

    return list_containers


count_containers = int(input('Кол-во контейнеров: '))
list_containers = []

for _ in range(count_containers):
    container = int(input('Введите вес контейнера: '))
    append_container(container, list_containers)

new_container = int(input('Введите вес нового контейнера: '))

for index in range(len(list_containers)):
    if list_containers[index] < new_container:
        print(f'Номер, куда встанет новый контейнер: {index + 1}')
        break

    elif list_containers[index] == new_container:
        if index == (len(list_containers) - 1):
            print(f'Номер, куда встанет новый контейнер: {index + 2}')

        elif list_containers[index + 1] == new_container:
            continue

        else:
            print(f'Номер, куда встанет новый контейнер: {index + 2}')
            break

else:
    print(f'Номер, куда встанет новый контейнер: {index + 2}')
