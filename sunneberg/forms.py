from django.forms import ModelForm
from django.conf import settings
from .models import SiteImage, SiteText, PdfModel
from django import forms


class ImageForm(ModelForm):

    class Meta:
        model = SiteImage
        fields = ('img_img',)


class TextForm(ModelForm):
    
    class Meta:
        model = SiteText
        fields = ('txt_title', 'txt_text')


class ConnexionForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput)


class PdfForm(ModelForm):
    
    class Meta:
        model = PdfModel
        fields = ('pdf_title', 'pdf_file',)