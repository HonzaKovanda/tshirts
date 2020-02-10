#!/usr/bin/python3.8.1

from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

from django.views import generic
from cart.views import migrate_temp_user

from .models import Tshirt


"""
class IndexView(generic.ListView):
    template_name = 'products/index.html'


    def get_queryset(self):
        return Tshirt.objects.filter(cover=True)
"""

def index_view(request):
    object_list = Tshirt.objects.filter(cover=True)
    all_colors = Tshirt.objects.filter()

    #migrate_temp_user(request)
    return render(request, 'products/index.html', {'object_list': object_list, 'all_colors': all_colors })


def tshirt_detail(request, slug):
    tshirt = get_object_or_404(Tshirt, slug=slug)
    all_colors = Tshirt.objects.filter(nomen_code=tshirt.nomen_code)
    return render(request, 'products/detail.html', {'tshirt': tshirt, 'all_colors' : all_colors, })


class DescriptionUpdate(generic.edit.UpdateView):
    model = Tshirt
    fields = ['description']
    template_name_suffix = '_update'

    def get_context_data(self,**kwargs):
        context = super(DescriptionUpdate,self).get_context_data(**kwargs)
        tshirt = get_object_or_404(Tshirt, slug=self.object.slug)
        context['all_colors'] = Tshirt.objects.filter(nomen_code=tshirt.nomen_code)
        return context

    def get_success_url(self):
        return reverse('products:detail', args=(self.object.slug, ))

