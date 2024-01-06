from django.db import models
from django.conf import settings
# from django.urls import reverse
from django.contrib.auth.models import AbstractUser



## models fo notes

class CustomUser(AbstractUser):
    bio = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username
    

class Note(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='notes')
    title = models.CharField(max_length=100, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    shared_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_notes')

    def __str__(self):
        return self.title

