from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    phone=models.CharField( max_length=15)
    address=models.CharField( max_length=50)
    photo = models.ImageField(upload_to='profil/%Y/%m/%d/',blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    unique_id=models.CharField(max_length=55,blank=True,null=True) 
    def __str__(self):
        return f'Profile of {self.user.username}'