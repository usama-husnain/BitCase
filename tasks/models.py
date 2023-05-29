from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField(null=True)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=200, validators=[MinLengthValidator(2)])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
