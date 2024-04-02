import sqlite3 as db
import telebot
import config
import datetime
import threading
lock = threading.Lock()
bot = telebot.TeleBot(config.TOKEN)

db = db.connect('database.db', check_same_thread=False)
cur = db.cursor()
global info
global checking_exist
global forbidden_time


def create_table():
    cur.execute("CREATE TABLE IF NOT EXISTS customers("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "tg_id int,"
                "name TEXT,"
                "date TEXT,"
                "cut_style TEXT,"
                "preferred_time TEXT)")
    db.commit()


def checking_user(message):
    user = cur.execute("SELECT * FROM customers WHERE tg_id == {key}".format(key=message)).fetchone()
    if not user:
        cur.execute("INSERT INTO customers (tg_id) VALUES ('%d')" % message)
        db.commit()


def insert_date(message, message2):
    cur.execute("UPDATE customers SET date = ('%s') WHERE tg_id = ('%s')" % (message, message2))
    db.commit()


def insert_name(message, message2):
    cur.execute("UPDATE customers SET name = ('%s') WHERE tg_id = ('%s')" % (message, message2))
    db.commit()


def insert_time(message, message2):
    cur.execute("UPDATE customers SET preferred_time = ('%s') WHERE tg_id = ('%s')" % (message, message2))
    db.commit()


def insert_cut_style(message, message2):
    cur.execute("UPDATE customers SET cut_style = ('%s') WHERE tg_id = ('%s')" % (message, message2))
    db.commit()


def see_all_customers(message):
    cur.execute("SELECT * FROM customers")
    customers = cur.fetchall()

    global info
    info = ''

    for customer in customers:
        info += f"""{customer[2]} | {customer[3]} | {customer[5]} |
{customer[4]}____________________________________\n"""

    bot.send_message(message.chat.id, info, parse_mode='html')
    db.commit()


def checking_for_replacing_time():
    cur.execute("SELECT * FROM customers")
    customers = cur.fetchall()

    global checking_exist
    checking_exist = []

    for customer in customers:
        checking_exist.append(customer[2])

    db.commit()


def examination_hours():
    with lock:
        cur.execute("SELECT * FROM customers WHERE date = ('%s')" % (str(datetime.datetime.now().day)))
        customers = cur.fetchall()
        global forbidden_time
        forbidden_time = []

    for customer in customers:
        forbidden_time.append(customer[5])
    db.commit()


def examination_hours_2():
    with lock:
        cur.execute("SELECT * FROM customers WHERE date = ('%s')" % (datetime.datetime.now().day + 1))
        customers = cur.fetchall()
        global forbidden_time
        forbidden_time = []

    for customer in customers:
        forbidden_time.append(customer[5])
    db.commit()


def adding_forbidden_time(message, message2):
    cur.execute("INSERT INTO customers (tg_id, name, date, preferred_time) VALUES ('0', 'Barber', '%s', '%s')"
                % (message, message2.text))
    db.commit()


def update_db():
    cur.execute("DELETE FROM customers")
    db.commit()
