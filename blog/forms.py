from django import forms
from .models import Post
from django.core.exceptions import ValidationError

def validate_age(value):
    if value < 1 or value > 100:
        print("Error accurs")
        raise ValidationError("Age must be between 1 and 100")

class PostForm(forms.ModelForm):
    # age = forms.IntegerField(validators=[validate_age])

    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
