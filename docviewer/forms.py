from django import forms
from docviewer.models import Document
from django.utils.translation import ugettext_lazy as _


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
