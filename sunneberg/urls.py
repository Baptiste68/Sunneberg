from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    path('aboutus/', views.AboutusView.as_view(), name='aboutus'),
    path('farming/', views.FarmingView.as_view(), name='farming'),
    path('vine/', views.VineView.as_view(), name='vine'),
    path('apple/', views.AppleView.as_view(), name='apple'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)