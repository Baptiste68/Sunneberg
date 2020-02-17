import requests
import json
import logging

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic, View
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages

from .models import SiteImage, SiteText, ListModel
from .forms import ImageForm, TextForm

logger = logging.getLogger(__name__)


class IndexView(View):
    """
        Class view for index
    """
    template_name = 'sunneberg/index.html'
    farm = SiteImage.objects.filter(img_name=settings.FARM)
    farm_txt = SiteText.objects.filter(txt_name=settings.FARM_TXT)
    cows = SiteImage.objects.filter(img_name=settings.COWS)
    cows_txt = SiteText.objects.filter(txt_name=settings.COWS_TXT)
    apple = SiteImage.objects.filter(img_name=settings.APPLE)
    apple_txt = SiteText.objects.filter(txt_name=settings.APPLE_TXT)
    grappes = SiteImage.objects.filter(img_name=settings.GRAPPES)
    grappes_txt = SiteText.objects.filter(txt_name=settings.GRAPPES_TXT)
    pfarminghome = SiteImage.objects.filter(img_name=settings.COWS_VIGNETTE)
    grappeshome = SiteImage.objects.filter(img_name=settings.GRAPPES_VIGNETTE)
    applehome = SiteImage.objects.filter(img_name=settings.APPLE_VIGNETTE)
    newslist = ListModel.objects.filter(
        list_name=settings.NEWSLETTER_USER_LIST)

    def get(self, request):
        return render(request, self.template_name, {'cows': self.cows[0],
                                                    'farm': self.farm[0],
                                                    'apple': self.apple[0],
                                                    'grappes': self.grappes[0],
                                                    'farm_txt': self.farm_txt[0],
                                                    'cows_txt': self.cows_txt[0],
                                                    'apple_txt': self.apple_txt[0],
                                                    'grappes_txt': self.grappes_txt[0],
                                                    'pfarminghome': self.pfarminghome[0],
                                                    'grappeshome': self.grappeshome[0],
                                                    'applehome': self.applehome[0]})

    def post(self, request):

        #Adding user to Newsletter list
        email = request.POST.get('email', '')
        if email not in self.newslist[0].list_content and email is not "":
            temp = self.newslist[0].list_content
            temp.append(email)
            try:
                self.newslist.update(list_content=temp)
                messages.info(request, 'Your email has been added to the newsletter difusion list!')
            except:
                messages.info(request, 'Your email could not be added!')
        else:
            messages.info(request, 'Your email is already in the newsletter difusion list...')


        return render(request, self.template_name, {'cows': self.cows[0],
                                                    'farm': self.farm[0],
                                                    'apple': self.apple[0],
                                                    'grappes': self.grappes[0],
                                                    'farm_txt': self.farm_txt[0],
                                                    'cows_txt': self.cows_txt[0],
                                                    'apple_txt': self.apple_txt[0],
                                                    'grappes_txt': self.grappes_txt[0],
                                                    'pfarminghome': self.pfarminghome[0],
                                                    'grappeshome': self.grappeshome[0],
                                                    'applehome': self.applehome[0]})


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
        meat = ListModel.objects.filter(list_name=settings.MEAT_LIST_NAME)
        return render(request, self.template_name, {'meat_list': meat[0]})


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


