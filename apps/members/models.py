import uuid

from django.db import models

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill, SmartCrop

# urls reverse
from django.urls import reverse

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
        

class Notification(models.Model):
    NOTIFICATION_TYPE = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # uuid - це унікальний ідентифікатор
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE)
    profile = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    url = models.URLField(max_length=200, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
   
    class Meta:
        ordering = ['-created_at']
   
   
    def __str__(self):
        return self.notification_type
    
    def get_icon(self):
        if self.notification_type == 'like':
            return 'heart'
        elif self.notification_type == 'comment':
            return 'comment'
        elif self.notification_type == 'follow':
            return 'user-friends'
        
    def add_like(self, post, author_like):
        self.notification_type = 'like'
        self.profile = post.author
        self.message = '{} liked your post'.format(author_like.username)
        self.url = reverse('blog:detail', args=[post.pk])
        self.save()
        
    def add_comment(self, post, author_comment):
        self.notification_type = 'comment'
        self.profile = post.author
        self.message = '{} commented on your post'.format(author_comment.username)
        self.url = reverse('blog:detail', args=[post.pk])
        self.save()
        
    def add_follow(self, profile, author_follow):
        self.notification_type = 'follow'
        self.profile = profile
        self.message = '{} started following you'.format(author_follow.username)
        self.url = reverse('members:profile', args=[author_follow.profile.pk])
        self.save()
        
    def read(self):
        self.is_read = True
        self.save()
        
        
    