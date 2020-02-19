from django.urls import path

from . import views
#from .models import unsupported_extension_alert

app_name='gallery'

urlpatterns = [
    path('', views.index_view, name='home'),
    path('nahrat/', views.CreateImage.as_view(), name='create'),
    #path('nepodporovany_soubor/', unsupported_extension_alert, name='unsupported_extension_alert'),
    
]