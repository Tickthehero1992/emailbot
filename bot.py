import telebot
import smtplib
import pandas as pd
import os
import imaplib
import email
import hashlib
import uuid
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup

from email.header import decode_header

salt = uuid.uuid4().hex

def hash_password(password):
    # uuid используется для генерации случайного числа
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

text_subtype = 'plain'


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

    if st.find('@')==-1:
        return None, None
    ll = st.split('@')
    if ll[1].find("mail") == -1:
        if not inout:
            return mail_out, mail_out_port
        else:
            return mail_in, mail_in_port
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
    id = message.from_user.id # получаем айди юзера по сообщению
    if len(message.text.split())<2:
        bot.send_message(id, "Неверная команда")
        return
    list_info = message.text.split() #текст из сообщения разделяем по пробелам
    address = list_info[1] #адрес 1 элемент
    password = list_info[2] #пароль второй

    if len(list(df.loc[df['address']==address]['password'].values)) == 0: #смотрим был ли емейл в нашем файле
        host, port = check_address_out(address, False) #получаем хост и порт в зависимости от адреса мейл или джимейл
        if host is None:
            if port == 0:
                bot.send_message(id, "Нужна почта gmail mail")
                return
            bot.send_message(id, "Проверьте вводимую почту")
            return
        server = smtplib.SMTP_SSL(host, port) # идем на сервер логинимся, если логин не срабатывает присылаем ошибку
        try:
            server.login(address,password)
        except:
            bot.send_message(id, "Ошибка авторизации")
            return

        fl = open(path_to_file, mode='a') #тут добавление данных в файл по хорошему надо хэшировать емейл
        fl.write(str(id)+';'+address+';'+str(password)+'\n')
        fl.close()
        bot.send_message(id, "Пользователь добавлен")
    else:
        bot.send_message(id, "Пользователь уже есть")


@bot.message_handler(commands=['send'])
def send_message(message):
    df = pd.read_csv(path_to_file,sep=';') # открываем датафрейм наших пользователей
    id = message.from_user.id
    if len(message.text.split())<3:
        bot.send_message(id, "Неверная команда")
        return
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
    if len(to)==0:
        bot.send_message(id, "Вы не ввели адресата")
        return

    for j in range(number, len(list_info)):#получаем строки сообщений
        msg+=str(list_info[j]) + " "

    if msg == "" or number==0:
        bot.send_message(id, "Вы не ввели сообщение")
        return
    if len(df.loc[(df['address'] == fr) & (df['id'] == id)]['password'].values) != 0:
            host, port = check_address_out(fr, False)
            st = msg.replace(list_info[number],'')
            subject = list_info[number]
            msg = MIMEMultipart()
            msg['From'] = fr
            msg['To'] = ''.join(to)
            msg['Date'] = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
            msg['Subject'] = subject

            msg.attach(MIMEText(st.encode('utf-8'), _charset='utf-8'))
            server = smtplib.SMTP_SSL(host, port)
            server.login(fr, list(df.loc[(df['address']==fr) & (df['id']==id)]['password'].values)[0])
            server.sendmail(fr, to, msg.as_string())
            server.quit()
            bot.send_message(id,"Ваше сообщение отправлено")
    else:
        bot.send_message(id, "Зарегистрируйтесь командой /register user password")

@bot.message_handler(commands=['read'])
def read_email(message):
    df = pd.read_csv(path_to_file, sep=';')#смотрим датафрейм почт
    id = message.from_user.id
    if len(message.text.split())<2:
        bot.send_message(id, "Неверная команда")
        return
    address = message.text.split()[1]#адрес
    if len(message.text.split())<3:
        count = 0
    else:
        count = message.text.split()[2]#счетчик сообщений для чтения

    if len(df.loc[(df['address']==address) & (df['id']==id)]['password'].values) != 0 :#проверяем есть ли для пользователя почта и читаем ее
        host, port = check_address_out(address, True)
        mail = imaplib.IMAP4_SSL(host, port)
        mail.login(address, list(df.loc[(df['address']==address) & (df['id']==id)]['password'].values)[0])
        mail.list()
        mail.select("inbox")
        result, data = mail.search(None, "ALL")
        ids = data[0]
        id_list = ids.split()
        try:
            count = int(count)
        except:
            bot.send_message(id, "Не корректное количество сообщений")
            return

        if count < 2:
            latest_email_ids = []
            latest_email_ids.append(id_list[-1])
        else:
            latest_email_ids = id_list[-count-1:-1]
        st = ""

        if len(latest_email_ids)>4:
            bot.send_message(id, "Слишком много сообщений")
            return
        for l in latest_email_ids:
            result, data = mail.fetch(l, "(RFC822)")
            raw_email = data[0][1]

            raw_email_string = raw_email.decode('utf-8')
            b = email.message_from_bytes(raw_email)
            if b["Subject"] is not None:
                subject, encoding = decode_header(b["Subject"])[0]
                st += "Subject: "
                if isinstance(subject, bytes):
                    st+=subject.decode('utf-8')
                else:
                    st+=subject
                st += '\n'
            if b.get("From") is not None:
                From, encoding = decode_header(b.get("From"))[0]
                st += "From: "
                if isinstance(From, bytes):
                    st += From.decode('utf-8')
                else:
                    st += From
                st+='\n'
            if b.get("To") is not None:
                To, encoding = decode_header(b.get("To"))[0]
                st+= "To: "
                if isinstance(To, bytes):
                    st += To.decode('utf-8')
                else:
                    st += To
                st += '\n'
            if b.get("Date") is not None:
                Date, encoding = decode_header(b.get("Date"))[0]
                st+="Date: "
                st += Date
            st+='\nText: '
            if b.is_multipart():
                for part in b.walk():
                    # extract content type of email
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        # get the email body
                        body = part.get_payload(decode=True).decode()


                    except:
                        pass
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        # print text/plain emails and skip attachments
                        st+=body
                    if content_type == "text/html":
                        soup = BeautifulSoup(body, 'html.parser')
                        ll = soup.get_text()
                        ll = ll.replace("  ", '')
                        ll = ll.replace("\n\n", '')
                        ll = ll.replace(" \n", '')
                        ll = ll.replace("\t", '')
                        st += ll

            else:
                content_type = b.get_content_type()
                # get the email body
                body = b.get_payload(decode=True).decode()

                if content_type == "text/plain":
                    # print only text email parts
                    st+=body
                if content_type == "text/html":
                    soup = BeautifulSoup(body,'html.parser')
                    ll = soup.get_text()
                    ll = ll.replace("  ",'')
                    ll = ll.replace("\n\n", '')
                    ll = ll.replace(" \n",'')
                    ll = ll.replace("\t", '')
                    st+=ll

        bot.send_message(id,st)
    else:
        bot.send_message(id, "Не зарегистрированный пользователь для данного аккаунта")

@bot.message_handler(commands=['help'])
def help(message):
    st = "/register user password - регистрация почты, принимаются gmail/mail, убедитесь" \
         "что вы настроили аутентификацию на почте\n" \
         "/send user emails title message - отправляет сообщения из почты  user на список emails почт перечисленных через" \
         "пробел в message содержание сообщения и с заглавием title\n" \
         "/read user count - читает сообщения из почты user count - количество сообщений"
    bot.send_message(message.from_user.id, st)


bot.polling(none_stop=True, interval=0)