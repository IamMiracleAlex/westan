from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from taggit.managers import TaggableManager

from users.models import User
from utils.handlers import image_resizer


class Post(models.Model):

    DRAFT, PUBLISHED = 0, 1
    status_choices = ((DRAFT, 'Draft'),
                    (PUBLISHED, 'Published'))

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=250, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.SmallIntegerField(default=DRAFT, choices=status_choices)
    image = models.ImageField(upload_to='blog', null=True)  
    views = models.BigIntegerField(default=0)  
    featured = models.BooleanField(default=False, help_text='Whether post should appear on slide')                        

    tags = TaggableManager()                                                  

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:blog_single", args=[self.pk, self.slug])

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)

        if self.image:    
            image_resizer(self.image)
            
        super().save(*args, **kwargs)

                                                                    
