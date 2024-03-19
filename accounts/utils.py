from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

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
    
    
# def send_verification_email(request,user):
#     current_site=get_current_site(request)
#     mail_subject="Please activate your account"
#     message= render_to_string('accounts/emails/account_verification_email.html', {
#         'user' : user,
#         'domain': current_site,
#         'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
#         'token':default_token_generator.make_token(user)
#     })
#     to_email= 'vivekchauhan14@hotmail.com'  #user.email
#     mail= EmailMessage(mail_subject,message, to=[to_email])
#     mail.send()
    

def send_activation_email(request,user, email_subject, email_template):  
    msg = EmailMessage()
    msg['Subject'] = email_subject
    msg['From'] = 'vivekchauhan14@hotmail.com'
    msg['To'] = ', '.join([user.email,])
    message= render_to_string(email_template, {
        'user' : user,
        'domain': '127.0.0.1:8000',
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user)
    })
    print("Activation email content ************* : ",message)
    msg.set_content(message)
    try:
        with smtplib.SMTP('pod51000.outlook.com', 587) as smtp:
            smtp.starttls()
            smtp.login('vsc1404@outlook.com', 'Adarsh@0103')
            # smtp.send_message(msg)
            print('activation email sent successfully !!',msg)
    except Exception as e:
        print('activation email sending failed !!', e)    
        
        
def send_notification(mail_subject, mail_template, context):
    msg = EmailMessage()
    msg['Subject'] = mail_subject
    msg['From'] = settings.DEFAULT_FROM_EMAIL
    msg['To'] = context['user'].email
    message= render_to_string(mail_template, context)
    print("Activation email content ************* : ",message)
    msg.set_content(message)
    try:
        with smtplib.SMTP('pod51000.outlook.com', 587) as smtp:
            smtp.starttls()
            smtp.login('vivekchauhan14@hotmail.com.com', 'Adarsh@0103')
            print("============> : ",msg)
            # smtp.send_message(msg)
            print('activation email sent successfully !!')
    except Exception as e:
        print('activation email sending failed !!', e)    
    