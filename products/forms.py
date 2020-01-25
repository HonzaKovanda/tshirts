from django import forms
from .models import Tshirt

class ChooseSizeForm(forms.ModelForm):

    class Meta:
        model = Tshirt
        fields=["size"]