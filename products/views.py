#!/usr/bin/python3.8.1

from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

from django.views import generic
from cart.views import migrate_temp_user

from .models import Tshirt
from .adler_stock import stock_status


"""
class IndexView(generic.ListView):
    template_name = 'products/index.html'


    def get_queryset(self):
        return Tshirt.objects.filter(cover=True)
"""

def index_view(request):
    object_list = Tshirt.objects.filter(cover=True)
    all_colors = Tshirt.objects.filter()

    return render(request, 'products/index.html', {'object_list': object_list, 'all_colors': all_colors })


def tshirt_detail(request, slug):
    tshirt = get_object_or_404(Tshirt, slug=slug)
    all_colors = Tshirt.objects.filter(nomen_code=tshirt.nomen_code)

    # Get items stock status
    nomen_tshirt = tshirt.nomen_code
    nomen_color = tshirt.color.nomen_code
    nomen_size = tshirt.size.all()
    on_stock = []


    for size in nomen_size:
        nomen = str(nomen_tshirt) + str(nomen_color) + str(size.nomen_code)
        i = str(size.title) +' - '+ str(stock_status(nomen))
        on_stock.append(i)

    return render(request, 'products/detail.html', {'tshirt': tshirt, 'all_colors' : all_colors, 'on_stock' : on_stock,})


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

