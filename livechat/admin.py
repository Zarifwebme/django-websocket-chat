from django.contrib import admin
from .models import Room, Message


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "username", "short_content", "created_at")
    list_filter = ("room", "created_at")
    search_fields = ("username", "content")

    def short_content(self, obj):
        return obj.content[:50]