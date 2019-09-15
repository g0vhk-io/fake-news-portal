from django.shortcuts import render
from django.http import HttpResponse
from portal.settings import API_HOST
from markdownx.widgets import MarkdownxWidget
from django.views.decorators.csrf import csrf_exempt
from proxy.views import proxy_view
import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from portal.settings import API_SERVER_TOKEN
from requests_toolbelt import MultipartEncoder
from django.utils.module_loading import import_string

# Create your views here.

def index_view(request):
    r = requests.get(API_HOST + '/api/reports')
    print(r.text)
    j = r.json()
    total = len(j)
    #return HttpResponse("Hello world ! " + str(len(j)))
    return render(request, 'index.html', {'total': total, 'reports': j})

def detail_view(request, report_id):
    is_editor = is_user_an_editor(request)
    r = requests.get(API_HOST + '/api/report/%d/' % (report_id))
    if r.status_code // 100 == 4:
        return render(request, 'not_found.html')
    widget_html = ""
    report = r.json()
    md = ""
    comment = report.get('comment', None)
    if comment is None:
        comment = {'md': ''}
    value = comment['md']
    if is_editor:
        w = MarkdownxWidget()
        widget_html = w.render('comment', value, {})
    else:
        markdownify = import_string('markdownx.utils.markdownify')
        md = markdownify(value)
    return render(request, 'detail.html', {'report': report, 'markdownx_editor': widget_html, 'is_editor': is_editor, 'markdownx_md': md})




def is_user_an_editor(request):
    groups = [g.name for g in request.user.groups.all()]
    return 'editor' in groups

@csrf_exempt
@login_required
def update_comment(request):
    if not is_user_an_editor(request):
        return HttpResponseForbidden()
    report_id = int(request.POST.get('report_id', -1)) 
    comment = request.POST.get('comment', '')
    data = {'comment': comment, 'report_id': report_id}
    headers = {'Authorization': 'Token %s' % API_SERVER_TOKEN}
    r = requests.post(API_HOST + '/api/report/update_comment', data=data, headers=headers)
    print(r.status_code)
    return redirect('/report/' + str(report_id) + '/')


@csrf_exempt
@login_required
def proxy_markdown_upload_view(request):
    if not is_user_an_editor(request):
        return HttpResponseForbidden()
    remote_url = API_HOST + '/markdownx/upload/'
    return proxy_view(request, remote_url, {})

@csrf_exempt
@login_required
def proxy_markdownify_view(request):
    if not is_user_an_editor(request):
        return HttpResponseForbidden()
    remote_url = API_HOST + '/markdownx/markdownify/'
    return proxy_view(request, remote_url, {})
