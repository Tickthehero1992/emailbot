import telebot
import smtplib
import pandas as pd
import os
import imaplib



yandex_out = "smtp.yandex.ru"
yandex_out_port = 465
yandex_in = "pop.yandex.ru"
yandex_in_port = 995

gmail_in = "imap.gmail.com" #должна быть настроена аутентификация через приложение в гугле https://support.google.com/mail/answer/7126229?hl=ru
gmail_out = "smtp.gmail.com"
gmail_port_out = 465
gmail_port_in = 993

mail_out = "smtp.mail.ru" #должна быть настроена аутентификация в мейл https://help.mail.ru/mail/mailer/popsmtp
mail_out_port = 465
mail_in = "imap.mail.ru"
mail_in_port = 993

token = '613486352:AAGOjFuscBIb-fyXghecOST4qheIT9FFwGA' #здесь надо настроить токен бота
bot = telebot.TeleBot(token)

path_to_file = "clients.csv"

if os.path.exists(path_to_file):
    df = pd.read_csv(path_to_file, sep=';')
else:
    fl = open(path_to_file, mode='w')
    fl.write("id;address;password\n")
    fl.close()
    df = pd.read_csv(path_to_file, sep=';')

def check_address_out(st, inout):
    ll = st.split('@')
    if ll[1].find("gmail") != -1:
        if not inout:
            return gmail_out, gmail_port_out
        else:
            return gmail_in, gmail_port_in
    if ll[1].find("mail") != -1:
        if not inout:
            return mail_out, mail_out_port
        else:
            return mail_in, mail_in_port

@bot.message_handler(commands=['register']) #декоратор для приема сообщений регистр
def register_account(message):
    list_info = message.text.split() #текст из сообщения разделяем по пробелам
    address = list_info[1] #адрес 1 элемент
    password = list_info[2] #пароль второй
    id = message.from_user.id # получаем айди юзера по сообщению
    if len(list(df.loc[df['address']==address]['password'].values)) == 0: #смотрим был ли емейл в нашем файле
        host, port = check_address_out(address, False) #получаем хост и порт в зависимости от адреса мейл или джимейл
        server = smtplib.SMTP_SSL(host, port) # идем на сервер логинимся, если логин не срабатывает присылаем ошибку
        try:
            server.login(address,password)
        except:
            bot.send_message(id, "Authentification failed")
            return

        fl = open(path_to_file, mode='a') #тут добавление данных в файл по хорошему надо хэшировать емейл
        fl.write(str(id)+';'+address+';'+str(password)+'\n')
        fl.close()

@bot.message_handler(commands=['send'])
def send_message(message):
    df = pd.read_csv(path_to_file,sep=';') # открываем датафрейм наших пользователей
    list_info = message.text.split()
    fr = list_info[1]
    to = []
    msg = ""
    number = 0
    for i in range(2,len(list_info)): # ищем все емейлы
        if list_info[i].find("@")!=-1:
            to.append(list_info[i])
        else:
            number = i
            break
    for j in range(number, len(list_info)):#получаем строки сообщений
        msg+=str(list_info[j]) + " "
    id = message.from_user.id
    if id in list(df['id']):
        if fr in list(df['address']):#проверяем наличие адреса для пользователя, подключаемся логинимся отправляем, в случае ошибки пишем
            host, port = check_address_out(fr, False)
            server = smtplib.SMTP_SSL(host, port)
            server.login(fr, list(df.loc[(df['address']==fr) & (df['id']==id)]['password'].values)[0])
            server.sendmail(fr, to, msg)
            server.quit()
            bot.send_message(id,"Ваше сообщение отправлено")
        else:
            bot.send_message(id, "Нужна регистрация почты отправления")
    else:
        bot.send_message(id, "зарегистрируйтесь командой /register user password")

@bot.message_handler(commands=['read'])
def read_email(message):
    df = pd.read_csv(path_to_file, sep=';')#смотрим датафрейм почт
    address = message.text.split()[1]#адрес
    count = message.text.split()[2]#счетчик сообщений для чтения
    id = message.from_user.id
    if id in list(df['id']) and address in list(df['address']):#проверяем есть ли для пользователя почта и читаем ее
        host, port = check_address_out(address, True)
        mail = imaplib.IMAP4_SSL(host, port)
        mail.login(address, list(df.loc[(df['address']==address) & (df['id']==id)]['password'].values)[0])
        mail.list()
        mail.select("inbox")
        result, data = mail.search(None, "ALL")
        ids = data[0]
        id_list = ids.split()
        latest_email_ids = id_list[-count:-1]
        st = ""
        for l in latest_email_ids:
            result, data = mail.fetch(l, "(RFC822)")
            raw_email = data[0][1]
            raw_email_string = raw_email.decode('utf-8')
            bot.send_message(id,raw_email_string)
    else:
        bot.send_message(id, "Проверьте адресс ввода")

@bot.message_handler(commands=['help'])
def help(message):
    st = "/register user password - регистрация почты, принимаются gmail/mail, убедитесь" \
         "что вы настроили аутентификацию на почте\n" \
         "/send user emails message - отправляет сообщения из почты  user на список emails почт перечисленных через" \
         "пробел в message содержание сообщения\n" \
         "/read user count - читает сообщения из почты user count - количество сообщений"
    bot.send_message(message.from_user.id, st)


bot.polling(none_stop=True, interval=0)