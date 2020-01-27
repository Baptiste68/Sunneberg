from django.core.files.storage import FileSystemStorage
from django.db import models
from django.conf import settings


class Site(models.Model):
    img_name = models.CharField(max_length=200, blank=True)
    img_img = models.ImageField()
    
    def __str__(self):
        return self.img_name
