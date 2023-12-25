# models.py
from django.db import models
from django.conf import settings
from social_django.models import UserSocialAuth

class PublicChatRoom(models.Model):
    title = models.CharField(max_length=255, unique=True, blank=False)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, help_text="Users who are connected to the chat")

    def __str__(self):
        return self.title
    
    def connect_user(self, user):
        # Return True if the user is added to the users list

        is_user_added = False
        user_uid = user.social_auth.get(provider='google-oauth2').uid

        if not self.users.filter(social_auth__uid=user_uid).exists():
            self.users.add(user)
            self.save()
            is_user_added = True

        return is_user_added
    
    def disconnect_user(self, user):
        # Return True if the user is removed from the users list

        is_user_removed = False
        user_uid = user.social_auth.get(provider='google-oauth2').uid

        if self.users.filter(social_auth__uid=user_uid).exists():
            self.users.remove(user)
            self.save()
            is_user_removed = True

        return is_user_removed
    
    @property
    def group_name(self):
        # Return channels group name
        return f"PublicChatRoom-{self.id}"

class PublicChatMessageManager(models.Manager):
    def by_room(self, room):
        qs = PublicRoomChatMessage.objects.filter(room=room).order_by("-timestamp")
        return qs

class PublicRoomChatMessage(models.Model):
    # Chat message created by a user inside a PublicChatRoom (foreign key)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(PublicChatRoom, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(unique=False, blank=False)

    objects = PublicChatMessageManager()

    def __str__(self):
        return self.content
