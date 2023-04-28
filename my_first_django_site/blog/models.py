from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from django.conf import settings

# Create your models here.
class Category(models.Model):
    
    name = models.CharField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blog_categories', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        
        return self.name

class Post(models.Model):

    class PostStatus(models.TextChoices):

        DRAFT = "draft", _('DRAFT')
        PUBLISHED = "published", _('Published')

    tags = TaggableManager()
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blog_posts', on_delete=models.CASCADE)
    body = models.TextField()
    category = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=PostStatus.choices, default=PostStatus.DRAFT)
    image = models.ImageField(upload_to='blog/', null=True, default=None)

    class Meta:

        ordering = ('-publish',)

    def __str__(self):

        return self.title
    
    def get_absolute_url(self):

        return reverse('blog:post_detail', args=[str(self.id)])

class Comment(models.Model):
    
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        
        ordering = ('created',)

    def __str__(self):
        
        return 'Comment by {} on {}'.format(self.name, self.post)