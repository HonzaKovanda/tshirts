from django.db import models

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


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    image = models.ImageField(upload_to='gallery_for_print')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, default=1)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, default=1)
    note = models.TextField(max_length=500, blank=True, null=True)
    created = models.DateTimeField('Created', auto_now_add=True)
    price = models.IntegerField(blank=True, null=True)
    basic_image = models.BooleanField(default=False)
    belongs_to_order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

