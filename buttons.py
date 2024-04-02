import database as db
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from datetime import datetime
from pytz import timezone
tz_yerevan = timezone('Asia/Yerevan')
global list_hours
global times
global times_2
global cutting_style
global current_date
global weekday
global date_button
register_button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn1 = KeyboardButton("✅ Գրանցվել")
btn2 = KeyboardButton("📍 Գտնվելու Վայրը")
btn6 = KeyboardButton("🧡 Իդրամ")
btn7 = KeyboardButton("🔁 Փոփոխել ժամը")
btn8 = KeyboardButton("☎️ Զանգահարել")
btn10 = KeyboardButton("💲 գնացուցակ")
register_button.add(btn1, btn2, btn6, btn7, btn8, btn10)


def forb_times_current_day():
    db.examination_hours()
    list_hours = ["11:00", "11:30", "12:00", "12:30", "13:00", "13:30",
                  "14:00", "14:30", "15:00", "15:30", "16:00", "16:30",
                  "17:00", "17:30", "18:00", "18:30", "19:00", "19:30",
                  "20:00", "20:30", "21:00", "21:30", "22:00", "22:30"]
    for el in db.forbidden_time:
        try:
            index = list_hours.index(el)
        except ValueError:
            continue
        list_hours.pop(index)
        list_hours.insert(index, f"Զբաղված   {el}")

    global times
    times = ReplyKeyboardMarkup(row_width=3)
    for hour in range(0, len(list_hours), 3):
        times.row(KeyboardButton(list_hours[hour]),
                  KeyboardButton(list_hours[hour + 1]),
                  KeyboardButton(list_hours[hour + 2]))
    times.row(KeyboardButton("↩️ Վարադառնալ"))


def forb_times_current_day_2():
    db.examination_hours_2()
    list_hours = ["11:00", "11:30", "12:00", "12:30", "13:00", "13:30",
                  "14:00", "14:30", "15:00", "15:30", "16:00", "16:30",
                  "17:00", "17:30", "18:00", "18:30", "19:00", "19:30",
                  "20:00", "20:30", "21:00", "21:30", "22:00", "22:30"]
    for el in db.forbidden_time:
        try:
            index = list_hours.index(el)
        except ValueError:
            continue
        list_hours.pop(index)
        list_hours.insert(index, f"Զբաղված   {el}")

    global times_2
    times_2 = ReplyKeyboardMarkup(row_width=3)
    for hour in range(0, len(list_hours), 3):
        times_2.row(KeyboardButton(list_hours[hour]),
                    KeyboardButton(list_hours[hour + 1]),
                    KeyboardButton(list_hours[hour + 2]))
    times_2.row(KeyboardButton("↩️ Վարադառնալ"))


map_button = InlineKeyboardMarkup()
map_button.add(InlineKeyboardButton("📌 Բացել Քարտեզը", url="https://yandex.ru/maps/116123/metsamor/?ll=44.118383%2"
                                                           "C40.143820&mode=poi&poi%5Bpoint%5D=44.118468%2C40.143809&po"
                                                           "i%5Buri%5D=ymapsbm1%3A%2F%2Forg%3Foid%3D220927114235&z=21"))

lst_weekdays = ["Երկուշաբթի", "Երեքշաբթի", "Չորեքշաբթի", "Հինգշաբթի", "Ուրբաթ", "Շաբաթ", "Կիրակի"]


def mention_timezone():
    global current_date
    global weekday
    current_date = datetime.now(tz_yerevan)
    weekday = current_date.weekday()
    global date_button
    date_button = ReplyKeyboardMarkup(resize_keyboard=True)
    for day in range(current_date.day, current_date.day + 2):
        if weekday == 0:
            weekday = lst_weekdays[0]
        elif weekday == 1:
            weekday = lst_weekdays[1]
        elif weekday == 2:
            weekday = lst_weekdays[2]
        elif weekday == 3:
            weekday = lst_weekdays[3]
        elif weekday == 4:
            weekday = lst_weekdays[4]
        elif weekday == 5:
            weekday = lst_weekdays[5]
        elif weekday == 6:
            weekday = lst_weekdays[6]
        elif weekday == 7:
            weekday = lst_weekdays[0]
        date_button.add(KeyboardButton(f"{weekday} | {day}"))
        weekday = current_date.weekday() + 1
    date_button.add(KeyboardButton("↩️ Վարադառնալ"))


main_button = ReplyKeyboardMarkup(resize_keyboard=True)
btn3 = KeyboardButton("🤍 Ադմին Հարթակ")
main_button.add(btn1, btn2)
main_button.row(btn6, btn7)
main_button.row(btn8, btn3)


admin_panel = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn4 = KeyboardButton("📋 Տեսնել հաճախորդների ցուցակը")
btn5 = KeyboardButton("↩️ Վարադառնալ")
btn9 = KeyboardButton("🔁 Վերաակտիվացնել ցուցակը")
btn11 = KeyboardButton("⏰Ավելացնել զբաղված ժամ")
admin_panel.add(btn4, btn5, btn9, btn11)

back_button = ReplyKeyboardMarkup(resize_keyboard=True)
back_button.add(btn5)


def cut():
    global cutting_style
    cutting_style = InlineKeyboardMarkup(row_width=1)
    lst_style = ["Մորուքի մոդելավորում - 1000 դր․", "Ոսկ (Մազահեռացում) - 1000 դր․", "Մազի կտրվածք - 1500 դր․",
                 "Մազի Ներկում - 1500 դր․", "Մորուքի ներկում - 1500 դր․", "Դեմքի խնամք - 2000 դր․",
                 "Մազի և մորուքի ներկում - 2000 դր․", "Ածելիով սափրում (գլխի) - 2000 դր․",
                 "Մազի և Մորուքի կտրվածք - 2500 դր․"]
    for el in lst_style:
        cutting_style.add(InlineKeyboardButton(el, callback_data=el))
