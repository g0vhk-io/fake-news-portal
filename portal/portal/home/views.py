from django.shortcuts import render
from django.http import HttpResponse
from portal.settings import API_HOST
from markdownx.widgets import MarkdownxWidget
from django.views.decorators.csrf import csrf_exempt
from proxy.views import proxy_view
import requests

# Create your views here.

def index_view(request):
    r = requests.get(API_HOST + '/api/reports')
    print(r.text)
    j = r.json()
    total = len(j)
    #return HttpResponse("Hello world ! " + str(len(j)))
    return render(request, 'index.html', {'total': total, 'reports': j})

def detail_view(request, report_id):
    r = requests.get(API_HOST + '/api/report/%d/' % (report_id))
    if r.status_code // 100 == 4:
        return render(request, 'not_found.html')
    w = MarkdownxWidget()
    a = w.render('comment', '', {})
    return render(request, 'detail.html', {'report': r.json(), 'markdownx_editor': a})


@csrf_exempt
def proxy_markdown_upload_view(request):
    remote_url = API_HOST + '/markdownx/upload/'
    return proxy_view(request, remote_url, {})

@csrf_exempt
def proxy_markdownify_view(request):
    remote_url = API_HOST + '/markdownx/markdownify/'
    return proxy_view(request, remote_url, {})
