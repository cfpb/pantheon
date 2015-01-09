from django.core.urlresolvers import reverse
from jenkins.models import Job
"""
        * short_title - 1-2 words suitable for a tab/button
        * long_title - descriptive title
        * description - 1-2 sentences describing action
        * cta - short call to action placed on button 
        * action - url to go to when cta clicked
        * method (default: GET) - POST or GET
        * form (optional) - form to display under description, before CTA
"""

def createJob(request, context, repo):
    if not repo.is_enterprise:
        return {}
    try:
        Job.objects.get(repo=repo)
    except:
        return {
            'short_title': 'Continuous Integration',
            'name': 'Jenkins CI Job',
            'title': 'Create a Job to Continuously test/build this repo',
            'description': """
                Use Jenkins to continuously test/build {}. In addition to creating the
                CI job here, you will need to add a .travis.yml file. See 
                <a href="http://docs.travis-ci.com/user/build-configuration/">the 
                .travis.yml docs</a> for more information. Our implemention supports:
                <ul><li>env</li><li>before_install</li><li>install</li><li>before_script</li>
                <li>script</li><li>after_script</li><li>after_success</li><li>after_failure</li></ul>
                """.format(repo.full_name),
            'cta': 'Create Continuous Integration Job',
            'action': reverse('jenkins:initialize_ci'),
        }
    else:
        return {}
