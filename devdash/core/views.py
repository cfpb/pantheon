from django.shortcuts import render_to_response, redirect
from django.contrib.auth import logout
from tiles.views import gen_context
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
import core.sync
from django.conf import settings

# Create your views here.
def sync(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed()
    elif request.user.is_authenticated:
        core.sync.sync(request.user)
        messages.success(request, 'Repositories refreshed')
    else:
        messages.error(request, 'You must login')
    return HttpResponseRedirect('/')


def home(request):
    return HttpResponseRedirect('/static/dash.html')
    context = RequestContext(request)

    if request.user.is_authenticated():
        context['tiles'] = []
        context = gen_context(request, settings.HOME_TILES, context, context['tiles'])

    return render_to_response('core/home.html', context)

def logout_view(request):
    logout(request)
    return redirect('/static/dash.html')
    return redirect('/')

def login(request):
    user = request.user
    if user.is_authenticated():
        logout(request)
    return HttpResponseRedirect('/login/github-enterprise/?next=/login_continue')

def login_continue(request):
    user = request.user
    try:
        user.social_auth.get(provider='github')
    except user.social_auth.model.DoesNotExist:
        return HttpResponseRedirect('/login/github/?next=/static/dash.html')
    else:
        return HttpResponseRedirect('/static/dash.html')
