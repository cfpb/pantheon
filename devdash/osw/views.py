from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from osw import forms
from osw import models
from github.client import GitHub, GitHubEnterprise, GitHubAdmin
from django.conf import settings
from django.contrib import messages

gha = GitHubAdmin()

def release_existing(request):
    return HttpResponse('release existing repo')

def start_new(request):
    return HttpResponse('start new repo')

def enable_2fa(request):
    pipeline_kwargs = request.session.get('partial_pipeline', {}).get('kwargs')
    if not pipeline_kwargs:
        return redirect('home')

    context = RequestContext(request)
    return render_to_response('osw/enable_2fa.html', context)

def join_org(request):
    pipeline_kwargs = request.session.get('partial_pipeline', {}).get('kwargs')
    if not pipeline_kwargs:
        return redirect('home')

    username = pipeline_kwargs['details']['username']


    welcome_team = settings.GH_WELCOME_TEAM
    gha.teams._(str(welcome_team)).memberships._(username).put()

    context = RequestContext(request)
    return render_to_response('osw/join_org.html', context)


def gh_details(request):
    context = RequestContext(request)

    pipeline_kwargs = request.session.get('partial_pipeline', {}).get('kwargs')
    if not pipeline_kwargs:
        return redirect('home')

    gh = GitHub(access_token=pipeline_kwargs['response']['access_token'])

    details = pipeline_kwargs['details']
    username = details['username']
    gh_details = request.session['gh_details']

    def build_name_form(data=None):
        gh_name = gh_details['gh_name']
        ghe_name = gh_details['ghe_name']
        if gh_name == ghe_name:
            return None
        name_form = forms.NameForm(initial={'updated_name': ghe_name}, data=data)
        if gh_name:
            help_text = 'Your public GitHub name ({}) differs from your enterprise name.'.format(gh_name)
        else:
            help_text = 'You do not have a public GitHub name.'
        help_text += ' Updating your public name will make it easier for your colleagues to find you.'
        name_form.fields['update_public_name'].help_text = help_text
        return name_form

    def build_publicize_form(data=None):
        # only check if the member has publicized their membership if they have a member to publicize
        if not gh_details['is_public_member']:
            return forms.PublicizeForm(data=data)
        else:
            return None

    def build_pub_key_form(data=None):
        gh_pub_keys = set([key['key'] for key in gh_details['gh_pub_keys']])
        ghe_pub_keys = set([key['key'] for key in gh_details['ghe_pub_keys']])
        if gh_pub_keys.intersection(ghe_pub_keys):
            return None
        pub_key_form = forms.PubKeyForm(initial={'key_name': 'cfpb laptop'}, data=data)
        pub_key_form.fields['key_to_add'].choices = [(key['title'], key['title']) for key in gh_details['ghe_pub_keys']]
        return pub_key_form

    if request.method == 'GET':
        ghe = GitHubEnterprise(request.user)
        gh_details.update({
            'gh_name': details['fullname'],
            'ghe_name': ghe.user.get().json()['name'],
            'ghe_pub_keys': ghe.user.keys.get().json(),
            'gh_pub_keys': gh.user.keys.get().json(),
        })
    
        context.update({
            'name_form': build_name_form(),
            'publicize_form': build_publicize_form(),
            'pub_key_form': build_pub_key_form(),
            'gh_pub_keys': [key['title'] for key in gh_details['gh_pub_keys']],
        })
        if context['publicize_form'] is None and context['name_form'] is None and context['pub_key_form'] is None:
            messages.success(request, 'Welcome to our org.')
            request.session.pop('gh_details', None)
            return HttpResponseRedirect('/complete/github')

        request.session['gh_details'] = gh_details
        return render_to_response('osw/gh_details.html', context)

    if request.method == 'POST':
        # generate forms and validate
        name_form = build_name_form(data=request.POST)
        publicize_form = build_publicize_form(data=request.POST)
        pub_key_form = build_pub_key_form(data=request.POST)

        if publicize_form and not publicize_form.is_valid() or \
           name_form and not name_form.is_valid() or \
           pub_key_form and not pub_key_form.is_valid():
            context.update({
                'gh_pub_keys': [key['title'] for key in gh_details['gh_pub_keys']],
                'publicize_form': publicize_form,
                'name_form': name_form,
                'pub_key_form': pub_key_form,
            })
            return render_to_response('osw/gh_details.html', context)

        # update user name
        if name_form:
            name_data = name_form.cleaned_data
            if name_data['update_public_name']:
                resp = gh.user.patch(data={'name': name_data['updated_name']})
                print resp
                print resp.json()
                messages.success(request, 'Public GitHub name updated.')

        # publicize org membership
        if publicize_form:
            if publicize_form.cleaned_data['make_membership_public']:
                gh.orgs._(gh_details['org_name']).public_members._(username).put()
                messages.success(request, 'Org membership made public.')

        # copy GHE public key to GH
        if pub_key_form:
            pub_key_data = pub_key_form.cleaned_data
            if pub_key_data['add_public_key']:
                pub_key = [key for key in gh_details['ghe_pub_keys'] if key['title'] == pub_key_data['key_to_add']][0]
                pub_key_req = {'title': pub_key_data['key_name'], 'key': pub_key['key']}
                resp = gh.user.keys.POST(data=pub_key_req)
                print resp
                print resp.json()
                messages.success(request, "Enterprise public key added as '{}'".format(pub_key_data['key_name']))
        

        messages.success(request, 'Welcome to our org.')
        request.session.pop('gh_details', None)
        return HttpResponseRedirect('/complete/github')
