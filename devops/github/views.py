from django.contrib import messages
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from github.models import Repo
from appring import apps
from django.apps import apps as djangoapps
from django.template import RequestContext

# Create your views here.
def refresh(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed()
    elif request.user.is_authenticated:
        Repo.objects.sync_user(request.user)
        messages.success(request, 'Repositories refreshed')
    else:
        messages.error(request, 'You must login')
    return HttpResponseRedirect('/')

