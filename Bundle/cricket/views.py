from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# Create your views here.

# @login_required
def search_page(request):
    return render(request, 'cricket/search.html')

def play_page(request):
    return render(request)


"""
Players
Find partner
Play page

"""