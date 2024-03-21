from PIL import Image
from django.core.files import File
from io import BytesIO

from django.db import models
from django.contrib.auth.models import User

from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, Thumbnail, SmartCrop



# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=True, blank=True, default=None)
        
    title = models.CharField(max_length=100)
    content = models.TextField()

    image = ProcessedImageField(
        upload_to='posts',
        processors=[ ResizeToFill(800, 400),
                    SmartCrop(800, 400)],
        format='JPEG',
        options={'quality': 60})
    thumbnail = ImageSpecField(
        source='image',
        processors=[Thumbnail(400, 200)],
        format='JPEG',
        options={'quality': 60})
    like = models.ManyToManyField(User, related_name='like_posts', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 


    class Meta:
        ordering = ['-created_at']
        
    
    
    def get_thumbnail(self):
        return self.thumbnail.url
