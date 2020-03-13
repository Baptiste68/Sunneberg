from django.test import TestCase, RequestFactory, Client

from django.urls import reverse, path
from django.conf.urls import include, url
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.conf import settings

from .models import SiteImage, SiteText, ListModel, PdfModel, UnsubModel
from .forms import ImageForm, TextForm, ConnexionForm
from .views import IndexView, MyadminView

from django.contrib import messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware

# Create your tests here.


def populate():
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

    # Meat list
    if not ListModel.objects.filter(list_name=settings.MEAT_LIST_NAME):
        my_insert = ListModel(list_name=settings.MEAT_LIST_NAME,
                              list_content=["Entrecote", "Filet", "Foie"])
        my_insert.save()

    # Newsletter user list
    if not ListModel.objects.filter(list_name=settings.NEWSLETTER_USER_LIST):
        my_insert = ListModel(list_name=settings.NEWSLETTER_USER_LIST,
                              list_content=["email@test.com"])
        my_insert.save()

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

    if not ListModel.objects.filter(list_name=settings.VINE_LIST_NAME):
            my_insert = ListModel(list_name=settings.VINE_LIST_NAME,
                                  list_content=settings.VINE_TUPLE_LIST)
            my_insert.save()



class GeneralTest(TestCase):
    populate()
    def test_index(self):
        response = self.client.get(reverse('sunneberg:index'))
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.client.get(reverse('sunneberg:aboutus'))
        self.assertEqual(response.status_code, 200)

    def test_farming(self):
        response = self.client.get(reverse('sunneberg:farming'))
        self.assertEqual(response.status_code, 200)

    def test_vine(self):
        response = self.client.get(reverse('sunneberg:vine'))
        self.assertEqual(response.status_code, 200)

    def test_apple(self):
        response = self.client.get(reverse('sunneberg:apple'))
        self.assertEqual(response.status_code, 200)

    def test_myadmin01(self):
        response = self.client.get(reverse('sunneberg:myadmin'))
        self.assertEqual(response.status_code, 200)


class UserTest(TestCase):
    def setUp(self):
        # Create some users
        self.user_1 = User.objects.create_user(
            'basim', 'bas@bas.bas', 'simba', first_name='first_name',
            last_name='last_name')
        self.client = Client()
    
    def test_login(self):
        response = self.client.post('/sunneberg/myadmin01/', {'username': 'basim', 'password': 'simba'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context["user"]), "basim")

    def test_logout(self):
        self.client.force_login(self.user_1)
        logout = self.client.post('/sunneberg/logmeout/')
        response = self.client.get('/sunneberg/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context["user"]), "AnonymousUser")


class ListTest(TestCase):
    """
        Testing correct behavior of lists
        after a POST request
    """
    def setUp(self):
        self.template_name = ''
        self.client = Client()
        populate()

    def test_email_news(self):
        self.template_name = "sunneberg/index.html"
        mail = "test@email.com"
        self.newslist = ListModel.objects.filter(list_name=settings.NEWSLETTER_USER_LIST)
        result=self.client.post(reverse('sunneberg:index'), {'email': mail})
        self.newslist = ListModel.objects.filter(list_name=settings.NEWSLETTER_USER_LIST)

        self.assertIn(mail, self.newslist[0].list_content)
        self.assertEqual(result.status_code, 200)


    def test_meat_list(self):
        #testing adding element
        new_elem = 'my elem'
        meatlist = ListModel.objects.filter(list_name=settings.MEAT_LIST_NAME)
        meatlist = meatlist[0].list_content
        meatlist.append(new_elem)
        request = self.client.get('/sunneberg/myadmin01/', {'new_element': new_elem})
        gotmeatlist = ListModel.objects.filter(list_name=settings.MEAT_LIST_NAME)
        self.assertEqual(meatlist, gotmeatlist[0].list_content)

        #testing deleting this new element
        request = self.client.get('/sunneberg/myadmin01/', {'element': new_elem})
        meatlist.remove(new_elem)
        gotmeatlist = ListModel.objects.filter(list_name=settings.MEAT_LIST_NAME)
        self.assertEqual(meatlist, gotmeatlist[0].list_content)

        #testing of empty list
        empty = []
        newmeatlist = ['my elem']
        gotmeatlist.update(list_content=empty)
        result = self.client.get('/sunneberg/myadmin01/', {'element': new_elem})
        gotmeatlist = ListModel.objects.filter(list_name=settings.MEAT_LIST_NAME)
        self.assertEqual(result.status_code, 200)
        result = self.client.get('/sunneberg/myadmin01/', {'new_element': new_elem})
        gotmeatlist = ListModel.objects.filter(list_name=settings.MEAT_LIST_NAME)
        self.assertEqual(newmeatlist, gotmeatlist[0].list_content)
        self.assertEqual(result.status_code, 200)

    def test_available_list(self):
        #testing switching availability to 0
        #to do so, enter an empty post
        vine_list = ListModel.objects.filter(list_name=settings.VINE_LIST_NAME)
        #entry 0 (leo_millot) should be to 1 cf. settings
        self.assertEqual(vine_list[0].list_content[0][1], '1')
        request = self.client.post('/sunneberg/myadmin01/')
        new_vine_list = ListModel.objects.filter(list_name=settings.VINE_LIST_NAME)
        self.assertEqual(new_vine_list[0].list_content[0][1], '0')

        #testing switching it back to 1
        val = 1
        vine_list = ListModel.objects.filter(list_name=settings.VINE_LIST_NAME)
        vine_list = vine_list[0].list_content
        key_list = []
        for key, val in vine_list:
            key_list.append(key)
        
        index = key_list[0].index("leo_millot")
        vine_list[index][1] = val
        request = self.client.get('/sunneberg/myadmin01/', {'leo_millot': val})
        new_vine_list = ListModel.objects.filter(list_name=settings.VINE_LIST_NAME)
        self.assertEqual(vine_list[index][1], new_vine_list[0].list_content[index][1])