class MyadminView(View):
    """
        Class view for admin panel
    """

    template_name = 'sunneberg/myadmin.html'

    def get(self, request):
        #get all editable elements
        farm = SiteImage.objects.filter(img_name=settings.FARM)
        farm_txt = SiteText.objects.filter(txt_name=settings.FARM_TXT)
        cows = SiteImage.objects.filter(img_name=settings.COWS)
        cows_txt = SiteText.objects.filter(txt_name=settings.COWS_TXT)
        apple = SiteImage.objects.filter(img_name=settings.APPLE)
        apple_txt = SiteText.objects.filter(txt_name=settings.APPLE_TXT)
        grappes = SiteImage.objects.filter(img_name=settings.GRAPPES)
        grappes_txt = SiteText.objects.filter(txt_name=settings.GRAPPES_TXT)
        meat = ListModel.objects.filter(list_name=settings.MEAT_LIST_NAME)
        pfarminghome = SiteImage.objects.filter(
            img_name=settings.COWS_VIGNETTE)
        grappeshome = SiteImage.objects.filter(
            img_name=settings.GRAPPES_VIGNETTE)
        applehome = SiteImage.objects.filter(img_name=settings.APPLE_VIGNETTE)
        newslist = ListModel.objects.filter(
            list_name=settings.NEWSLETTER_USER_LIST)

        #Deleting element from meat list
        element = request.GET.get('element', '')
        if element in meat[0].list_content and element is not "":
            temp = meat[0].list_content
            temp.remove(element)
            meat.update(list_content=temp)

        #Adding element in meat list
        new_element = request.GET.get('new_element', '')
        if new_element not in meat[0].list_content and new_element is not "":
            temp = meat[0].list_content
            temp.append(new_element)
            meat.update(list_content=temp)

        return render(request, self.template_name, {'cows': cows[0],
                                                    'farm': farm[0],
                                                    'apple': apple[0],
                                                    'grappes': grappes[0],
                                                    'farm_txt': farm_txt[0],
                                                    'cows_txt': cows_txt[0],
                                                    'apple_txt': apple_txt[0],
                                                    'grappes_txt': grappes_txt[0],
                                                    'meat': meat,
                                                    'meat_list': meat[0],
                                                    'pfarminghome': pfarminghome[0],
                                                    'grappeshome': grappeshome[0],
                                                    'applehome': applehome[0]})


def edit_thing(request, img_name):
    # grab the object...
    thing = SiteImage.objects.get(img_name=img_name)
    """if thing.user != request.user:
        raise Http404"""
    # set the form we're using...
    form_class = ImageForm
    if request.method == 'POST':
        # grab the data from the submitted form
        form = form_class(data=request.POST,
                          files=request.FILES, instance=thing)
        if form.is_valid():
            # save the new data
            form.save()
            return redirect('sunneberg/myadmin01.html', img_name=thing.img_name)
    # otherwise just create the form
    else:
        form = form_class(instance=thing)
    # and render the template
    return render(request, 'sunneberg/edit_thing.html', {
        'thing': thing,
        'form': form,
    })


def edit_thing_txt(request, txt_name):
    # grab the object...
    thing = SiteText.objects.get(txt_name=txt_name)
    """if thing.user != request.user:
        raise Http404"""
    # set the form we're using...
    form_class = TextForm
    if request.method == 'POST':
        # grab the data from the submitted form
        form = form_class(data=request.POST, instance=thing)
        if form.is_valid():
            # save the new data
            form.save()
            return redirect('/sunneberg/myadmin01', txt_name=thing.txt_name)
    # otherwise just create the form
    else:
        form = form_class(instance=thing)
    # and render the template
    return render(request, 'sunneberg/edit_thing_txt.html', {
        'thing': thing,
        'form': form,
    })

class DisplayListView(View):
    """
        Class to display email in newsletter list
    """
    template_name = 'sunneberg/displaylist.html'
    newslist = ListModel.objects.filter(
        list_name=settings.NEWSLETTER_USER_LIST)

    def get(self, request):
        return render(request, self.template_name, {'newslist': self.newslist[0]})


class EditListView(View):
    """
        Class to edit email in newsletter list
    """
    template_name = 'sunneberg/editlist.html'
    newslist = ListModel.objects.filter(
        list_name=settings.NEWSLETTER_USER_LIST)

    def get(self, request):

        #Deleting email from newsletter list
        del_email = request.GET.get('del_email', '')
        if del_email in self.newslist[0].list_content and del_email is not "":
            temp = self.newslist[0].list_content
            temp.remove(del_email)
            self.newslist.update(list_content=temp)

        #Adding email in newsletter list
        new_email = request.GET.get('new_email', '')
        if new_email not in self.newslist[0].list_content and new_email is not "":
            temp = self.newslist[0].list_content
            temp.append(new_email)
            self.newslist.update(list_content=temp)

        return render(request, self.template_name, {'newslist': self.newslist[0]})
    

class ContactView(View):
    """
        Class to display contact details
    """
    template_name = 'sunneberg/contact.html'

    def get(self, request):
        return render(request, self.template_name)


class CarouView(View):
    """
        Class to display contact details
    """
    template_name = 'sunneberg/testcarou.html'

    def get(self, request):
        return render(request, self.template_name)


