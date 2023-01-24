from django import forms 
from .models import Post 

class PostCreationForm(forms.ModelForm):
    tags = forms.CharField(max_length=20)
    class Meta:
        model = Post 
        fields = ["title", "content", "image"]

        