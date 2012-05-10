from django import forms
from docviewer.models import Document
from django.utils.translation import ugettext_lazy as _



class DocumentForm(forms.ModelForm):
    
    file = forms.FileField(label = _('Document'))


    class Meta:
        model = Document