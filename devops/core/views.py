from django.shortcuts import render_to_response, redirect
from django.contrib.auth import logout
from tiles.views import gen_context
from django.template import RequestContext

def home(request):
    if request.user.is_authenticated():
        context = gen_context(request)
    else:
        context = RequestContext(request)

    return render_to_response('core/home.html', context)

def logout_view(request):
    logout(request)
    return redirect('/')
