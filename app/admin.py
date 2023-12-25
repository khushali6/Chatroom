# app/admin.py
from django.contrib import admin
from .models import PublicChatRoom

class PublicChatRoomAdmin(admin.ModelAdmin):
    list_display=['id','title']
    search_fields=['id','title']

admin.site.register(PublicChatRoom, PublicChatRoomAdmin)
