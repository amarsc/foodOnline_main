from base64 import urlsafe_b64decode
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages ,auth
from django.template.defaultfilters import slugify

from accounts.forms import UserForm
from accounts.utils import detectUser,send_verification_email
from vendor.forms import VendorForm
from .models import User, UserProfile
from .utils import detectUser,send_verification_email,sendActivation_mail,send_password_reset_email
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from vendor.models import Vendor
from django.core.exceptions import PermissionDenied

# Create your views here.

def check_role_vendor(user):
    if user.role==1:
        return True
    else:
        raise PermissionDenied
    
def check_role_customer(user):
    if user.role ==2:
        return True
    else:
        raise PermissionDenied

def registeruser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'you are already logged in')
        return redirect('myAccount')
    # elif request.method =='POST':
    elif request.method=='POST':
        form=UserForm(request.POST)

        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role=User.CUSTOMER
            user.save()
            
            # send verification email
            email_subject= "Please activate your account"
            email_template= 'accounts/emails/account_verification_email.html'
            sendActivation_mail(request,user,email_subject,email_template)
            
            messages.info(request, "Your account has been registered successfully!")
            # print("user is created")
            return redirect('registeruser')
        else:
            print("invalid form")
            print(form.errors)
    else:
        form=UserForm()  
    context={
        'form':form,
    }
    return render(request,'accounts/registerUser.html', context)

def registerVendor(request): 
    if request.user.is_authenticated:
        messages.warning(request, 'you are already logged in')
        return redirect('myAccounnt')
    elif request.method =='POST':
    # if request.method == "POST":
        #Store Data
        form=UserForm(request.POST)
        v_form=VendorForm(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role=User.VENDOR
            user.save()
            vendor=v_form.save(commit=False)
            vendor.user=user
            vendor_name = v_form.cleaned_data['vendor_name']
            vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)
            user_profile=UserProfile.objects.get(user=user)
            vendor.user_profile=user_profile
            vendor.save()
            # send verification email
            
            email_subject= "Please activate your account"
            email_template= 'accounts/emails/account_verification_email.html'
            sendActivation_mail(request,user,email_subject,email_template)
            # send_verification_email(request,user)
            messages.success(request,'your restaurant has been registered successfully ! pls wait for approval')
            messages.info(request, "Your vendor has been registered successfully!")
            print("vendor is created")
            return redirect('registerVendor')
            
        else:
            print("invalid form")
            print(form.errors)        
        
    else:                    
        form=UserForm()
        v_form=VendorForm()
    context={
        'form':form,
        'v_form': v_form, 
    }
    return render(request,'accounts/registerVendor.html',context)

def activate(request, uidb64,token):
    # print("inside Activation...................")
    #Activate the user by setting the is_activate status is True
    try:
        
        uid=urlsafe_base64_decode(uidb64).decode()
        # print("uid...........",uid)
        user=User._default_manager.get(pk=uid)
        # print("user..............",user)
        # print("inside try...", uid  ,"  user: ",user)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist) as e:
        print(e)
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        # print("before is acticate.................")
        user.is_active=True
        user.save()
        messages.success(request,'Congratualations your account is activated...')
        return redirect('myAccount')
    else:
        messages.error(request,"invalid activation link")
        return redirect('myAccount')
    
def login(request):  
    if request.user.is_authenticated:
        messages.warning(request, 'you are already logged in')
        return redirect('myAccount')
    elif request.method =='POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user= auth.authenticate(email=email , password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request,'You are now logged in.')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request,'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'you are logged out')
    return redirect('login')

def dashboard(request):
    # print("inside dashboard...............................................")
    return render(request,'accounts/dashboard.html')

@login_required(login_url='login')
def myAccount(request):
    user=request.user
    redirectUrl=detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
def custDashboard(request):
    # print("inside custDashboard...............................................")
    return render(request,'accounts/custDashboard.html')


@login_required(login_url='login')
def vendorDashboard(request):
    # print("inside vendorDashboard...............................................")
    return render(request,'accounts/vendorDashboard.html')

def forgot_password(request):
    if request.method == 'POST':
        email=request.POST['email']
        if User.objects.filter(email=email).exists():
            user= User.objects.get(email__exact=email)
            # send reset password email
            email_subject="Reset your Password"
            email_template= 'accounts/emails/reset_password_email.html'
            print("email_subject...",email_subject,"email_template....",email_template)
            sendActivation_mail(request,user,email_subject,email_template)
            messages.success(request, "password change link has been sent to your email address")
            return redirect('login')
        else:
            messages.error(request,'Account does not exist')
            return redirect('forgot_password')
            
    return render(request,'accounts/forgot_password.html')

def reset_password_validate(request, uidb64, token):
    # validate the user by decoding  the token and user pk
    try:
        
        uid=urlsafe_base64_decode(uidb64).decode()
        # print("uid...........",uid)
        user=User._default_manager.get(pk=uid)
        # print("user..............",user)
        # print("inside try...", uid  ,"  user: ",user)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist) as e:
        print(e)
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        # print("before is activate.................")
        request.session['uid']=uid
        messages.info(request, 'pls reset your password')
        user.save()
        # messages.success(request,'Congratualations your account is activated...')
        return redirect('reset_password')
    else:
        messages.error(request,"link has been expired.")
        return redirect('myAccount')


def reset_password(request):
    if request.method=='POST':
        
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password == confirm_password: 
            pk=request.session.get('uid')
            user=User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active=True
            user.save()
            messages.success(request,'Password reset successfully')
            return redirect('login')
        else:
            messages.error(request,"password do not match!")
            return redirect('reset_password')
    
    return render(request, 'accounts/reset_password.html')