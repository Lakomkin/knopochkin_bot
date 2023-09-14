
from turtle import pos
import telebot
from telebot import types

#TRUE – 6019076174:AAH9Sl7icwRbEz5okECl4fVR84BCzLbdYAM
#TEST – 6270339225:AAG6f1r1cMEQa1h7LHgQJDKhHr7GTSg3_fU
bot = telebot.TeleBot('6019076174:AAH9Sl7icwRbEz5okECl4fVR84BCzLbdYAM')

menu_phase = '0'

class post:
    caption = ''
    photo = ''
    address = ''
    btn_setup = [[]]
    message_id = -1
    markup = types.InlineKeyboardMarkup(row_width=3)

@bot.message_handler(commands=['start'])
def start(message):
    post.caption = ''
    post.photo = ''
    post.address = ''
    post.btn_setup = [[]]
    post.message_id = -1
    post.markup = types.InlineKeyboardMarkup(row_width=3)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("Новый пост 🖼")
    markup.add(btn)

    bot.send_message(message.chat.id, "👋 Привет! Я твой бот для постов с кнопочками")
    bot.send_message(message.chat.id, "Давай начнем создавать твой постик! 🔥🔥🔥", reply_markup=markup)
   
    

    
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global menu_phase 

    if message.text == 'Новый пост 🖼':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton("Отмена ❌")
        markup.add(btn)

        bot.send_message(message.chat.id, "Придумай надпись для поста...")
        bot.send_message(message.chat.id, "Напиши его здесь ✏️:", reply_markup=markup)
        bot.register_next_step_handler(message, post_caption)

    elif message.text == "Отмена ❌" or message.text == "Сделать еще раз 🔁":
        post.caption = ''
        post.photo = ''
        post.address = ''
        post.btn_setup = [[]]
        post.message_id = -1
        post.markup = types.InlineKeyboardMarkup(row_width=3)
        menu_phase = ''
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton("/start")
        markup.add(btn)
        bot.send_message(message.chat.id, "Напиши '/start' или нажми на кнопку", reply_markup=markup)


@bot.message_handler(content_types=['photo'])
def get_text_messages(message):
    if menu_phase == 'choose_photos':
        #choose_photos(message)
        print()

def post_caption(message):
    post.caption = message.text
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("Оставлю без фото✖️")
    markup.add(btn)

    bot.send_message(message.chat.id, "Отлично!🎊🎊🎊 \nТеперь время добавить изображение к твоему посту!")
    bot.send_message(message.chat.id, "Просто отправь мне его сообщением, и я все скомпаную 🤖", reply_markup=markup)

    bot.register_next_step_handler(message, post_image)

def post_image(message):
    if message.text != 'Оставлю без фото✖️':
        post.photo = message.photo[0].file_id 

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Новая строка ➕")
    btn2 = types.KeyboardButton("Кнопки готовы! ✅")
    markup.add(btn1, btn2)

    bot.send_message(message.chat.id, "Начни создавать кнопки в таком формате \n\n    My_btn_text - My_alert \n\nЕсли хочешь сделать новую строку кнопок, нажми на кнопку на панели")
    bot.send_message(message.chat.id, "Так будет выглядеть твой пост 🔎⤵️:... ", reply_markup=markup)

    if message.text != 'Оставлю без фото✖️':
        post_message = bot.send_photo(message.chat.id, post.photo, post.caption, reply_markup=post.markup)
    else:
        post_message = bot.send_message(message.chat.id, post.caption, reply_markup=post.markup)
    post.message_id = post_message.message_id 

    bot.register_next_step_handler(message, post_buttons)

def post_buttons(message):
    btn_info = message.text

    if btn_info.find('-') != -1:
        btn_info = btn_info.split('-')

        btn_info[0] = btn_info[0].strip()
        btn_info[1] = btn_info[1].strip()

        if 'http' in btn_info[1]:
            btn = types.InlineKeyboardButton(text=btn_info[0], url=btn_info[1])
        else:
            btn = types.InlineKeyboardButton(text=btn_info[0], callback_data=btn_info[1])
        
        post.btn_setup[len(post.btn_setup) - 1].append(btn)
        post.markup = types.InlineKeyboardMarkup(row_width=3)

        for row in range(len(post.btn_setup)):
            post.markup.row(*post.btn_setup[row])

        bot.delete_message(message.chat.id, message.message_id)

        bot.edit_message_reply_markup(message.chat.id, post.message_id, reply_markup=post.markup)

        bot.register_next_step_handler(message, post_buttons)

    elif message.text == 'Новая строка ➕':
        bot.delete_message(message.chat.id, message.message_id)
        post.btn_setup.append([])
        bot.register_next_step_handler(message, post_buttons)
    elif message.text == 'Кнопки готовы! ✅':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        bot.send_message(message.chat.id, "Отправь мне канал куда отправить пост... \n(Не забудь сперва добавить бот в администраторы канала)", reply_markup=markup)
        bot.register_next_step_handler(message, post_address)
    #row_width= len(post.btn_setup) 

def post_address(message):
    post.address = message.text
    print(post.address)
    if post.photo != '':
        bot.send_photo(post.address, post.photo, post.caption, reply_markup=post.markup)
        bot.send_message(message.chat.id, "Отправил))) Наслаждайся")
    else:
        bot.send_message(post.address, post.caption, reply_markup=post.markup)
        bot.send_message(message.chat.id, "Отправил))) Наслаждайся")
    
@bot.callback_query_handler(func= lambda call: True)
def callback(call):
    bot.answer_callback_query(call.id, call.data, show_alert=True)

bot.polling(non_stop=True) 