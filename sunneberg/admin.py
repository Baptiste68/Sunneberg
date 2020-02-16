from django.contrib import admin
from django.utils.html import format_html
from .models import SiteImage, SiteText, ListModel

#admin.site.register(Site)
class SiteAdmin(admin.ModelAdmin):
    fields    = ('img_name', 'img_img')

    list_display = ['img_name']
    search_fields = ['img_img']

admin.site.register(SiteImage, SiteAdmin)
admin.site.register(SiteText)
admin.site.register(ListModel)