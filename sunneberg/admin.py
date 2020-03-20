"""
Module to manage the admin panel
form Django
"""
from django.contrib import admin
from .models import SiteImage, SiteText, ListModel, PdfModel, UnsubModel, DictModel

#admin.site.register(Site)
class SiteAdmin(admin.ModelAdmin):
    """
    This class to manage the images
    """
    fields = ('img_name', 'img_img')

    list_display = ['img_name']
    search_fields = ['img_img']

admin.site.register(SiteImage, SiteAdmin)
admin.site.register(SiteText)
admin.site.register(ListModel)
admin.site.register(PdfModel)
admin.site.register(UnsubModel)
admin.site.register(DictModel)
