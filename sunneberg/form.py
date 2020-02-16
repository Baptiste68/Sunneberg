from django.core.files.storage import FileSystemStorage
from django.forms import ModelForm
from django.db import models
from django.conf import settings
from .models import SiteImage


class ImageForm(ModelForm):

    class Meta:
        model = SiteImage
        fields = ('img_img',)
