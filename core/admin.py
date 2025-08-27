from django.contrib import admin
from .models import MyUser , EmailOpt
# Register your models here.
admin.site.register(MyUser)

admin.site.register(EmailOpt)