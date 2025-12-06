from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    online_status = models.BooleanField(default=False)
    last_seen = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class ChatRoom(models.Model):
    ROOM_TYPES = [
        ('one_on_one', 'One-on-One'),
        ('group', 'Group'),
    ]
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        if self.room_type == 'group':
            return self.room_name or f'Group Chat {self.id}'
        else:
            participants = list(self.participants.all())
            if len(participants) == 2:
                return f'{participants[0].email} - {participants[1].email}'
            return f'Chat Room {self.id}'

class Message(models.Model):
    MESSAGE_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('file', 'File'),
    ]
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='text')
    file_url = models.URLField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['chat_room']),
        ]

    def __str__(self):
        return f'{self.sender.email}: {self.content[:50]}'

    @staticmethod
    def get_unread_count(user, chat_room):
        return Message.objects.filter(chat_room=chat_room, is_read=False).exclude(sender=user).count()