class BasicInsert(View):
    """
        Class basic image insert (site init)
    """
    template_name = 'sunneberg/binsert.html'

    def get(self, request):
        # APPLE
        if not SiteImage.objects.filter(img_name=settings.APPLE):
            my_insert = SiteImage(img_name=settings.APPLE,
                                  img_img="applejuice.jpg")
            print(my_insert)
            my_insert.save()

        if not SiteText.objects.filter(txt_name=settings.APPLE_TXT):
            my_insert = SiteText(txt_name=settings.APPLE_TXT,
                                 txt_title="Thanks To Our Appletree We Produce Fresh Juice",
                                 txt_text="Ut enim ad minim quis nostrud exerci sed do eiusmod tempor incididunt ut labore et dolore magna aliqua nostrud exerci sed.")
            print(my_insert)
            my_insert.save()

        if not SiteImage.objects.filter(img_name=settings.APPLE_VIGNETTE):
            my_insert = SiteImage(img_name=settings.APPLE_VIGNETTE,
                                  img_img="applehome.jpg")
            print(my_insert)
            my_insert.save()

        # Farm
        if not SiteImage.objects.filter(img_name=settings.FARM):
            my_insert = SiteImage(img_name=settings.FARM,
                                  img_img="farm.jpg")
            print(my_insert)
            my_insert.save()

        if not SiteText.objects.filter(txt_name=settings.FARM_TXT):
            my_insert = SiteText(txt_name=settings.FARM_TXT,
                                 txt_title="Discover How We Are And What We Do",
                                 txt_text="Ut enim ad minim quis nostrud exerci sed do eiusmod tempor incididunt ut labore et dolore magna aliqua nostrud exerci sed.")
            print(my_insert)
            my_insert.save()

        # Cows
        if not SiteImage.objects.filter(img_name=settings.COWS):
            my_insert = SiteImage(img_name=settings.COWS,
                                  img_img="cows.jpg")
            print(my_insert)
            my_insert.save()

        if not SiteText.objects.filter(txt_name=settings.COWS_TXT):
            my_insert = SiteText(txt_name=settings.COWS_TXT,
                                 txt_title="We raise cows in order to produce meat ",
                                 txt_text="Ut enim ad minim quis nostrud exerci sed do eiusmod tempor incididunt ut labore et dolore magna aliqua nostrud exerci sed.")
            print(my_insert)
            my_insert.save()

        if not SiteImage.objects.filter(img_name=settings.COWS_VIGNETTE):
            my_insert = SiteImage(img_name=settings.COWS_VIGNETTE,
                                  img_img="pfarminghome.jpg")
            print(my_insert)
            my_insert.save()

        # Grappes
        if not SiteImage.objects.filter(img_name=settings.GRAPPES):
            my_insert = SiteImage(img_name=settings.GRAPPES,
                                  img_img="grappes.jpg")
            print(my_insert)
            my_insert.save()

        if not SiteText.objects.filter(txt_name=settings.GRAPPES_TXT):
            my_insert = SiteText(txt_name=settings.GRAPPES_TXT,
                                 txt_title="Cultivating Grappes To Produce Vine",
                                 txt_text="Ut enim ad minim quis nostrud exerci\
                                 sed do eiusmod tempor incididunt ut labore\
                                      et dolore magna aliqua nostrud exerci sed.")
            print(my_insert)
            my_insert.save()

        if not SiteImage.objects.filter(img_name=settings.GRAPPES_VIGNETTE):
            my_insert = SiteImage(img_name=settings.GRAPPES_VIGNETTE,
                                  img_img="vinehome.jpg")
            print(my_insert)
            my_insert.save()

        # Meat list
        if not ListModel.objects.filter(list_name=settings.MEAT_LIST_NAME):
            my_insert = ListModel(list_name=settings.MEAT_LIST_NAME,
                                  list_content=["Entrecote", "Filet", "Foie"])
            print(my_insert)
            my_insert.save()

        # Newsletter user list
        if not ListModel.objects.filter(list_name=settings.NEWSLETTER_USER_LIST):
            my_insert = ListModel(list_name=settings.NEWSLETTER_USER_LIST,
                                  list_content=[])
            print(my_insert)
            my_insert.save()

        return render(request, self.template_name)
