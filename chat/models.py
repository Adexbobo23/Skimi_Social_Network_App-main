from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Room(models.Model):
    # room_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, related_name='author_room', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend_room', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room_id}-{self.author}-{self.friend}"


class Chat(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='chats')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_msg')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_msg')
    text = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    has_seen = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' %(self.id, self.date)



from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    input_message = models.TextField()
    bot_response = models.TextField()

    # Other fields as per requirement

    def __str__(self):
        return f"Chat with {self.user.username} at {self.timestamp}"



from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Story(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    image_file = models.ImageField(upload_to='story_images/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        
        # Set expires_at 24 hours after created_at
        if self.created_at:
            self.expires_at = self.created_at + timezone.timedelta(hours=24)
        else:
            self.expires_at = timezone.now() + timezone.timedelta(hours=24)
        
        super(Story, self).save(*args, **kwargs)



