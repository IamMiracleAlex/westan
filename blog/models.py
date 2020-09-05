from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify

from taggit.managers import TaggableManager

from users.models import User



class Post(models.Model):

    DRAFT, PUBLISH = 0, 1
    status_choices = ((DRAFT, 'Draft'),
                    (PUBLISH, 'Publish'))

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=250, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.SmallIntegerField(default=DRAFT, choices=status_choices)
    image = models.ImageField(upload_to='blog', blank=True, null=True)  
    views = models.BigIntegerField(default=0)                          

    tags = TaggableManager()                                                  

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:single", args=[self.pk, self.slug])

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     body = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     active = models.BooleanField(default=False)

#     class Meta:
#         ordering = ('created_at',)

#     def __str__(self):
#         return f'Comment by {self.name} on {self.post}'  
    pass                                                                         
