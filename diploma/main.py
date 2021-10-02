<<<<<<< HEAD

=======
>>>>>>> origin/hello_world
import telebot

bot = telebot.TeleBot('1922020612:AAF886Zt8N7bpsBQxqBVSjb0JL7bkgD4SfM')

<<<<<<< HEAD
for i in dir(telebot.types):
    print(i)

=======
>>>>>>> origin/hello_world

@bot.message_handler(content_types=['text'])
def get_text_message(message) -> None:
    if message.text in (r'/hello-world', 'Привет'):
        bot.send_message(message.from_user.id, 'Привет, {} {}'.format(
            message.from_user.first_name,
            message.from_user.last_name,
        ))


bot.polling(none_stop=True, interval=0)
