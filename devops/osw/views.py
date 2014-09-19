from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from osw import forms
from osw import models
from github.client import GitHub, GitHubEnterprise, GitHubAdmin, get_org_name, is_org_member, is_team_member, is_2fa_enabled
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
    audit_team_id = str(settings.GH_2FA_AUDIT_TEAM)
    github_details = {}

    gha = GitHubAdmin()
    ghaudit = GitHubAdmin(settings.GH_2FA_ADMIN_CREDENTIALS).headers(accept='application/vnd.github.the-wasp-preview+json')
    org_name = github_details['org_name'] = get_org_name(gha, settings.GH_ORG_IDS[0])

    is_member = github_details['is_member'] = is_org_member(gha, username, org_name)
    is_audit_member = github_details['is_audit_member'] = is_team_member(ghaudit, username, settings.GH_2FA_AUDIT_TEAM)

    twofa_enabled = False
    if is_member:
        # if already a member, then just check for 2fa
        twofa_enabled = github_details['2fa_enabled'] = is_2fa_enabled(gha, username, org_name)
    elif is_audit_member:
        audit_org_name = ghaudit.teams._(audit_team_id).get().json()['organization']['repos_url'].split('/')[-2]
        twofa_enabled = github_details['2fa_enabled'] = is_2fa_enabled(ghaudit, username, audit_org_name)
    else:
        # add user to audit org by adding them to the audit team
        ghaudit.teams._(audit_team_id).memberships._(username).put()

    request.session['github_details'] = github_details
    if twofa_enabled:
        # remove user from audit team
        ghaudit.teams._(audit_team_id).members._(username).delete()
        return HttpResponseRedirect('/complete/github')
    else:
        context.update(github_details)
        return render_to_response('osw/two_factor_audit.html', context)


def github_details(request):
    context = RequestContext(request)
    github_details = request.session['github_details']
    org_name = github_details['org_name']
    pipeline_kwargs = request.session['partial_pipeline']['kwargs']
    details = pipeline_kwargs['details']
    username = details['username']

    gh = GitHub(access_token=pipeline_kwargs['response']['access_token'])

    if request.method == 'GET':

        ghe = GitHubEnterprise(request.user)
        gh_name = github_details['gh_name'] = details['fullname']
        ghe_name = github_details['ghe_name'] = ghe.user.get().json()['name']
        if gh_name != ghe_name:
            name_form = context['name_form'] = forms.NameForm(data={'updated_name': ghe_name})
            if gh_name:
                help_text = 'Your public GitHub name ({}) differs from your enterprise name.'.format(gh_name)
            else:
                help_text = 'You do not have a public GitHub name.'
            help_text += ' Updating your public name will make it easier for your colleagues to find you.'
            name_form.fields['update_public_name'].help_text = help_text

        is_public_member = github_details['is_public_member'] = github_details['is_member'] and is_org_member(gh, username, org_name, public=True)
        if not is_public_member:
            context['publicize_form'] = forms.PublicizeForm()

        request.session['github_details'] = github_details
        return render_to_response('osw/github_details.html', context)

    if request.method == 'POST':
        is_member = github_details['is_member']
        user_extension_data = {'user': request.user}
        # update user name
        name_form = forms.NameForm(data=request.POST)
        name_form.is_valid()
        name_data = name_form.cleaned_data
        if name_data['update_public_name']:
            gh.user.patch(data={'name': name_data['updated_name']})
            messages.success(request, 'Public GitHub name updated.')

        # publicize org membership
        publicize_form = forms.PublicizeForm(data=request.POST)
        publicize_form.is_valid()
        if publicize_form.cleaned_data['make_membership_public']:
            if is_member:
                gh.orgs._(org_name).public_members._(username).put()
            else:
                user_extension_data['publicize_membership'] = True

        user_extension = models.UserExtension.objects.create(**user_extension_data)

        if is_member:
            user_extension.existing_approval()
            user_extension.save()
            messages.info(request, 'You are already an org member')
        else:
            messages.info(request, 'Org membership request pending.')

        request.session.pop('github_details', None)
        return HttpResponseRedirect('/complete/github')
