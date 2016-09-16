from django.contrib import admin
from .models import User
from .models import Tools
from .models import Shed, Notifications
# Register your models here.
admin.site.register(User)
admin.site.register(Tools)
admin.site.register(Shed)
admin.site.register(Notifications)