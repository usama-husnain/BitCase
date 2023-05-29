from .models import Task, Post
from django import forms

class PostFormValidation(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['title', 'content']
        error_messages = {
            'title': {
                'required': 'Title field is required.',
                'min_length': 'Title length must be greater than 2.',
            },
            'content': {
                'required': 'Content field is required.',
                
            },
        }
