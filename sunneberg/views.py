import requests
import json
import logging

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic, View
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings

from .models import Site

logger = logging.getLogger(__name__)


class IndexView(View):
    """
        Class view for index
    """
    template_name = 'sunneberg/index.html'

    def get(self, request):
        """
        my_insert = Site(img_name="Appel_banner_img",
                         img_img="applejuice.jpg")
        print(my_insert)
        my_insert.save()"""
        farm = Site.objects.filter(img_name=settings.FARM)
        cows = Site.objects.filter(img_name=settings.COWS)
        appel = Site.objects.filter(img_name=settings.APPEL)
        grappes = Site.objects.filter(img_name=settings.GRAPPES)

        return render(request, self.template_name, {'cows': cows[0],
                                                    'farm': farm[0],
                                                    'appel': appel[0],
                                                    'grappes': grappes[0]})

class AboutusView(View):
    """
        Class view for about us section
    """
    template_name = 'sunneberg/aboutus.html'
    
    def get(self, request):
        return render(request, self.template_name)


class FarmingView(View):
    """
        Class view for pastoral farming section
    """
    template_name = 'sunneberg/farming.html'
    
    def get(self, request):
        return render(request, self.template_name)


class VineView(View):
    """
        Class view for vineyard section
    """
    template_name = 'sunneberg/vine.html'
    
    def get(self, request):
        return render(request, self.template_name)


class AppleView(View):
    """
        Class view for vineyard section
    """
    template_name = 'sunneberg/apple.html'
    
    def get(self, request):
        return render(request, self.template_name)

