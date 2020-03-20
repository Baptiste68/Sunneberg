"""
Module to manage the forms used
in the project
"""
from django import forms
from django.forms import ModelForm
from .models import SiteImage, SiteText, PdfModel


class ImageForm(ModelForm):
    """
    Image form to change image
    """
    class Meta:
        """
        Meta for image update
        """
        model = SiteImage
        fields = ('img_img',)


class TextForm(ModelForm):
    """
    Text form to update text and title
    """
    class Meta:
        """
        Meta for text update
        """
        model = SiteText
        fields = ('txt_title', 'txt_text')


class ConnexionForm(forms.Form):
    """
    For user login
    """
    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput)


class PdfForm(ModelForm):
    """
    To upload new PDF
    """
    class Meta:
        """
        Meta for pdf update
        """
        model = PdfModel
        fields = ('pdf_title', 'pdf_file',)
