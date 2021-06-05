# TODO здесь писать код

list_video_cards = []
new_list_video_cards = []
count_video_cards = int(input('Введите кол-во видеокрт: '))

for i in range(count_video_cards):
    video_card = int(input(f'{i + 1} Видеокарта: '))
    list_video_cards.append(video_card)

old_video_card = list_video_cards[0]

for video_card in list_video_cards:
    if video_card > old_video_card:
        old_video_card = video_card

for new_video_card in list_video_cards:
    if new_video_card < old_video_card:
        new_list_video_cards.append(new_video_card)

print(f'Страый список видеокард: {list_video_cards}')
print(f'Новый список видеокард: {new_list_video_cards}')
