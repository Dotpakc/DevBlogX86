from django.db import models

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill, SmartCrop

from ckeditor.fields import RichTextField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    bio = RichTextField(null=True, blank=True)
    avatar = ProcessedImageField(
        upload_to='posts',
        processors=[ ResizeToFill(200, 200)],
        format='JPEG',
        options={'quality': 60},
        blank=True,
        null=True)
    
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    
    def __str__(self):
        return self.user.username
    
    def follow(self, profile):
        self.followers.add(profile)
        
    def unfollow(self, profile):
        self.followers.remove(profile)
        
    def is_following(self, profile):#це функція, яка перевіряє чи підписаний користувач на іншого користувача
        return profile in self.followers.all()
    
    def get_followers(self): #це функція, яка повертає всіх користувачів, які підписані на користувача
        return self.followers.all()
    
    def get_following(self):#це функція, яка повертає всіх користувачів, на яких підписаний користувач
        return Profile.objects.filter(followers=self)
        # Profile.objects.filter(followers__in=[self])
    

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        else:
            return 'https://www.gravatar.com/avatar/{}?d=identicon'.format(self.user.username)