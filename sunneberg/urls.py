from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.clickjacking import xframe_options_sameorigin

from . import views

app_name='sunneberg'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    path('aboutus/', views.AboutusView.as_view(), name='aboutus'),
    path('farming/', views.FarmingView.as_view(), name='farming'),
    path('vine/', views.VineView.as_view(), name='vine'),
    path('apple/', views.AppleView.as_view(), name='apple'),
    path('binsert/', views.BasicInsert.as_view(), name='binsert'),
    url(r'^things/(?P<img_name>[-\w]+)/edit/$', views.edit_thing, name='edit_thing'),
    url(r'^txt_things/(?P<txt_name>[-\w]+)/edit/$', views.edit_thing_txt, name='edit_thing_txt'),
    url(r'^pdf_things/(?P<pdf_name>[-\w]+)/edit/$', views.edit_thing_pdf, name='edit_thing_pdf'),
    path('myadmin01/', views.MyadminView.as_view(), name='myadmin'),
    path(r'myadmin01/?', views.MyadminView.as_view(), name='myadmin'),
    path(r'displaylist/', views.DisplayListView.as_view(), name='displaylist'),
    path(r'editlist/', views.EditListView.as_view(), name='editlist'),
    path(r'editlist/?', views.EditListView.as_view(), name='editlist'),
    path(r'contact/', views.ContactView.as_view(), name='contact'),
    path(r'testcarou/', views.CarouView.as_view(), name='testcarou'),
    path(r'news/', xframe_options_sameorigin(views.NewsView.as_view()), name='news'),
    path(r'unsubscribe/', views.UnsubView.as_view(), name='unsub'),
    path(r'unsubscribe/^$', views.UnsubView.as_view(), name='unsub'),
    path(r'unsubconfirm/', views.UnsubConfView.as_view(), name='unsubconfirm'),
    path(r'logmeout/', views.logmeout, name='logmeout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)