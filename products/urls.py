from django.urls import path

from . import views

app_name='products'

urlpatterns = [
    path('', views.index_view, name='home'),
    path('detail/<slug>/', views.tshirt_detail, name='detail'),
    path('update_description/<slug>/', views.DescriptionUpdate.as_view(), name='update_description'),
]