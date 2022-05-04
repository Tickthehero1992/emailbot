import smtplib

yandex_out = "smtp.yandex.ru"
yandex_out_port = 465
yandex_in = "pop.yandex.ru"
yandex_in_port = 995

gmail_in = "imap.gmail.com"
gmail_out = "smtp.gmail.com"
gmail_port_out = 465
gmail_port_in = 993

mail_out = "smtp.mail.ru"
mail_out_port = 465

mail_in = "imap.mail.ru"
mail_in_port = 993
server = smtplib.SMTP_SSL(mail_out, mail_out_port)
#server.login("gorshkovitchairlines@gmail.com", "tickthehero201192")
#server.sendmail("gorshkovitchairlines@gmail.com", ["gorshkovitchairlines@gmail.com"], "hello")
server.login("pereirasanchez@mail.ru", "PVhN745H3z9BbtpQXdHB")
server.sendmail("pereirasanchez@mail.ru", ["gorshkovitchairlines@gmail.com"], "hello")
server.quit()
