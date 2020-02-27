from django.core.files.storage import FileSystemStorage
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.conf import settings
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.utils.decorators import method_decorator


class SiteImage(models.Model):
    img_name = models.CharField(max_length=200, blank=True)
    img_img = models.ImageField()
    
    def __str__(self):
        return self.img_name

class SiteText(models.Model):
    txt_name = models.CharField(max_length=200, blank=True)
    txt_title = models.CharField(max_length=200, blank=True)
    txt_text = models.TextField(max_length=4000, blank=True)

    def __str__(self):
        return self.txt_name
 
class ListModel(models.Model):
    list_name = models.CharField(max_length=200)
    list_content = ArrayField(
        ArrayField(
            models.CharField(max_length=200, blank=True),
        ),
    )

    def __str__(self):
        return self.list_name

class PdfModel(models.Model):
    pdf_name = models.CharField(max_length=200)
    pdf_file = models.FileField()
    pdf_title = models.TextField(blank=True)

    def __str__(self):
        return self.pdf_name 

class UnsubModel(models.Model):
    unsub_email = models.CharField(max_length=200)
    unsub_code = models.IntegerField()
    unsub_duration = models.DurationField()

    def __str__(self):
        return self.unsub_email