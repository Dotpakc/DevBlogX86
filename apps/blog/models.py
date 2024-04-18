from PIL import Image
from django.core.files import File
from io import BytesIO

from django.db import models
from django.contrib.auth.models import User

from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, Thumbnail, SmartCrop

from ckeditor.fields import RichTextField
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=True, blank=True, default=None)
        
    title = models.CharField(max_length=100)
    content = CKEditor5Field('Text', config_name='extends')

    image = ProcessedImageField(
        upload_to='posts',
        processors=[ ResizeToFill(800, 400),
                    SmartCrop(800, 400)],
        format='JPEG',
        options={'quality': 60},
        )
    thumbnail = ImageSpecField(
        source='image',
        processors=[Thumbnail(400, 200)],
        format='JPEG',
        options={'quality': 60})
    like = models.ManyToManyField(User, related_name='like_posts', blank=True)
    tags = TaggableManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 


    class Meta:
        ordering = ['-created_at']
        
    
    
    def get_thumbnail(self):
        return self.thumbnail.url
    
    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return 'https://via.placeholder.com/800x400.jpg'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # recursive comment reply system
    # parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    
    like = models.ManyToManyField(User, related_name='like_comments', blank=True)

    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.content