from django.db import models
from django.utils import timezone

from users.models import User



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
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    garage = models.IntegerField(default=0)
    area = models.FloatField()
    photo_main = models.ImageField(upload_to='listings')
    photo_1 = models.ImageField(upload_to='listings', blank=True, null=True)
    photo_2 = models.ImageField(upload_to='listings', blank=True, null=True)
    photo_3 = models.ImageField(upload_to='listings', blank=True, null=True)
    photo_4 = models.ImageField(upload_to='listings', blank=True, null=True)
    status = models.SmallIntegerField(max_length=5, choices=STATUS_CHOICES)
    video = models.FileField(upload_to='listings/video', blank=True, null=True)
    vr_image = models.ImageField(pload_to='listings/vr')
    slug = models.SlugField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL)
    # location fileds for maps
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    type = models.SmallIntegerField(max_length=5, choices=TYPE_CHOICES)
    date = models.DateTimeField(default=timezone.now, blank=True)
    availability = models.SmallIntegerField(max_length=15, choices=AttributeError)
    views = models.BigIntegerField()
    reference = models.CharField(max_length=50)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
   
    def __str__(self):
        return self.title

    def get_address(self):
        pass    


# class WishList(models.Model):
#     pass