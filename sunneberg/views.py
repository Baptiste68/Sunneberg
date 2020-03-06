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
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail

from .models import SiteImage, SiteText, ListModel, PdfModel, UnsubModel
from .forms import ImageForm, TextForm, ConnexionForm, PdfForm

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
        return render(request, self.template_name, {'cows': self.cows,
                                                    'farm': self.farm,
                                                    'apple': self.apple,
                                                    'grappes': self.grappes,
                                                    'farm_txt': self.farm_txt,
                                                    'cows_txt': self.cows_txt,
                                                    'apple_txt': self.apple_txt,
                                                    'grappes_txt': self.grappes_txt,
                                                    'pfarminghome': self.pfarminghome,
                                                    'grappeshome': self.grappeshome,
                                                    'applehome': self.applehome})

    def post(self, request):
        #Adding user to Newsletter list
        email = request.POST.get('email', '')
        try:
            self.newslist[0] is not ""
            if email not in self.newslist[0].list_content and email is not "":
                temp = self.newslist[0].list_content
                temp.append(email)
                try:
                    self.newslist.update(list_content=temp)
                    messages.info(
                        request, 'Your email has been added to the newsletter difusion list!')
                except:
                    messages.info(request, 'Your email could not be added!')
            else:
                messages.info(
                    request, 'Your email is already in the newsletter difusion list...')
        
        except:
            try:
                self.newslist.update(list_content=temp)
                messages.info(
                    request, 'Your email has been added to the newsletter difusion list!')
            except:
                messages.info(request, 'Your email could not be added!')

        return render(request, self.template_name, {'cows': self.cows,
                                                    'farm': self.farm,
                                                    'apple': self.apple,
                                                    'grappes': self.grappes,
                                                    'farm_txt': self.farm_txt,
                                                    'cows_txt': self.cows_txt,
                                                    'apple_txt': self.apple_txt,
                                                    'grappes_txt': self.grappes_txt,
                                                    'pfarminghome': self.pfarminghome,
                                                    'grappeshome': self.grappeshome,
                                                    'applehome': self.applehome})


class AboutusView(View):
    """
        Class view for about us section
    """
    template_name = 'sunneberg/aboutus.html'
    
    project1 = SiteText.objects.filter(txt_name=settings.PROJ1_TXT)
    project2 = SiteText.objects.filter(txt_name=settings.PROJ2_TXT)
    project3 = SiteText.objects.filter(txt_name=settings.PROJ3_TXT)

    def get(self, request):
        return render(request, self.template_name, {'proj1': self.project1,
                                                    'proj2': self.project2,
                                                    'proj3': self.project3})


class FarmingView(View):
    """
        Class view for pastoral farming section
    """
    template_name = 'sunneberg/farming.html'
    meat = ListModel.objects.filter(list_name=settings.MEAT_LIST_NAME)
    farmingcow1 = SiteImage.objects.filter(img_name=settings.FCOW1)
    farmingcow2 = SiteImage.objects.filter(img_name=settings.FCOW2)
    farmingcow3 = SiteImage.objects.filter(img_name=settings.FCOW3)
    farmingcow4 = SiteImage.objects.filter(img_name=settings.FCOW4)
    meat_order = PdfModel.objects.filter(pdf_name=settings.ORDER_MEAT)

    def get(self, request):
        
        return render(request, self.template_name, {'meat_list': self.meat,
                                                    'fcow1': self.farmingcow1,
                                                    'fcow2': self.farmingcow2,
                                                    'fcow3': self.farmingcow3,
                                                    'fcow4': self.farmingcow4,
                                                    'pdf_order': self.meat_order})


class VineView(View):
    """
        Class view for vineyard section
    """
    template_name = 'sunneberg/vine.html'
    vine_order = PdfModel.objects.filter(pdf_name=settings.ORDER_VINE)

    def get(self, request):
        return render(request, self.template_name, {'pdf_order': self.vine_order})


class AppleView(View):
    """
        Class view for apple section
    """
    template_name = 'sunneberg/apple.html'
    applepage1 = SiteImage.objects.filter(img_name=settings.APPLE_PAGE1)
    applepage2 = SiteImage.objects.filter(img_name=settings.APPLE_PAGE2)
    apple_order = PdfModel.objects.filter(pdf_name=settings.ORDER_APPLE)

    def get(self, request):
        return render(request, self.template_name, {'apple1': self.applepage1,
                                                    'apple2': self.applepage2,
                                                    'pdf_order': self.apple_order})


