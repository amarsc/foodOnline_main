import os
import smtplib
from email.message import EmailMessage

#credentials
email_user = 'prabhatidubey@outlook.com'
email_pass = 'God@1110'
contacts = ['vivekchauhan14@hotmail.com']
sender = email_user
to = contacts

msg = EmailMessage()
msg['Subject'] = 'Subject...............E'
msg['From'] = sender
msg['To'] = ', '.join(contacts)
msg.set_content('YOUR EMAIL MESSAGE HERE')

try:
    with smtplib.SMTP('smtp-mail.outlook.com', 587) as smtp:
        smtp.starttls()
        smtp.login(email_user, email_pass)
        print("after login ........................")
        smtp.send_message(msg)
except Exception as e:
    print(e)