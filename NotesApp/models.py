from django.db import models
from django.conf import settings
# from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.search import SearchVectorField, SearchVector



## models fo notes

class CustomUser(AbstractUser):
    bio = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username
    

class Note(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='notes')
    title = models.CharField(max_length=100, null=True, blank=True)
    # cover_image = models.ImageField(upload_to='images/', null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    search_vector = SearchVectorField(null=True)
    # is_public = models.BooleanField(default=False)
    shared_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_notes')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
        self.search_vector = vector
        self.save()


    def __str__(self):
        return self.title

