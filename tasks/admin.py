from django.contrib import admin
from .models import Task, Post

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'desc')  # Customize the displayed fields
    list_filter = ('title',)  # Add filtering options
    # search_fields = ('title')  # Enable search functionality

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content')  # Customize the displayed field
   