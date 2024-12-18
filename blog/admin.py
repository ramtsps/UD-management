from django.contrib import admin

from .models import Contact, UserData

# Register your models here.
admin.site.register(Contact)
admin.site.register(UserData)