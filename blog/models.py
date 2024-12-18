from django.db import models

# Create your models here.
from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
# models.py
from django.db import models

class UserData(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)  # Store hashed password
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Add profile picture
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the registration time
    
    def __str__(self):
        return self.username