def logmeout(request):
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
    project1 = SiteText.objects.filter(txt_name=settings.PROJ1_TXT)
    project2 = SiteText.objects.filter(txt_name=settings.PROJ2_TXT)
    project3 = SiteText.objects.filter(txt_name=settings.PROJ3_TXT)
    farmingcow1 = SiteImage.objects.filter(img_name=settings.FCOW1)
    farmingcow2 = SiteImage.objects.filter(img_name=settings.FCOW2)
    farmingcow3 = SiteImage.objects.filter(img_name=settings.FCOW3)
    farmingcow4 = SiteImage.objects.filter(img_name=settings.FCOW4)
    applepage1 = SiteImage.objects.filter(img_name=settings.APPLE_PAGE1)
    applepage2 = SiteImage.objects.filter(img_name=settings.APPLE_PAGE2)
    mvp = PdfModel.objects.filter(pdf_name=settings.MVP_NEWS)
    first = PdfModel.objects.filter(pdf_name=settings.NEWS_LIST_FIRST)
    second = PdfModel.objects.filter(pdf_name=settings.NEWS_LIST_SECOND)
    third = PdfModel.objects.filter(pdf_name=settings.NEWS_LIST_THIRD)
    fourth = PdfModel.objects.filter(pdf_name=settings.NEWS_LIST_FOURTH)
    order_meat = PdfModel.objects.filter(pdf_name=settings.ORDER_MEAT)
    order_vine = PdfModel.objects.filter(pdf_name=settings.ORDER_VINE)
    order_apple = PdfModel.objects.filter(pdf_name=settings.ORDER_APPLE)

    def get(self, request):
        form = ConnexionForm(request.POST)

        #Deleting element from meat list
        element = request.GET.get('element', '')
        try:
            self.meat[0] is not ""
            if element in self.meat[0].list_content and element is not "":
                temp = self.meat[0].list_content
                temp.remove(element)
                self.meat.update(list_content=temp)
        except:
            pass

        #Adding element in meat list
        new_element = request.GET.get('new_element', '')
        try:
            self.meat[0] is not ""
            if new_element not in self.meat[0].list_content and new_element is not "":
                temp = self.meat[0].list_content
                temp.append(new_element)
                self.meat.update(list_content=temp)
        except:
            temp = eval('[' + new_element + ']')
            self.meat.update(list_content=temp)

        return render(request, self.template_name, {'cows': self.cows,
                                                    'farm': self.farm,
                                                    'apple': self.apple,
                                                    'grappes': self.grappes,
                                                    'farm_txt': self.farm_txt,
                                                    'cows_txt': self.cows_txt,
                                                    'apple_txt': self.apple_txt,
                                                    'grappes_txt': self.grappes_txt,
                                                    'meat': self.meat,
                                                    'meat_list': self.meat,
                                                    'pfarminghome': self.pfarminghome,
                                                    'grappeshome': self.grappeshome,
                                                    'applehome': self.applehome,
                                                    'form': form,
                                                    'proj1': self.project1,
                                                    'proj2': self.project2,
                                                    'proj3': self.project3,
                                                    'fcow1': self.farmingcow1,
                                                    'fcow2': self.farmingcow2,
                                                    'fcow3': self.farmingcow3,
                                                    'fcow4': self.farmingcow4,
                                                    'apple1': self.applepage1,
                                                    'apple2': self.applepage2,
                                                    'mvp': self.mvp,
                                                    'first': self.first,
                                                    'second': self.second,
                                                    'third': self.third,
                                                    'fourth': self.fourth,
                                                    'order_meat': self.order_meat,
                                                    'order_vine': self.order_vine,
                                                    'order_apple': self.order_apple})


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

        return render(request, self.template_name, {'cows': self.cows,
                                                    'farm': self.farm,
                                                    'apple': self.apple,
                                                    'grappes': self.grappes,
                                                    'farm_txt': self.farm_txt,
                                                    'cows_txt': self.cows_txt,
                                                    'apple_txt': self.apple_txt,
                                                    'grappes_txt': self.grappes_txt,
                                                    'meat': self.meat,
                                                    'meat_list': self.meat,
                                                    'pfarminghome': self.pfarminghome,
                                                    'grappeshome': self.grappeshome,
                                                    'applehome': self.applehome,
                                                    'form': form,
                                                    'proj1': self.project1,
                                                    'proj2': self.project2,
                                                    'proj3': self.project3,
                                                    'error': error,
                                                    'fcow1': self.farmingcow1,
                                                    'fcow2': self.farmingcow2,
                                                    'fcow3': self.farmingcow3,
                                                    'fcow4': self.farmingcow4,
                                                    'apple1': self.applepage1,
                                                    'apple2': self.applepage2})


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
            return redirect('/sunneberg/myadmin01')
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


