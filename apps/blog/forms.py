from django import forms

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image')
        
        
class CommentForm(forms.Form):
    content = forms.CharField(min_length=6,max_length=200)
