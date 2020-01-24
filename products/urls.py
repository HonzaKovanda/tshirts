from django.urls import path

from . import views

app_name='products'

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('detail/<slug>/', views.tshirt_detail, name='detail'),
]