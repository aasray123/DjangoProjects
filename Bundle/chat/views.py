from django.shortcuts import HttpResponse, render, redirect
from django.template import loader

def lobby(request):
    
    return render(request, 'chat/lobby.html')

def home(request):
    return render(request, 'chat/lobby.html')