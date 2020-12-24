from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.tools import generate_unique_id
from users.managers import CustomUserManager
from utils.handlers import image_resizer


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='email address', unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_marketer = models.BooleanField(default=False)
    refer_code = models.CharField(
        max_length=15,
        unique=True,
        editable=False,
    )
    referer = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='referrals'
    )
    next_of_kin = models.CharField(max_length=50, null=True, blank=True)
    send_notifications = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='users', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return "{} {} - {}".format(self.first_name, self.last_name, self.email)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.refer_code = generate_unique_id(User, 'refer_code')
            
        image_resizer(self.image)    

        super(User, self).save(*args, **kwargs)


class Subscribe(models.Model):

    email = models.EmailField(max_length=100)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        verbose_name_plural = "Subscribers"

    def __str__(self):
        return self.email