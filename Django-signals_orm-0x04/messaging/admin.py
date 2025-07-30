from django.contrib import admin
from messaging.models import Conversation, User, Message, Notifications
# Register your models here.

admin.site.register(Conversation)
admin.site.register(User)
admin.site.register(Message)
admin.site.register(Notifications)