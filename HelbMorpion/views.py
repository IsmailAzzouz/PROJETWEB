from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'index.html', {'title':'HOME'})

def about(request):
    return HttpResponse("<h1>about</h1>", {'title':'ABOUT'})