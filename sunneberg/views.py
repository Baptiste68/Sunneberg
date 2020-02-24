import requests
import json
import logging
import random

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
from django.http import FileResponse, Http404
# Manage X_Frame
from django.views.decorators.clickjacking import xframe_options_deny
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.decorators import method_decorator

from django.core.mail import send_mail

from .models import SiteImage, SiteText, ListModel, PdfModel, UnsubModel
from .forms import ImageForm, TextForm, ConnexionForm

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

def logmeout(request):
    print("Here")
    logout(request)
    return redirect('sunneberg:myadmin')

class MyadminView(View):
    """
        Class view for admin panel incl. login
    """

    template_name = 'sunneberg/myadmin.html'

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

    def get(self, request):
        #Deleting element from meat list
        element = request.GET.get('element', '')
        if element in self.meat[0].list_content and element is not "":
            temp = self.meat[0].list_content
            temp.remove(element)
            self.meat.update(list_content=temp)

        #Adding element in meat list
        new_element = request.GET.get('new_element', '')
        if new_element not in self.meat[0].list_content and new_element is not "":
            temp = self.meat[0].list_content
            temp.append(new_element)
            self.meat.update(list_content=temp)

        form = ConnexionForm(request.POST)

        return render(request, self.template_name, {'cows': self.cows[0],
                                                    'farm': self.farm[0],
                                                    'apple': self.apple[0],
                                                    'grappes': self.grappes[0],
                                                    'farm_txt': self.farm_txt[0],
                                                    'cows_txt': self.cows_txt[0],
                                                    'apple_txt': self.apple_txt[0],
                                                    'grappes_txt': self.grappes_txt[0],
                                                    'meat': self.meat,
                                                    'meat_list': self.meat[0],
                                                    'pfarminghome': self.pfarminghome[0],
                                                    'grappeshome': self.grappeshome[0],
                                                    'applehome': self.applehome[0],
                                                    'form': form})

    def post(self, request):
        error = False
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            # Nous vérifions si les données sont correctes
            user = authenticate(username=username, password=password)
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
            else:  # sinon une erreur sera affichée
                error = True

        return render(request, self.template_name, {'cows': self.cows[0],
                                                    'farm': self.farm[0],
                                                    'apple': self.apple[0],
                                                    'grappes': self.grappes[0],
                                                    'farm_txt': self.farm_txt[0],
                                                    'cows_txt': self.cows_txt[0],
                                                    'apple_txt': self.apple_txt[0],
                                                    'grappes_txt': self.grappes_txt[0],
                                                    'meat': self.meat,
                                                    'meat_list': self.meat[0],
                                                    'pfarminghome': self.pfarminghome[0],
                                                    'grappeshome': self.grappeshome[0],
                                                    'applehome': self.applehome[0],
                                                    'form': form,
                                                    'error': error})


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


@xframe_options_sameorigin
@xframe_options_exempt
def NewsView(request):
    """
        Class to display the news in pdf format
    """
    template_name = 'sunneberg/news.html'
    mvp = PdfModel.objects.filter(pdf_name=settings.MVP_NEWS)
    first = PdfModel.objects.filter(pdf_name=settings.NEWS_LIST_FIRST)
    second = PdfModel.objects.filter(pdf_name=settings.NEWS_LIST_SECOND)
    third = PdfModel.objects.filter(pdf_name=settings.NEWS_LIST_THIRD)
    fourth = PdfModel.objects.filter(pdf_name=settings.NEWS_LIST_FOURTH)
    print(mvp[0])
    print(mvp[0].pdf_file.url)

    return render(request, template_name, {'mvp': mvp[0],
                                            'first': first[0],
                                            'second': second[0],
                                            'third': third[0],
                                            'fourth': fourth[0],
                                            })


class UnsubView(View):
    """
        Unsubscribe View
    """
    
    template_name = 'sunneberg/unsubscribe.html'
    newslist = ListModel.objects.filter(
        list_name=settings.NEWSLETTER_USER_LIST)

    def get(self, request):
        return render(request, self.template_name)
        
    def post(self, request):
        email = request.POST.get('email_un', '')
        if email in self.newslist[0].list_content: 
            if not UnsubModel.objects.filter(unsub_email=email):
                my_insert = UnsubModel(unsub_email=email,
                                    unsub_code=random.randrange(10000,99999),
                                    unsub_duration = "2:20:10")
                my_insert.save()
                code = UnsubModel.objects.filter(unsub_email=email)[0].unsub_code
                
                try:
                    send_mail(
                        'Unsubscribe Sunnenberg NewsLetter',
                        "Hello /n Please click to this link to end the unsubscription:/n http://127.0.0.1:8000/sunneberg/unsubconfirm /n "+
                        "Your code is " + str(code),
                        'from@example.com',
                        [email],
                        fail_silently=False,
                    )
                    messages.info(request, 'SUCCES: You should have received an email to confirm the deletion')
                
                except:
                    UnsubModel.objects.filter(unsub_email=email).delete()
                    messages.info(request, 'ERROR: while trying to send email')
            else:
                messages.info(request, 'ERROR: Your email is already in the deletion process...')
        else:
            messages.info(request, 'ERROR: Your email is not in the NewsLetter list...')

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

        # Pdf Insert
        if not PdfModel.objects.filter(pdf_name=settings.MVP_NEWS):
            my_insert = PdfModel(pdf_name=settings.MVP_NEWS,
                                  pdf_file="news1.pdf",
                                  pdf_title="Feb 2020 - New arrival")
            print(my_insert)
            my_insert.save()
        
        
        if not PdfModel.objects.filter(pdf_name=settings.NEWS_LIST_FIRST):
            my_insert = PdfModel(pdf_name=settings.NEWS_LIST_FIRST,
                                  pdf_file="news2.pdf",
                                  pdf_title="Dec 2019 - Merry Xmas")
            print(my_insert)
            my_insert.save()
        
        
        if not PdfModel.objects.filter(pdf_name=settings.NEWS_LIST_SECOND):
            my_insert = PdfModel(pdf_name=settings.NEWS_LIST_SECOND,
                                  pdf_file="news3.pdf",
                                  pdf_title="Oct 2019 - Apple time")
            print(my_insert)
            my_insert.save()

            
        if not PdfModel.objects.filter(pdf_name=settings.NEWS_LIST_THIRD):
            my_insert = PdfModel(pdf_name=settings.NEWS_LIST_THIRD,
                                  pdf_file="news4.pdf",
                                  pdf_title="August 2019 - For sunny days")
            print(my_insert)
            my_insert.save()

        if not PdfModel.objects.filter(pdf_name=settings.NEWS_LIST_FOURTH):
            my_insert = PdfModel(pdf_name=settings.NEWS_LIST_FOURTH,
                                  pdf_file="news5.pdf",
                                  pdf_title="April 2019 - Easter")
            print(my_insert)
            my_insert.save()

        return render(request, self.template_name)
