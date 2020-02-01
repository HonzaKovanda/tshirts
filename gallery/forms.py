from django import forms
from .models import Image

from django.contrib.auth import get_user_model

User = get_user_model()

class ImageForm(forms.ModelForm):

    #image = forms.ImageField(label='Vybrat obrázek', required = True)
    #title = forms.CharField(label='Název obrázku (můžete zvolit vlastní)', required=True,)
    
    
    class Meta:
        model = Image
        fields = ['title', 'image', 'size', 'position']
        widgets = {'size': forms.RadioSelect, 'position': forms.RadioSelect,}

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs={'id': 'files',}
        self.fields['title'].widget.attrs={'id': 'title',}
        
        
        """
        widgets = {
            'question_text': forms.TextInput(
				attrs={
					'class': 'form-control'
					}
				),
            'image': forms.FileInput(
				attrs={
					'class': 'form-control-file',
					}
				),
			}
            """