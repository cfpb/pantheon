from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from osw import forms
from osw import models
from github.client import GitHub, GitHubEnterprise, GitHubAdmin, get_org_name, is_org_member, is_2fa_enabled
from django.conf import settings
from django.contrib import messages

def release_existing(request):
    return HttpResponse('release existing repo')

def start_new(request):
    return HttpResponse('start new repo')



def two_factor_audit(request):
    context = RequestContext(request)

    # first check if the user is a member of the primary team:
    pipeline_kwargs = request.session.get('partial_pipeline', {}).get('kwargs')
    if not pipeline_kwargs:
        return redirect('home')

    details = pipeline_kwargs['details']
    username = details['username']

    gha = GitHubAdmin()

    github_details = {}
    org_name = github_details['org_name'] = get_org_name(gha, settings.GH_ORG_IDS[0])
    is_member = github_details['is_member'] = is_org_member(gha, username, org_name)
    twofa_enabled = github_details['2fa_enabled'] = False

    if is_member:
        # if already a member, then just check for 2fa
        twofa_enabled = github_details['2fa_enabled'] = is_2fa_enabled(gha, username, org_name)


    request.session['github_details'] = github_details

    if is_member and not twofa_enabled:
        context.update(github_details)
        return render_to_response('osw/two_factor_audit.html', context)
    else:
        return HttpResponseRedirect('/complete/github')


def github_details(request):
    context = RequestContext(request)

    pipeline_kwargs = request.session.get('partial_pipeline', {}).get('kwargs')
    if not pipeline_kwargs:
        return redirect('home')

    github_details = request.session['github_details']
    org_name = github_details['org_name']

    details = pipeline_kwargs['details']
    username = details['username']

    gh = GitHub(access_token=pipeline_kwargs['response']['access_token'])

    def build_name_form(data=None):
        gh_name = github_details['gh_name']
        ghe_name = github_details['ghe_name']
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
        is_public_member = github_details['is_public_member'] = github_details['is_member'] and is_org_member(gh, username, org_name, public=True)
        if not is_public_member:
            return forms.PublicizeForm(data=data)
        else:
            return None

    def build_pub_key_form(data=None):
        gh_pub_keys = set([key['key'] for key in github_details['gh_pub_keys']])
        ghe_pub_keys = set([key['key'] for key in github_details['ghe_pub_keys']])
        if gh_pub_keys.intersection(ghe_pub_keys):
            return None
        pub_key_form = forms.PubKeyForm(initial={'key_name': 'cfpb laptop'}, data=data)
        pub_key_form.fields['key_to_add'].choices = [(key['title'], key['title']) for key in github_details['ghe_pub_keys']]
        return pub_key_form

    def build_two_fa_form(data=None):
        is_member = github_details['is_member']
        if is_member:
            return None
        else:
            return forms.TwoFactorAuthForm(data=data)

    def process_membership_request(user_extension_data):
        user_extension = models.UserExtension.objects.create(**user_extension_data)

        if github_details['is_member']:
            user_extension.existing_approval()
            user_extension.save()
            messages.info(request, 'You are already an org member')
        else:
            messages.info(request, 'Org membership request pending.')

    if request.method == 'GET':
        ghe = GitHubEnterprise(request.user)
        github_details.update({
            'gh_name': details['fullname'],
            'ghe_name': ghe.user.get().json()['name'],
            'ghe_pub_keys': ghe.user.keys.get().json(),
            'gh_pub_keys': gh.user.keys.get().json(),
        })
    
        context.update({
            'name_form': build_name_form(),
            'publicize_form': build_publicize_form(),
            'pub_key_form': build_pub_key_form(),
            'gh_pub_keys': [key['title'] for key in github_details['gh_pub_keys']],
            'two_fa_form': build_two_fa_form(),
        })
        if context['publicize_form'] is None and context['name_form'] is None and context['pub_key_form'] is None:
            request.session.pop('github_details', None)
            process_membership_request({'user': request.user})
            return HttpResponseRedirect('/complete/github')

        request.session['github_details'] = github_details
        return render_to_response('osw/github_details.html', context)

    if request.method == 'POST':
        is_member = github_details['is_member']
        user_extension_data = {'user': request.user}
        # generate forms and validate
        name_form = build_name_form(data=request.POST)
        publicize_form = build_publicize_form(data=request.POST)
        pub_key_form = build_pub_key_form(data=request.POST)
        two_fa_form = build_two_fa_form(data=request.POST)

        if publicize_form and not publicize_form.is_valid() or \
           name_form and not name_form.is_valid() or \
           pub_key_form and not pub_key_form.is_valid() or\
           two_fa_form and not two_fa_form.is_valid():
            context.update({
                'gh_pub_keys': [key['title'] for key in github_details['gh_pub_keys']],
                'publicize_form': publicize_form,
                'name_form': name_form,
                'pub_key_form': pub_key_form,
                'two_fa_form': two_fa_form,
            })
            return render_to_response('osw/github_details.html', context)

        # update user name
        if name_form:
            name_data = name_form.cleaned_data
            if name_data['update_public_name']:
                gh.user.patch(data={'name': name_data['updated_name']})
                messages.success(request, 'Public GitHub name updated.')

        # publicize org membership
        if publicize_form:
            if publicize_form.cleaned_data['make_membership_public']:
                if is_member:
                    gh.orgs._(org_name).public_members._(username).put()
                    messages.success(request, 'Org membership made public.')
                else:
                    user_extension_data['publicize_membership'] = True

        # copy GHE public key to GH
        if pub_key_form:
            pub_key_data = pub_key_form.cleaned_data
            if pub_key_data['add_public_key']:
                pub_key = [key for key in github_details['ghe_pub_keys'] if key['title'] == pub_key_data['key_to_add']][0]
                pub_key_req = {'title': pub_key_data['key_name'], 'key': pub_key['key']}
                gh.user.keys.POST(data=pub_key_req)
                messages.success(request, "Enterprise public key added as '{}'".format(pub_key_data['key_name']))

        # as long as two factor form is checked, we don't have to do anything.


        process_membership_request(user_extension_data)
        request.session.pop('github_details', None)
        return HttpResponseRedirect('/complete/github')
