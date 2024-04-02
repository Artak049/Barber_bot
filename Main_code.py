import telebot
import database as db
import buttons
import config
from string import punctuation
from string import digits
import datetime
from pytz import timezone
tz_yerevan = timezone('Asia/Yerevan')


db.create_table()
forbidden_name = punctuation + digits
bot = telebot.TeleBot(config.TOKEN)
buttons.forb_times_current_day()
buttons.forb_times_current_day_2()
buttons.cut()
buttons.mention_timezone()
global name
global date
global cut_style
global date_text


@bot.message_handler(commands=['start'])
def send_welcome_and_register(message):
    db.create_table()
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIVBmXBMbmjXKgS7Yh3SR5y8t5Zcyj1AAIEAQACVp29Ct4E0XpmZvdsNAQ')
    bot.send_message(message.chat.id, f"Ողջունում ենք ձեզ Հարգելի {message.from_user.first_name} 😊",
                     reply_markup=buttons.register_button)
    db.checking_user(message.from_user.id)
    if message.from_user.id == config.ADMIN_ID:
        bot.send_message(message.chat.id, "Դուք մուտք եք գործել որպես Ադմին 😍", reply_markup=buttons.main_button)


@bot.message_handler(content_types=['photo'])
def send_photo(message):
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAIeymXFUrbnlozqsPuvCkyg1XXLmVHeAAL5AANWnb0KlWVuqyorGzY0BA")


@bot.message_handler(content_types=['text'])
def handle_message(message):
    if message.text == "✅ Գրանցվել":
        db.insert_name(message.from_user.first_name, message.chat.id)
        db.checking_user(message.from_user.id)
        buttons.cut()
        bot.send_message(message.chat.id, "Ընտրեք կտրվածքը: ✂", reply_markup=buttons.cutting_style)
    elif message.text == "📍 Գտնվելու Վայրը":
        bot.send_message(message.chat.id, "Բարբեր սրահը գտնվում է Ավտոմասերի խանութի կողքին",
                         reply_markup=buttons.map_button)
    elif message.text == "🧡 Իդրամ":
        with open("Idram.jpg", "rb") as photo:
            bot.send_photo(message.chat.id, photo)
    elif message.text == "🔁 Փոփոխել ժամը":
        try:
            db.checking_for_replacing_time()
            if message.from_user.first_name not in db.checking_exist:
                bot.send_message(message.chat.id, "Դուք դեռ չեք գրանցվել։", reply_markup=buttons.register_button)
            else:
                bot.send_message(message.chat.id, "Ընտրեք օրը:", reply_markup=buttons.date_button)
                bot.register_next_step_handler(message, choosing_date)
        except NameError:
            bot.send_message(message.chat.id, "Դուք դեռ չեք գրանցվել։", reply_markup=buttons.register_button)
    elif message.text == "☎️ Զանգահարել":
        bot.send_message(message.chat.id, "<a>+37494080775</a>", parse_mode='html')
    elif message.text == "🤍 Ադմին Հարթակ":
        if message.from_user.id == config.ADMIN_ID:
            bot.send_message(message.chat.id, "Դուք Մուտք եք գործել Ադմին հարթակ", reply_markup=buttons.admin_panel)
            bot.register_next_step_handler(message, admin_panel)
        else:
            bot.send_message(message.chat.id, "🤷‍♂️ Ես քեզ չեմ հասկանում")
    elif message.text == "💲 գնացուցակ":
        bot.send_message(message.chat.id, """Մազի կտրվածք - <b><u>1500 դր․</u></b>
Մորուքի մոդելավորում - <b><u>1000 դր․</u></b>
Դեմքի խնամք - <b><u>2000 դր․</u></b>
Ոսկ (Մազահեռացում) - <b><u>1000 դր․</u></b>
Մազի Ներկում - <b><u>1500 դր․</u></b>
Մորուքի ներկում - <b><u>1500 դր․</u></b>
Մազի և մորուքի ներկում - <b><u>2000 դր․</u></b>
Ածելիով սափրում (գլխի) - <b><u>2000 դր․</u></b>""", parse_mode="html")
    elif message.text == "/start":
        if message.from_user.id == config.ADMIN_ID:
            bot.send_message(message.chat.id, f"Մենք արդեն ձեզ ողջունել ենք {message.from_user.first_name} 😊",
                             reply_markup=buttons.main_button)
        else:
            bot.send_message(message.chat.id, f"Մենք արդեն ձեզ ողջունել ենք {message.from_user.first_name} 😊",
                             reply_markup=buttons.register_button)
    else:
        bot.reply_to(message, "🤷‍♂️ Ես քեզ չեմ հասկանում")
        bot.register_next_step_handler(message, handle_message)


