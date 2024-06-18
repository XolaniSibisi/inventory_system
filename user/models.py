from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from phonenumber_field.modelfields import PhoneNumberField

# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()
    phone_number = PhoneNumberField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    is_supplier = models.BooleanField(default=False)
    

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)
        if img.height > 100 or img.width > 100:
            output_size = (100, 100)
            img.thumbnail(output_size)
            img.save(self.avatar.path)
