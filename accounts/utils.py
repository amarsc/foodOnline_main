from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings

import os
import smtplib
from email.message import EmailMessage

def detectUser(user):
    if user.role ==1:
        redirectUrl='vendorDashboard'
        return redirectUrl
    elif user.role ==2:
        redirectUrl='custDashboard'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl ='/admin'
        return redirectUrl
    
    
def send_verification_email(request,user):
    current_site=get_current_site(request)
    mail_subject="Please activate your account"
    message= render_to_string('accounts/emails/account_verification_email.html', {
        'user' : user,
        'domain': current_site,
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user)
    })
    to_email= 'vivekchauhan14@hotmail.com'  #user.email
    mail= EmailMessage(mail_subject,message, to=[to_email])
    mail.send()
    

def sendActivation_mail(request,user,email_subject, email_template):
#credentials
    email_user ='prabhatidubey@outlook.com'
    email_pass = 'God@1110'
    # contacts =  [user.email,] # ['vivekchauhan14@hotmail.com'] 
    msg = EmailMessage()
    msg['Subject'] = email_subject #"Please activate your account"
    msg['From'] = email_user
    msg['To'] = ', '.join( [user.email,])
    message = render_to_string(email_template, {
        'user' : user,
        'domain': '127.0.0.1:8000',
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user)
    })
    
    print("message: &&  ** ", message)
    msg.set_content(message)
    try:
        with smtplib.SMTP('smtp-mail.outlook.com', 587) as smtp:
            smtp.starttls()
            smtp.login(email_user, email_pass)
            print("sending activation email ........................")
            smtp.send_message(msg)
    except Exception as e:
        print(e)
    
    
def send_password_reset_email(request,user):
#credentials
    email_user ='prabhatidubey@outlook.com'
    print("sendActivation_mail email_user", email_user)
    email_pass = 'God@1110'

    contacts =  [user.email,] # ['vivekchauhan14@hotmail.com']
    sender = email_user
    to = contacts

    msg = EmailMessage()
    msg['Subject'] ="Reset your password"
    msg['From'] = sender
    msg['To'] = ', '.join(contacts)
    msg.set_content('YOUR EMAIL MESSAGE HERE')
    message= render_to_string('accounts/emails/reset_password_email.html', {
        'user' : user,
        'domain': '127.0.0.1:8000',
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user)
    })
    
    print("message: &&  ** ", message)
    msg.set_content(message)
    try:
        with smtplib.SMTP('smtp-mail.outlook.com', 587) as smtp:
            print("utils ....... inside try ............")
            smtp.starttls()
            smtp.login(email_user, email_pass)
            print("after login ........................")
            # smtp.send_message(msg)
    except Exception as e:
        print(e)
    


def send_notification(mail_subject,mail_template,context):
    email_user = 'amarsc28041972@rediffmail.com'#'prabhatidubey@outlook.com'
    # print("sendActivation_mail email_user", email_user)
    email_pass= 'Bhopal@123'#'God@1110'    
    # contacts =  context['user'].email# ['vivekchauhan14@hotmail.com']

    msg = EmailMessage()
    msg['Subject'] = mail_subject #"Please activate your account"
    msg['From'] = email_user
    msg['To'] = context['user'].email
   
    message= render_to_string(mail_template,context)
    
    print("message: &&  ** ", message)
    msg.set_content(message)
    try:
        with smtplib.SMTP('smtp-mail.outlook.com', 587) as smtp:
            print("utils ....... send_notification ............")
            smtp.starttls()
            smtp.login(email_user, email_pass)
            print("after login send_notification........................")
            # smtp.send_message(msg)
    except Exception as e:
        print(e)