def admin_panel(message):
    if message.text == "📋 Տեսնել հաճախորդների ցուցակը":
        db.see_all_customers(message)
        bot.register_next_step_handler(message, admin_panel)
    elif message.text == "↩️ Վարադառնալ":
        bot.send_message(message.chat.id, "Դուք նախորդ մենյույում եք։", reply_markup=buttons.main_button)
    elif message.text == "🔁 Վերաակտիվացնել ցուցակը":
        db.update_db()
        bot.send_message(message.chat.id, "Ցուցակը թարմացվել է։", reply_markup=buttons.main_button)
        bot.register_next_step_handler(message, handle_message)
    elif message.text == "⏰Ավելացնել զբաղված ժամ":
        bot.send_message(message.chat.id, "ընտրեք ամսվա օրը։", reply_markup=buttons.date_button)
        bot.register_next_step_handler(message, adding_forbidden_time_dating)
    else:
        bot.reply_to(message, "🤷‍♂️ Ես քեզ չեմ հասկանում")
        bot.register_next_step_handler(message, admin_panel)


def adding_forbidden_time_dating(message):
    global date_text
    date_text = message.text.split(' ')[-1]
    if date_text == datetime.datetime.now().day:
        bot.send_message(message.chat.id, "ընտրեք ժամը։", reply_markup=buttons.times)
    elif message.text == "↩️ Վարադառնալ":
        bot.send_message(message.chat.id, "Դուք նախորդ մենյույում եք։", reply_markup=buttons.main_button)
    else:
        bot.send_message(message.chat.id, "ընտրեք ժամը։", reply_markup=buttons.times_2)
        bot.register_next_step_handler(message, adding_forbidden_time)


def adding_forbidden_time(message):
    buttons.mention_timezone()
    db.adding_forbidden_time(date_text, message)
    bot.send_message(message.chat.id, "ժամը ավելացվել է:", reply_markup=buttons.date_button)
    bot.register_next_step_handler(message, adding_forbidden_time_dating)


@bot.callback_query_handler(func=lambda callback: True)
def cutting_style(callback):
    global cut_style
    cut_style = callback.data
    buttons.mention_timezone()
    db.insert_cut_style(cut_style, callback.message.chat.id)
    bot.send_message(callback.message.chat.id, "Շատ լավ\nԸնտրեք օրը:", reply_markup=buttons.date_button)
    bot.register_next_step_handler(callback.message, choosing_date)


def choosing_date(message):
    global date
    message_text = message.text.split(' ')
    if message.text == "↩️ Վարադառնալ":
        bot.send_message(message.chat.id, "Դուք նախորդ մենյույում եք։", reply_markup=buttons.register_button)
    elif int(message_text[-1]) == datetime.datetime.now(tz_yerevan).day:
        date = message_text[-1]
        buttons.forb_times_current_day()
        db.insert_date(date, message.chat.id)
        bot.send_message(message.chat.id, "Կարող եք ընտրել ձեզ հարմար ժամը", reply_markup=buttons.times)
        bot.register_next_step_handler(message, after_register)
    elif int(message_text[-1]) == datetime.datetime.now(tz_yerevan).day + 1:
        date = message_text[-1]
        buttons.forb_times_current_day_2()
        db.insert_date(date, message.chat.id)
        bot.send_message(message.chat.id, "Կարող եք ընտրել ձեզ հարմար ժամը", reply_markup=buttons.times_2)
        bot.register_next_step_handler(message, after_register)
    else:
        bot.reply_to(message, "🤷‍♂️ Ես քեզ չեմ հասկանում")
        bot.register_next_step_handler(message, choosing_date)


def after_register(message):
    lst_hours = ["11:00", "11:30", "12:00", "12:30", "13:00", "13:30",
                 "14:00", "14:30", "15:00", "15:30", "16:00", "16:30",
                 "17:00", "17:30", "18:00", "18:30", "19:00", "19:30",
                 "20:00", "20:30", "21:00", "21:30", "22:00", "22:30"]
    if message.text in lst_hours:
        db.insert_time(message.text, message.from_user.id)
        if message.from_user.id == config.ADMIN_ID:
            bot.send_message(message.chat.id, f"Կսպասենք, ամսի {date}-ին, ժամը <b><u>{message.text}</u></b> |-ին 😊",
                             parse_mode='html', reply_markup=buttons.main_button)
        else:
            bot.send_message(chat_id=config.ADMIN_ID, text=f"{message.from_user.first_name}-ը գրանցվել է ամսի {date}-ին, ժամը "
                                                           f"{message.text}-ին, {cut_style}")
            bot.send_message(message.chat.id, f"Կսպասենք, ամսի {date}-ին, ժամը <b><u>{message.text}</u></b> |-ին 😊",
                             parse_mode='html', reply_markup=buttons.register_button)
    elif message.text == "↩️ Վարադառնալ":
        message.text = message.text[0]
        if message.from_user.id == config.ADMIN_ID:
            bot.send_message(message.chat.id, "Դուք նախորդ մենյույում եք։", reply_markup=buttons.main_button)
        else:
            bot.send_message(message.chat.id, "Դուք նախորդ մենյույում եք։", reply_markup=buttons.register_button)
    else:
        bot.reply_to(message, "🤷‍♂️ Ես քեզ չեմ հասկանում")
        bot.register_next_step_handler(message, after_register)


if __name__ == "__main__":
    bot.infinity_polling(none_stop=True)
