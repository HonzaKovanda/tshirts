from django.shortcuts import render, redirect, reverse
from django.views import generic

from .models import Image
from .forms import ImageForm
from cart.views import anonymous_or_real

from random import randint

"""
class IndexView(generic.ListView):
    template_name = 'gallery/index.html'

    def get_queryset(self, request):
        return Image.objects.filter(user=request.user)
"""


def index_view(request):

    anonymous_or_real(request)
    user = request.user

    object_list = Image.objects.filter(user=user, basic_image=True).order_by('-created')
    return render(request, "gallery/index.html", { 'object_list':object_list})


class CreateImage(generic.edit.CreateView):
    
    form_class = ImageForm
    template_name = "gallery/create_image.html"

    def get(self, request):

        #random_numer = randint(1000, 100000)
        #default_image_name = 'Obrázek ' + str(random_numer)
        #initial = {'title':default_image_name,}
        #form = self.form_class(initial=initial)

        form = self.form_class()
        return render(request, self.template_name, {"form":form, })

    def post(self, request):
        form = self.form_class(request.POST, request.FILES,)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.basic_image = True
            obj.save()
            return redirect(reverse("gallery:home"))
        else:
            alert = "Invalid form"
            return render(request, self.template_name, {"form":form, })