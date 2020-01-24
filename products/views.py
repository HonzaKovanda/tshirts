#!/usr/bin/python3.8.1

from django.shortcuts import render, HttpResponse, get_object_or_404
from django.urls import reverse

from django.views import generic

from .models import Tshirt


class IndexView(generic.ListView):
    template_name = 'products/index.html'
    #context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Tshirt.objects.filter()

def tshirt_detail(request, slug):
    tshirt = get_object_or_404(Tshirt, slug=slug)
    all_colors = Tshirt.objects.filter(title=tshirt.title)
    return render(request, 'products/detail.html', {'tshirt': tshirt, 'all_colors' : all_colors,})


"""
class DetailView(generic.DetailView):
    #model = Tshirt
    template_name = 'products/detail.html'

    def get_queryset(self):
        return Tshirt.objects.filter(title="Classic")

"""
