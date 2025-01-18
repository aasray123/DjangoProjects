from django.urls import path
from .views import *

urlpatterns = [
    path('', search_page, name='search')
]