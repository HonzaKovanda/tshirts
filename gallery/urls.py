from django.urls import path

from . import views

app_name='gallery'

urlpatterns = [
    path('', views.index_view, name='home'),
    path('nahrat/', views.CreateImage.as_view(), name='create'),
]