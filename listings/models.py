from django.db import models
from django.utils import timezone


class Listing(models.Model):
    
    # title = models.CharField(max_length=50)
    # address = models.CharField(max_length=200)
    # city = models.CharField(max_length=40)
    # state = models.CharField(max_length=40)
    # zipcode = models.CharField(max_length=20)
    # description = models.TextField(blank=True)
    # price = models.IntegerField()
    # bedrooms = models.IntegerField()
    # bathrooms = models.DecimalField(max_digits=2, decimal_places=1)
    # garage = models.IntegerField(default=0)
    # sqft = models.IntegerField()
    # lot_size = models.DecimalField(max_digits=5, decimal_places=1)
    # photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    # photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
    # photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
    # photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
    # photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
    # status = models.SmallIntegerField()
    # date = models.DateTimeField(default=timezone.now)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    
   
    def __str__(self):
        return self.title
