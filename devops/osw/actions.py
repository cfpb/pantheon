from django.core.urlresolvers import reverse

"""
        * short_title - 1-2 words suitable for a tab/button
        * long_title - descriptive title
        * description - 1-2 sentences describing action
        * cta - short call to action placed on button 
        * action - url to go to when cta clicked
        * method (default: GET) - POST or GET
        * form (optional) - form to display under description, before CTA
"""

def openSource(request, context, repo):
    if repo.is_enterprise:
        return {
            'short_title': 'Open Source',
            'name': 'Open Source',
            'title': 'Publish this Repo on GitHub.com',
            'description': 'Start the process to open source {}. A wizard will walk you through the items that must be complete.'.format(repo.full_name),
            'cta': 'Open The Source',
            'action': reverse('osw:release_existing'),
        }
    else:
        return {}
