from django.db import models

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill, SmartCrop

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    avatar = ProcessedImageField(
        upload_to='posts',
        processors=[ ResizeToFill(200, 200)],
        format='JPEG',
        options={'quality': 60},
        blank=True,
        null=True)
    
    
    def __str__(self):
        return self.user.username