from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from utils.tools import generate_unique_id
from users.models import User



class Listing(models.Model):

    DRAFT, PUBLISHED = 0, 1 
    STATUS_CHOICES = [(DRAFT, 'Draft'), (PUBLISHED, 'Published')]

    HOUSE, LAND = 0, 1 
    TYPE_CHOICES = [(HOUSE, 'House'), (LAND, 'Land')]

    SOLD, AVAILABLE, LEASED = 0, 1, 2
    AVAILABILITY_CHOICES = [(SOLD, 'Sold'), (AVAILABLE, 'Available'), (LEASED, 'Leased')]   
    
    title = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=40)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    bedrooms = models.IntegerField(blank=True, null=True)
    bathrooms = models.IntegerField(blank=True, null=True)
    garage = models.IntegerField(blank=True, null=True)
    area = models.FloatField()
    image = models.ImageField(verbose_name='Main Image', upload_to='listings/img')
    image_1 = models.ImageField(upload_to='listings/img', blank=True, null=True)
    image_2 = models.ImageField(upload_to='listings/img', blank=True, null=True)
    image_3 = models.ImageField(upload_to='listings/img', blank=True, null=True)
    image_4 = models.ImageField(upload_to='listings/img', blank=True, null=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=DRAFT)
    video = models.FileField(upload_to='listings/video', blank=True, null=True)
    vr_image = models.ImageField(upload_to='listings/vr', blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    # location fileds for maps
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
        return f'{self.street}, {self.city}, {self.state}'    

    def get_absolute_url(self):
        return reverse("listings:single_lisitng", args=[self.pk, self.slug])

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
            self.reference = generate_unique_id(Listing, 'reference', len=10)

        super().save(*args, **kwargs)





class WishList(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)  
    listing = models.ForeignKey(Listing, models.DO_NOTHING)  
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.status}'
    