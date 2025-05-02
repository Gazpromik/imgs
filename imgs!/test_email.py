import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Данные для подключения
smtp_server = "smtp.yandex.ru"
smtp_port = 465  
sender_email = "Chiparick1234@yandex.ru"  # Ваш email на Яндексе
sender_password = "oxbceygctbveddim"      # Ваш пароль или пароль от приложения
recipient_email = "test-mflwaorvz@srv1.mail-tester.com"  # Email получателя

# Создание MIME-сообщения
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = recipient_email
message["Subject"] = "Подтверждение почты"

# Тело письма
body = ""
message.attach(MIMEText(body, "plain"))

# Подключение к серверу и отправка письма
try:
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        print("Сообщение успешно отправлено!")
except Exception as e:
    print(f"Ошибка при отправке сообщения: {e}")