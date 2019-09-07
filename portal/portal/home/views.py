from django.shortcuts import render
from django.http import HttpResponse
from portal.settings import API_HOST
import requests

# Create your views here.

def index_view(request):
    r = requests.get(API_HOST + '/api/reports')
    print(r.text)
    j = r.json()
    total = len(j)
    #return HttpResponse("Hello world ! " + str(len(j)))
    return render(request, 'index.html', {'total': total, 'reports': j})
