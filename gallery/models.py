from django.db import models
import os
from uuid import uuid4
from django.contrib import messages

from django.core.exceptions import ValidationError
from django.shortcuts import redirect

from django.core.validators import FileExtensionValidator

from django.contrib.auth import get_user_model

User = get_user_model()

class Position(models.Model):
    title = models.CharField(max_length=60)

    def __str__(self):
        return self.title


class Size(models.Model):
    title = models.CharField(max_length=60)

    def __str__(self):
        return self.title



def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    current_name = filename.split('.')[0:-1]
    current_name = '.'.join(current_name)
    filename = "%s_%s_%s.%s" % (current_name, instance.user.id, uuid4().hex[:8], ext)
    return os.path.join('gallery_for_print', filename)

"""
def validate_file_extension(value):
  ext = os.path.splitext(value.name)[1]
  valid_extensions = ['.png','.jpeg','.jpg','.pdf','.docx']
  if not ext in valid_extensions:
    raise ValidationError('File not supported!')
    #raise redirect('gallery:unsupported_extension_alert')
    

def unsupported_extension_alert(request):
    messages.info(request, 'Tento formát souboru nelze nahrát!')
    return redirect('gallery:create')
"""

class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    image = models.FileField(upload_to=content_file_name, validators=[FileExtensionValidator(['pdf', 'png', 'jpg', 'jpeg',],)])
    size = models.ForeignKey(Size, on_delete=models.CASCADE, default=1)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, default=1)
    note = models.TextField(max_length=500, blank=True, null=True)
    created = models.DateTimeField('Created', auto_now_add=True)
    price = models.IntegerField(blank=True, null=True)
    basic_image = models.BooleanField(default=False)
    belongs_to_order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

    def css_class(self):
        extension = (self.image.name).split('.')[-1]
        if extension == 'pdf':
            return 'pdf'
        if extension == 'xlsx':
            return 'xlsx'
        if extension == 'png':
            return 'png'
        if extension == 'jpg':
            return 'jpg'
        return 'other'

