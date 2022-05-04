убедитесь что произведены настройки на мейл и gmail
gmail: https://support.google.com/mail/answer/7126229?hl=ru
mail: https://help.mail.ru/mail/mailer/popsmtp

установка 
pip install virtualenv
mkdir venv
python3 -m venv venv
source venv/bin/activate
pip install -r req.txt
python bot.py

предварительно стоит заменить токен бота в строке 24, получается от
botfather в телеграмме
запуск python bot.py 