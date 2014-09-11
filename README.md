open-source-wizard
==================


Developer Dashboard lets developers see the status of their code,
and the actions they can perform on that code, all in one place.

In order support this, DevDash is modular and pluggable.


## settings.SYNC = tuple('app_name', 'app_name', ...)
(core)

Each app_name app must have a sync.py file that contains a sync(user=None) function. 
If a user is passed, then all information for that user must be synced.
If user is None, then all data in the database must be synced.

## settings.GHE_REPO_ACTIONS = tuple('app_name.action_name', 'app_name.action_name', ...)
## settings.GH_REPO_ACTIONS = tuple('app_name.action_name', 'app_name.action_name', ...)
(github tile)

Each app_name app must have an actions.py file that contains an action_name(request, context, repo) function.
The function must return a dict with the following keys:

    * short_title - 1-2 words suitable for a tab/button
    * long_title - descriptive title
    * description - 1-2 sentences describing action
    * cta - short call to action placed on button 
    * action - url to go to when cta clicked
    * method (default: GET) - POST or GET
    * form (optional) - form to display under description, before CTA

GHE_REPO_ACTIONS actions will be displayed next to each Github Enterprise repo.
GH_REPO_ACTIONS actions will be displayed next to each public github repo.
If you do not want an action displayed for a particular repo, return an empty dict.
