from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from profiles.models import Profile
from profiles.forms import UserRegistrationForm,LoginForm

from datetime import datetime, timedelta
import uuid
import subprocess
import os
import json

# Create your views here.

def create_mail_message(unique_id):
    url=f'http://localhost:8000/profiles/email_confirmation?id={unique_id}'
    message=f"Merci de nous avoir rejoint. Cliquez sur le lien ci-dessous pour valider votre compte :{url}"
    return message

def create_unique_identifier(current_date_str, email):
    # Convert the input string to a datetime object
    current_date = datetime.strptime(current_date_str, '%Y-%m-%d %H:%M:%S')
    
    # Add 24 hours to the current date
    updated_date = current_date + timedelta(hours=24)
    # Create a unique identifier
    unique_id = f"{updated_date.strftime('%Y%m%d%H%M%S')}_{email}_{uuid.uuid4()}"
    
    return unique_id

def parse_unique_identifier(unique_id):
    # Split the unique_id into its components
    try:
        date_str, email, unique_id = unique_id.split('_')
        
        # Convert the date string back to a datetime object
        date = datetime.strptime(date_str, '%Y%m%d%H%M%S')
        
        return date, email, unique_id
    except ValueError:
        print("Invalid unique identifier format.")
        return None

def check_datetime(date_obj):
    current_time = datetime.now()
    if date_obj >= current_time:
        return False
        
    time_difference = current_time - date_obj
    return time_difference.total_seconds() < 24 * 3600

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def registration(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            


            # generate id email confirmation
            formatted_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            unique_id = create_unique_identifier(formatted_date_time, user_form.cleaned_data['email'].replace('.','-'))
            message=create_mail_message(unique_id=unique_id)
            
            # putting the unique id in the db

            print('\n ************ \n')
            unique_id_value=unique_id.split('_')[-1]
            print(unique_id_value)
            print(type(unique_id_value) is str)
            print('\n ************ \n')

            #create profile and put the unique id in the profile
            Profile.objects.create(user=new_user,unique_id=unique_id.split('_')[-1])

            send_mail(
                'Confirmez votre compte email et validez votre compte',
                message,
                'from@yourdjangoapp.com',
                [user_form.cleaned_data['email']],
                fail_silently=False,
            )
            return render(request,'profiles/register_confirm_email_sent.html')
    else:
        user_form = UserRegistrationForm()
    
    context={
        'user_form':user_form,
    }

    return render(
        request,
        'profiles/registration.html',
        context
    )

@login_required
def dashboard_user(request):
    return render(request,'profiles/dashboard_user.html')


def email_confirmation_view(request):
    print(request.GET['id'])
    date,email,unique_id=parse_unique_identifier(request.GET['id'])
    profile=Profile.objects.filter(unique_id=unique_id,user__email__icontains=email.replace('-','.'))
    
    msg='Ca n\'a pas marche -..-'
    
    if profile.exists:
        print('\n\n *************')
        
        print(f'date {date} email {email} id {unique_id}')
        print(f'unique id : {unique_id}')
        print(profile.values_list('user',flat=True).first())
        
        user_obj=User.objects.get(id=profile.values_list('user',flat=True).first())
        print(user_obj.username)
        print(user_obj.password)
        
        if user_obj is not None:
            user=authenticate(request,user_obj=user_obj)
            if user.is_active:
                login(request, user)
                msg='Félicitations, votre compte a été activé.'
            else:
                msg='Oups something went wrong :-(0) '
        else:
            msg='Invalid login'
    else:
        msg='Profile do not exist'
    # HANDLE UNIQUE FOR VERIFICATION HERE
    return render(request,'profiles/register_mail_confirmed.html',{'message':msg})

