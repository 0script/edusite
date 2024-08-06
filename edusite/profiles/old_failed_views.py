from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.mail import send_mail

from profiles.models import Profile
from profiles.forms import UserRegistrationForm

from datetime import datetime, timedelta
import uuid
import subprocess
import os
import json

# Create your views here.

def create_mail_message(unique_id):
    url=f'http://localhost:8000/profile/email_confirmation?id={unique_id}'
    message=f"Merci de nous avoir rejoint. Cliquez sur le lien ci-dessous pour valider votre compte :{url}"
    return message


def create_json_file(destination, subject, message):
    # Create the subdirectory if it does not exist
    subdirectory = 'profiles/send_gmail/'
    print('\n The dir \n')
    print(os.getcwd())
    print('\n')
    if not os.path.exists(subdirectory):
        return print(f'Dir do not exist :{subdirectory}')

    # Prepare the data to be written to the JSON file
    data = {
        'destination': destination,
        'subject': subject,
        'message': message
    }
    
    # Define the file path
    file_path = os.path.join(subdirectory, 'email.json')
    
    # Write the data to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    print(f"JSON file created at {file_path}")

def create_unique_identifier(current_date_str, email):
    # Convert the input string to a datetime object
    current_date = datetime.strptime(current_date_str, '%Y-%m-%d %H:%M:%S')
    
    # Add 24 hours to the current date
    updated_date = current_date + timedelta(hours=24)
    # Create a unique identifier
    unique_id = f"{updated_date.strftime('%Y%m%d%H%M%S')}_{email}_{uuid.uuid4()}"
    
    return unique_id

def registration(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # new_user = user_form.save(commit=False)
            # new_user.set_password(user_form.cleaned_data['password'])
            # new_user.save()
            # Profile.objects.create(user=new_user)


            # generate id email confirmation
            formatted_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            unique_id = create_unique_identifier(formatted_date_time, user_form.cleaned_data['email'].replace('.','-'))
            messsage=create_mail_message(unique_id=unique_id)

            # print('\n')
            # print(messsage)
            # print('\n')
            
            # create_json_file(user_form.cleaned_data['email'], 'Confirmez votre compte email et validez votre compte', message=messsage)
            # subprocess.call('cd profiles/send_gmail/; python3 send_email.py', shell=True)

            #,{'new_user': new_user}
            
            send_mail(
                'That’s your subject',
                'That’s your message body',
                'from@yourdjangoapp.com',
                ['to@yourbestuser.com'],
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

# def email_confirmation_view(request,code):
    