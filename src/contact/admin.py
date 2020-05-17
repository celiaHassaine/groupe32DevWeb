from django.contrib import admin
from .models import Horaire, Contact, Adresse
# Register your models here.

admin.site.register(Adresse)
admin.site.register(Horaire)
admin.site.register(Contact)