def edit_thing_pdf(request, pdf_name):
    # grab the object...
    thing = PdfModel.objects.get(pdf_name=pdf_name)
    """if thing.user != request.user:
        raise Http404"""
    # set the form we're using...
    form_class = PdfForm
    if request.method == 'POST':
        # grab the data from the submitted form
        form = form_class(data=request.POST,
                          files=request.FILES, instance=thing)
        if form.is_valid():
            # save the new data
            form.save()
            return redirect('/sunneberg/myadmin01')
    # otherwise just create the form
    else:
        form = form_class(instance=thing)
    # and render the template
    return render(request, 'sunneberg/edit_thing_pdf.html', {
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


class NewsView(View):
    def get(self, request):
        """
            Class to display the news in pdf format
        """
        template_name = 'sunneberg/news.html'
        mvp = PdfModel.objects.filter(pdf_name=settings.MVP_NEWS)
        first = PdfModel.objects.filter(pdf_name=settings.NEWS_LIST_FIRST)
        second = PdfModel.objects.filter(pdf_name=settings.NEWS_LIST_SECOND)
        third = PdfModel.objects.filter(pdf_name=settings.NEWS_LIST_THIRD)
        fourth = PdfModel.objects.filter(pdf_name=settings.NEWS_LIST_FOURTH)

        return render(request, template_name, {'mvp': mvp,
                                            'first': first,
                                            'second': second,
                                            'third': third,
                                            'fourth': fourth,
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
                                       unsub_code=random.randrange(
                                           10000, 99999),
                                       unsub_duration="2:20:10")
                my_insert.save()
                code = UnsubModel.objects.filter(
                    unsub_email=email)[0].unsub_code

                try:
                    send_mail(
                        'Unsubscribe Sunnenberg NewsLetter',
                        "Hello \n Please click to this link to end the unsubscription:\n "+ settings.CONFIRM_UNSUB +" \n " +
                        "Your code is " + str(code),
                        'baptistesimon1@gmail.com',
                        [email],
                        fail_silently=False,
                    )
                    messages.info(
                        request, 'SUCCES: You should have received an email to confirm the deletion')

                except:
                    UnsubModel.objects.filter(unsub_email=email).delete()
                    messages.info(request, 'ERROR: while trying to send email')
            else:
                messages.info(
                    request, 'ERROR: Your email is already in the deletion process...')
        else:
            messages.info(
                request, 'ERROR: Your email is not in the NewsLetter list...')

        return render(request, self.template_name)


class UnsubConfView(View):
    """
        Unsubscribe View
    """

    template_name = 'sunneberg/unsubconf.html'
    newslist = ListModel.objects.filter(
        list_name=settings.NEWSLETTER_USER_LIST)

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email_conf', '')
        code = request.POST.get('code', '')
        if email in self.newslist[0].list_content:
            try:
                model = UnsubModel.objects.filter(unsub_email=email)
                if str(code) == str(model[0].unsub_code) and email == model[0].unsub_email:
                    temp = self.newslist[0].list_content
                    temp.remove(email)
                    self.newslist.update(list_content=temp)
                    UnsubModel.objects.filter(unsub_email=email).delete()

                    messages.info(
                        request, 'SUCCES: Your email has been removed')
                else:
                    messages.info(request, 'ERROR: email or code incorect')

            except:
                messages.info(request, 'ERROR: while trying to delete your email')

        else:
            messages.info(
                request, 'ERROR: Your email is not in the subscriber list...')


        return render(request, self.template_name)


class BasicInsert(View):
    """
        Class basic image insert (site init)
    """
    template_name = 'sunneberg/binsert.html'

    def get(self, request):
        """
            Index
        """
        # APPLE
        if not SiteImage.objects.filter(img_name=settings.APPLE):
            my_insert = SiteImage(img_name=settings.APPLE,
                                  img_img="applejuice.jpg")
            my_insert.save()

        if not SiteText.objects.filter(txt_name=settings.APPLE_TXT):
            my_insert = SiteText(txt_name=settings.APPLE_TXT,
                                 txt_title="Thanks To Our Appletree We Produce Fresh Juice",
                                 txt_text="Ut enim ad minim quis nostrud exerci sed do eiusmod tempor incididunt ut labore et dolore magna aliqua nostrud exerci sed.")
            my_insert.save()

        if not SiteImage.objects.filter(img_name=settings.APPLE_VIGNETTE):
            my_insert = SiteImage(img_name=settings.APPLE_VIGNETTE,
                                  img_img="applehome.jpg")
            my_insert.save()

        # Farm
        if not SiteImage.objects.filter(img_name=settings.FARM):
            my_insert = SiteImage(img_name=settings.FARM,
                                  img_img="farm.jpg")
            my_insert.save()

        if not SiteText.objects.filter(txt_name=settings.FARM_TXT):
            my_insert = SiteText(txt_name=settings.FARM_TXT,
                                 txt_title="Discover How We Are And What We Do",
                                 txt_text="Ut enim ad minim quis nostrud exerci sed do eiusmod tempor incididunt ut labore et dolore magna aliqua nostrud exerci sed.")
            my_insert.save()

        # Cows
        if not SiteImage.objects.filter(img_name=settings.COWS):
            my_insert = SiteImage(img_name=settings.COWS,
                                  img_img="cows.jpg")
            my_insert.save()

        if not SiteText.objects.filter(txt_name=settings.COWS_TXT):
            my_insert = SiteText(txt_name=settings.COWS_TXT,
                                 txt_title="We raise cows in order to produce meat ",
                                 txt_text="Ut enim ad minim quis nostrud exerci sed do eiusmod tempor incididunt ut labore et dolore magna aliqua nostrud exerci sed.")
            my_insert.save()

        if not SiteImage.objects.filter(img_name=settings.COWS_VIGNETTE):
            my_insert = SiteImage(img_name=settings.COWS_VIGNETTE,
                                  img_img="pfarminghome.jpg")
            my_insert.save()

        # Grappes
        if not SiteImage.objects.filter(img_name=settings.GRAPPES):
            my_insert = SiteImage(img_name=settings.GRAPPES,
                                  img_img="grappes.jpg")
            my_insert.save()

        if not SiteText.objects.filter(txt_name=settings.GRAPPES_TXT):
            my_insert = SiteText(txt_name=settings.GRAPPES_TXT,
                                 txt_title="Cultivating Grappes To Produce Vine",
                                 txt_text="Ut enim ad minim quis nostrud exerci\
                                 sed do eiusmod tempor incididunt ut labore\
                                      et dolore magna aliqua nostrud exerci sed.")
            my_insert.save()

        if not SiteImage.objects.filter(img_name=settings.GRAPPES_VIGNETTE):
            my_insert = SiteImage(img_name=settings.GRAPPES_VIGNETTE,
                                  img_img="vinehome.jpg")
            my_insert.save()

        # Newsletter user list
        if not ListModel.objects.filter(list_name=settings.NEWSLETTER_USER_LIST):
            my_insert = ListModel(list_name=settings.NEWSLETTER_USER_LIST,
                                  list_content=[])
            my_insert.save()

        """
            P Farming
        """
        # Meat list
        if not ListModel.objects.filter(list_name=settings.MEAT_LIST_NAME):
            my_insert = ListModel(list_name=settings.MEAT_LIST_NAME,
                                  list_content=["Entrecote", "Filet", "Foie"])
            my_insert.save()

        # Cows pix
        if not SiteImage.objects.filter(img_name=settings.FCOW1):
            my_insert = SiteImage(img_name=settings.FCOW1,
                                  img_img="vache1.jpg")
            my_insert.save()

        if not SiteImage.objects.filter(img_name=settings.FCOW2):
            my_insert = SiteImage(img_name=settings.FCOW2,
                                  img_img="vache2.jpg")
            my_insert.save()

        if not SiteImage.objects.filter(img_name=settings.FCOW3):
            my_insert = SiteImage(img_name=settings.FCOW3,
                                  img_img="vache3.jpg")
            my_insert.save()

        if not SiteImage.objects.filter(img_name=settings.FCOW4):
            my_insert = SiteImage(img_name=settings.FCOW4,
                                  img_img="vache4.jpg")
            my_insert.save()

        """
            News
        """
        # Pdf Insert
        if not PdfModel.objects.filter(pdf_name=settings.MVP_NEWS):
            my_insert = PdfModel(pdf_name=settings.MVP_NEWS,
                                 pdf_file="news1.pdf",
                                 pdf_title="Feb 2020 - New arrival")
            my_insert.save()

        if not PdfModel.objects.filter(pdf_name=settings.NEWS_LIST_FIRST):
            my_insert = PdfModel(pdf_name=settings.NEWS_LIST_FIRST,
                                 pdf_file="news2.pdf",
                                 pdf_title="Dec 2019 - Merry Xmas")
            my_insert.save()

        if not PdfModel.objects.filter(pdf_name=settings.NEWS_LIST_SECOND):
            my_insert = PdfModel(pdf_name=settings.NEWS_LIST_SECOND,
                                 pdf_file="news3.pdf",
                                 pdf_title="Oct 2019 - Apple time")
            my_insert.save()

        if not PdfModel.objects.filter(pdf_name=settings.NEWS_LIST_THIRD):
            my_insert = PdfModel(pdf_name=settings.NEWS_LIST_THIRD,
                                 pdf_file="news4.pdf",
                                 pdf_title="August 2019 - For sunny days")
            my_insert.save()

        if not PdfModel.objects.filter(pdf_name=settings.NEWS_LIST_FOURTH):
            my_insert = PdfModel(pdf_name=settings.NEWS_LIST_FOURTH,
                                 pdf_file="news5.pdf",
                                 pdf_title="April 2019 - Easter")
            my_insert.save()

        if not PdfModel.objects.filter(pdf_name=settings.ORDER_MEAT):
            my_insert = PdfModel(pdf_name=settings.ORDER_MEAT,
                                 pdf_file="PDFMEAT.pdf",
                                 pdf_title="Meat order formular")
            my_insert.save()
        
        if not PdfModel.objects.filter(pdf_name=settings.ORDER_VINE):
            my_insert = PdfModel(pdf_name=settings.ORDER_VINE,
                                 pdf_file="PDFVINE.pdf",
                                 pdf_title="Vine order formular")
            my_insert.save()

        if not PdfModel.objects.filter(pdf_name=settings.ORDER_APPLE):
            my_insert = PdfModel(pdf_name=settings.ORDER_APPLE,
                                 pdf_file="PDFAPPLE.pdf",
                                 pdf_title="Apple order formular")
            my_insert.save()

        """
            About us
        """
        #Projects insert
        if not SiteText.objects.filter(txt_name=settings.PROJ1_TXT):
            my_insert = SiteText(txt_name=settings.PROJ1_TXT,
                                 txt_title="Bio Diversity",
                                 txt_text="Vulputate ac met semper varius\
                                      Nullam consequat sapien sed leot cursus rhoncus. Nullam dui mi.")
            my_insert.save()
        
        if not SiteText.objects.filter(txt_name=settings.PROJ2_TXT):
            my_insert = SiteText(txt_name=settings.PROJ2_TXT,
                                 txt_title="EDUCATIONNAL FARMING",
                                 txt_text="Vulputate ac met semper varius\
                                      Nullam consequat sapien sed leot cursus rhoncus. Nullam dui mi.")
            my_insert.save()

        if not SiteText.objects.filter(txt_name=settings.PROJ3_TXT):
            my_insert = SiteText(txt_name=settings.PROJ3_TXT,
                                 txt_title="VULPUTATE AC",
                                 txt_text="Vulputate ac met semper varius\
                                      Nullam consequat sapien sed leot cursus rhoncus. Nullam dui mi.")
            my_insert.save()

        """
            Apple page
        """
        if not SiteImage.objects.filter(img_name=settings.APPLE_PAGE1):
            my_insert = SiteImage(img_name=settings.APPLE_PAGE1,
                                  img_img="apple1.jpg")
            my_insert.save()

        if not SiteImage.objects.filter(img_name=settings.APPLE_PAGE2):
            my_insert = SiteImage(img_name=settings.APPLE_PAGE2,
                                  img_img="apple2.jpg")
            my_insert.save()

        return render(request, self.template_name)
