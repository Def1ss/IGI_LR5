from django.contrib import admin
from .models import Client, Instructor, ClubCard

admin.site.register(Client)
admin.site.register(Instructor)
admin.site.register(ClubCard)