from django.db import models
from django.utils import timezone

from users.models import User
from utils.tools import generate_unique_id



class Listing(models.Model):

    DRAFT, PUBLISHED = 0, 1 
    STATUS_CHOICES = [(DRAFT, 'Draft'), (PUBLISHED, 'Published')]

    HOUSE, LAND = 0, 1 
    TYPE_CHOICES = [(HOUSE, 'House'), (LAND, 'Land')]

    SOLD, AVAILABLE, LEASED = 0, 1, 2
    AVAILABILITY_CHOICES = [(SOLD, 'Sold'), (AVAILABLE, 'Available'), (LEASED, 'Leased')]   
    
    title = models.CharField(max_length=50)
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=40)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    bedrooms = models.IntegerField(blank=True, null=True)
    bathrooms = models.IntegerField(blank=True, null=True)
    garage = models.IntegerField(blank=True, null=True)
    area = models.FloatField()
    photo_main = models.ImageField(upload_to='listings')
    photo_1 = models.ImageField(upload_to='listings', blank=True, null=True)
    photo_2 = models.ImageField(upload_to='listings', blank=True, null=True)
    photo_3 = models.ImageField(upload_to='listings', blank=True, null=True)
    photo_4 = models.ImageField(upload_to='listings', blank=True, null=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=DRAFT)
    video = models.FileField(upload_to='listings/video', blank=True, null=True)
    vr_image = models.ImageField(upload_to='listings/vr', blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    # author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # location fileds for maps
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    type = models.SmallIntegerField(choices=TYPE_CHOICES, default=HOUSE)
    availability = models.SmallIntegerField(choices=AVAILABILITY_CHOICES, default=AVAILABLE)
    views = models.BigIntegerField(default=0)
    reference = models.CharField(max_length=50, blank=True, null=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
   
    def __str__(self):
        return self.title

    def get_address(self):
        pass    

    def get_absolute_url(self):
        return reverse("blog:blog_single", args=[self.pk, self.slug])

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.refer_code = generate_unique_id(User, 'refer_code')
        super(User, self).save(*args, **kwargs)

# class WishList(models.Model):
#     pass