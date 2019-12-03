from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


# Create your models here.

class User(AbstractUser):
    TITLES = (
        ('1', 'MR'),
        ('2', 'MRS'),
        ('3', 'MISS')
    )
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    CATERGORIES = (
        ('SAE', 'Salary Earner'),
        ('BO', 'Business Owner'),
        ('CO', 'Corper')
    )
    title = models.CharField(max_length=100, choices=TITLES, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, blank=True)
    category = models.CharField(max_length=50, choices=CATERGORIES, blank=True)


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=300)
    phone = models.CharField(max_length=15)
    status = models.CharField(max_length=100)
    identification = models.FileField(max_length=500)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    email_confirmed = models.BooleanField(default=False)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    has_full_profile = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
