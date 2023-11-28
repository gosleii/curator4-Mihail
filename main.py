import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State

state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6437247129:AAE8uf6c6pq2iPUrQQgKenBt9tkS-2I8U4Q",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()
    dog = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Знакомство"  # Можно менять текст
text_button_1 = "Уход за щенком"  # Можно менять текст
text_button_2 = "Список пород"  # Можно менять текст
text_button_3 = "Ещё"  # Можно менять текст

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Привет! Я бот который любит собак!',  # Можно менять текст
        reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Давай знакомится. \n *Как твоё* _имя_?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Сколько тебе лет?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.dog, message.chat.id)


@bot.message_handler(state=PollState.dog)
def dog(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['dog'] = message.text
    bot.send_message(message.chat.id, 'Какая у тебя парода?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)

@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Спасибо за знакомство! Круто что у тебя такая собака!!!', reply_markup=menu_keyboard)# Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Ты можешь узнать все по уходу за своим щенком тут: "
                                      "(https://kinpet.ru/ukhod-za-shchenkom-po-mesyatsam-/?utm_source=yandex-direct&utm_medium=cpc&utm_campaign=Article_55&utm_content=14091808830&utm_term=44632390242_87351856_5189286913&yclid=9346556646902726655)", reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Ты можешь попробовать найти свою любимую породу тут, (https://doge.ru/)", reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "*Вообще я люблю всех животных, но об этом в следующих версиях меня*", parse_mode='Markdown',reply_markup=menu_keyboard)  # Можно менять текст


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()