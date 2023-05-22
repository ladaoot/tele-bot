import telebot
from telebot import types
from datetime import date

import psycopg2

token = '6097613713:AAEFihuglVUksXHl-7kFrKw0amFYDuVqtcg'

bot = telebot.TeleBot(token)

week_n = int(date.today().isocalendar().week)
if week_n % 2 == 0:
    st = 'четная'
else:
    st = 'нечетная'

conn = psycopg2.connect(database="schedule",
                        user="postgres",
                        password='lada',
                        host="localhost",
                        port="5432")

cursor = conn.cursor()


@bot.message_handler(commands=['start'])
def start(massage):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота")
    keyboard.row("Расписание на неделю",
                 "Расписание на следующую неделю")
    bot.send_message(massage.chat.id,
                     'Здравствуй, {}!\n'
                     'Этот бот был создан чтобы узнавать расписание группы БВТ2206.\n'
                     'Автором этого бота является Чумакова Лада.\n'
                     'Для того чтобы узнать имеющиеся команды используйте /help'.format(
                         massage.from_user.first_name), reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'У нас есть несколько команд, которые помогут Вам в использавие ботом:\n'
                                      '/help - Вы получите документацию и список команд;\n'
                                      '/mtuci - ссылка на сайт университета МТУСИ;\n'
                                      '/week - выводит какая сейчас неделя учебы четная или нечетная.')


@bot.message_handler(commands=['mtuci'])
def mtuci(message):
    bot.send_message(message.chat.id, 'Сайт нашего университета - https://mtuci.ru/')


@bot.message_handler(commands=['week'])
def week(message):
    bot.send_message(message.chat.id, 'Сейчас ' + st + ' неделя')


@bot.message_handler(func=lambda message: message.text == "Понедельник")
def monday(message):
    cursor.execute(
        "select t.subject, room_number, start_time, full_name from teacher as t "
        "join (select * from timetable where day='Понедельник' and week='{}') "
        "as s on t.subject=s.subject order by start_time;".format(
            st))
    records = list(cursor.fetchall())
    ms = "Понедельник ({} неделя)\n" \
         "_______________________\n".format(st)
    for r in records:
        ms = ms + r[0] + " | " + r[1] + " | " + r[2] + " | " + r[3] + "\n\n"
    bot.send_message(message.chat.id, ms)


@bot.message_handler(func=lambda message: message.text == "Вторник")
def tuesday(message):
    cursor.execute(
        "select t.subject, room_number, start_time, full_name from teacher as t "
        "join (select * from timetable where day='Вторник' and week='{}') "
        "as s on t.subject=s.subject order by start_time;".format(
            st))
    records = list(cursor.fetchall())
    ms = "Вторник ({} неделя)\n" \
         "_______________________\n".format(st)
    for r in records:
        ms = ms + r[0] + " | " + r[1] + " | " + r[2] + " | " + r[3] + "\n\n"
    bot.send_message(message.chat.id, ms)


@bot.message_handler(func=lambda message: message.text == "Среда")
def wednesday(message):
    cursor.execute(
        "select t.subject, room_number, start_time, full_name from teacher as t "
        "join (select * from timetable where day='Среда' and week='{}') "
        "as s on t.subject=s.subject order by start_time;".format(
            st))
    records = list(cursor.fetchall())
    ms = "Среда ({} неделя)\n" \
         "_______________________\n".format(st)
    for r in records:
        ms = ms + r[0] + " | " + r[1] + " | " + r[2] + " | " + r[3] + "\n\n"
    bot.send_message(message.chat.id, ms)


@bot.message_handler(func=lambda message: message.text == "Четверг")
def thursday(message):
    cursor.execute(
        "select t.subject, room_number, start_time, full_name from teacher as t "
        "join (select * from timetable where day='Четверг' and week='{}') "
        "as s on t.subject=s.subject order by start_time;".format(
            st))
    records = list(cursor.fetchall())
    ms = "Четверг ({} неделя)\n" \
         "_______________________\n".format(st)
    for r in records:
        ms = ms + r[0] + " | " + r[1] + " | " + r[2] + " | " + r[3] + "\n\n"
    bot.send_message(message.chat.id, ms)


@bot.message_handler(func=lambda message: message.text == "Пятница")
def friday(message):
    cursor.execute(
        "select t.subject, room_number, start_time, full_name from teacher as t "
        "join (select * from timetable where day='Пятница' and week='{}') "
        "as s on t.subject=s.subject order by start_time;".format(
            st))
    records = list(cursor.fetchall())
    ms = "Пятница ({} неделя)\n" \
         "_______________________\n".format(st)
    for r in records:
        ms = ms + r[0] + " | " + r[1] + " | " + r[2] + " | " + r[3] + "\n\n"
    bot.send_message(message.chat.id, ms)


@bot.message_handler(func=lambda message: message.text == "Суббота")
def saturday(message):
    cursor.execute(
        "select t.subject, room_number, start_time, full_name from teacher as t "
        "join (select * from timetable where day='Суббота' and week='{}') "
        "as s on t.subject=s.subject order by start_time;".format(
            st))
    records = list(cursor.fetchall())
    ms = "Суббота ({} неделя)\n" \
         "_______________________\n".format(st)
    for r in records:
        ms = ms + r[0] + " | " + r[1] + " | " + r[2] + " | " + r[3] + "\n\n"
    bot.send_message(message.chat.id, ms)


@bot.message_handler(func=lambda message: message.text == "Расписание на неделю")
def now_week(message):
    cursor.execute(
        "select day, t.subject, room_number, start_time, full_name from teacher as t "
        "join (select * from timetable where week='{}') "
        "as s on t.subject=s.subject order by s.id;".format(
            st))
    records = list(cursor.fetchall())
    ms = "Расписание на эту неделю ({})\n" \
         "_______________________\n".format(st)
    dir = dict()
    for r in records:
        if r[0] in dir:
            dir[r[0]] += r[1] + " | " + r[2] + " | " + r[3] + " | " + r[4] + "\n\n"
        else:
            dir[r[0]] = r[1] + " | " + r[2] + " | " + r[3] + " | " + r[4] + "\n\n"
    for k, v in dir.items():
        ms = ms + k + "\n__________________________________\n" + v + "\n\n"
    bot.send_message(message.chat.id, ms)


@bot.message_handler(func=lambda message: message.text == "Расписание на следующую неделю")
def next_week(message):
    if st == "четная":
        st_1 = "нечетная"
    else:
        st_1 = "четная"
    cursor.execute(
        "select day, t.subject, room_number, start_time, full_name from teacher as t "
        "join (select * from timetable where week='{}') "
        "as s on t.subject=s.subject order by s.id;".format(
            st_1))
    records = list(cursor.fetchall())
    ms = "Расписание на следующую неделю ({})\n" \
         "_______________________\n".format(st_1)
    dir = dict()
    for r in records:
        if r[0] in dir:
            dir[r[0]] += r[1] + " | " + r[2] + " | " + r[3] + " | " + r[4] + "\n\n"
        else:
            dir[r[0]] = r[1] + " | " + r[2] + " | " + r[3] + " | " + r[4] + "\n\n"
    for k, v in dir.items():
        ms = ms + k + "\n__________________________________\n" + v + "\n\n"
    bot.send_message(message.chat.id, ms)


@bot.message_handler(content_types=['text'])
def text(message):
    bot.send_message(message.chat.id, "Извините, я Вас не понял")


bot.polling(none_stop=True)
