from django.db import models

# Create your models here.
class EncryptedImage(models.Model):
    image = models.ImageField(upload_to='encrypted_images/')
    password = models.CharField(max_length=100)
    
    def __str__(self):
        return self.image.name