from django.shortcuts import render, redirect, reverse
from django.views import generic

from .models import Image
from .forms import ImageForm
from cart.views import anonymous_or_real

from django.contrib import messages

"""
class IndexView(generic.ListView):
    template_name = 'gallery/index.html'

    def get_queryset(self, request):
        return Image.objects.filter(user=request.user)
"""


def index_view(request):

    anonymous_or_real(request)
    user = request.user

    messages.info(request, 'Vítej v galerii :)')

    object_list = Image.objects.filter(user=user, basic_image=True).order_by('-created')
    return render(request, "gallery/index.html", { 'object_list':object_list})


class CreateImage(generic.edit.CreateView):
    
    form_class = ImageForm
    template_name = "gallery/create_image.html"

    def get(self, request):

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
            messages.warning(request, 'Neplatný formát souboru')
            return render(request, self.template_name, {"form":form, })