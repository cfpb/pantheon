from django.contrib import messages
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render_to_response
from github.models import Repo
from django.template import RequestContext
from github import forms

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


def enterprise_details(request):
    context = RequestContext(request)
    if request.method == 'GET':
        details = request.session['partial_pipeline']['kwargs']['details']
        details.setdefault('contractor', True)
        form = forms.EnterpriseDetailsForm(data=details)
        form.is_valid()
        context['form'] = form
        return render_to_response('github/enterprise_details.html', context)
    if request.method == 'POST':
        form = forms.EnterpriseDetailsForm(request.POST)
        if form.is_valid():
            request.session['enterprise_details'] = form.cleaned_data
            return HttpResponseRedirect('/complete/github-enterprise')
        else:
            context['form'] = form
            return render_to_response('github/enterprise_details.html', context)
