from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from profiles.models import Profile

class LoginForm(forms.Form):
    username=forms.CharField(label="Nom d'utilisateur")
    password=forms.CharField(label="Mot de passe",widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Mot de passe',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Répétez le mot de passe',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']
        labels={
            'username':_('Nom d\'utilisateur'),
            'email':_('Email')
        }
        help_texts={
            'username':"Requis. 150 caractères ou moins. Lettres, chiffres et @/./+/-/_ uniquement.",
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Les mots de passe ne correspondent pas.')
        return cd['password2']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email déjà utilisé.')
        return data

    def clean_username(self):
        data=self.cleaned_data['username']
        qs=User.objects.filter(username=data)
        if qs.exists():
            raise forms.ValidationError('Nom d\'utilisateur déjà utilisé')
        return data

class ProfileRegistrationForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=["phone","date_of_birth","address"]
        labels={
            'phone':_('Téléphone'),
            'date_of_birth':_('Date de naissance'),
            'address':_('Addresse')
        }

class UserEditForm(forms.ModelForm):
    class Meta:
        model=User
        fields=("first_name","last_name","username","email")
        labels={
            'first_name':_('Prénom'),
            'last_name':_('Nom de famille'),
            'username':_('Nom d\'utilisateur'),
            'email':_('Email'),
        }
    
    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Email déjà utilisé.')
        return data

    def clean_username(self):
        data=self.cleaned_data['username']
        qs=User.objects.exclude(id=self.instance.id).filter(username=data)
        if qs.exists():
            raise forms.ValidationError('Nom d\'utilisateur déjà utilisé')
        return data
