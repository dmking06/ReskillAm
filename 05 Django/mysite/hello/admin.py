from django.contrib import admin

# Register your models here.
from .models import Label, Data

admin.site.register(Label)
admin.site.register(Data)
