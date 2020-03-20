"""
Module to manage the models
used by the project
"""
from django.contrib.postgres.fields import ArrayField
from django.db import models


class SiteImage(models.Model):
    """
    Images used and stocked in db
    """
    img_name = models.CharField(max_length=200, blank=True)
    img_img = models.ImageField()

    def __str__(self):
        return self.img_name


class SiteText(models.Model):
    """
    Text used and stock in db
    """
    txt_name = models.CharField(max_length=200, blank=True)
    txt_title = models.CharField(max_length=200, blank=True)
    txt_text = models.TextField(max_length=4000, blank=True)

    def __str__(self):
        return self.txt_name


class ListModel(models.Model):
    """
    List used and stock in db
    """
    list_name = models.CharField(max_length=200)
    list_content = ArrayField(
        ArrayField(
            models.CharField(max_length=200, blank=True),
        ),
    )

    def __str__(self):
        return self.list_name


class PdfModel(models.Model):
    """
    Pdf used and stock in db
    """
    pdf_name = models.CharField(max_length=200)
    pdf_file = models.FileField()
    pdf_title = models.TextField(blank=True)

    def __str__(self):
        return self.pdf_name


class UnsubModel(models.Model):
    """
    For unsubscribtion in NewsLetter
    """
    unsub_email = models.CharField(max_length=200)
    unsub_code = models.IntegerField()
    unsub_duration = models.DurationField()

    def __str__(self):
        return self.unsub_email


class DictModel(models.Model):
    """
    Dictionary used and stock in db
    """
    dict_name = models.CharField(max_length=200)
    dict_content = ArrayField(
        ArrayField(
            models.CharField(max_length=200, blank=True),
        ),
    )

    def __str__(self):
        return self.dict_name
