from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    # Send a simple HTML response
    return HttpResponse('<h1>Hello</h1>')

def about(request):
    return render(request, 'about.html')