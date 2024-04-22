from django import forms

from .models import Post

from django_ckeditor_5.widgets import CKEditor5Widget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'tags')
        # widgets = {
        #     'content': CKEditor5Widget(
        #     attrs={"class": "django_ckeditor_5", "config_name": "extends"})
        # }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].required = False
        
        
class CommentForm(forms.Form):
    content = forms.CharField(min_length=6,max_length=200)
