open-source-wizard
==================o
Installation
------------
The easiest way to run the system is to use vagrant.

Prerequisites:
  * [Vagrant](https://www.vagrantup.com/)
  * [Virtualbox](https://www.vagrantup.com/)
  * [Ansible](http://www.ansible.com/) (if using mac w/o root install with `brew install ansible`, otherwise use pip)
  * you will need to check out both this repo and the cfpb/kratos repo as siblings in the filesystem.

1. add Node secret setting to `../kratos/src/config_secret.iced`
1. add Django secret settings to `./devops/devops/settings_secret.py`
1. `vagrant up`
1. `vagrant ssh`
1. load data from github:
  1. `cd /opt/kratos`
  1. `icake -n devdesign import_from_gh`
1. start the django server
  1. `/vagrant/devops/manage.py runserver 0.0.0.0:8000`
1. start the node server
  1. `cd /opt/kratos`
  1. `icake runtestserver`

Development
-----------
* Commit all node dependencies
* run `/vagrant/devops/manage.py collectstatic` prior to any commits that change static files


Pluggable
---------
Developer Dashboard lets developers see the status of their code,
and the actions they can perform on that code, all in one place.

In order support this, DevDash is modular and pluggable.

### urls.load_namespaced_urls(urlpatterns, 'app_name', 'app_name', ...)
Any apps that have urls.py should be added to this function. 
It will add the urls under `/app_name/`, and namespaces them to `app_name`.
reverse a namespaced url by reverse('app_name:url_name')

### settings.HOME_TILES = tuple('app_name.tile_name', 'app_name.tile_name', ...)
(home page)

Each app_name app must have a tiles.py file that contains a tile_name(request, context) function.
The function must return a context dict with at minimum the following keys:

    * name - unique name for this tile
    * template - the template path used to render this context

These tiles render the primary interfaces for each pluggable component in the dash board.

### settings.SYNC = tuple('app_name', 'app_name', ...)
(core)

Each app_name app must have a sync.py file that contains a sync(user=None) function. 
If a user is passed, then all information for that user must be synced.
If user is None, then all data in the database must be synced.

### settings.GHE_REPO_ACTIONS = tuple('app_name.action_name', 'app_name.action_name', ...)
### settings.GH_REPO_ACTIONS = tuple('app_name.action_name', 'app_name.action_name', ...)
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

### settings.GHE_TILES = tuple('app_name.tile_name', 'app_name.tile_name', ...)
### settings.GH_TILES = tuple('app_name.tile_name', 'app_name.tile_name', ...)
(github tile)

Each app_name app must have a tiles.py file that contains a tile_name(request, context) function.
The function must return a context dict with at minimum the following keys:

    * name - unique name for this tile
    * template - the template path used to render this context

These tiles render actions and alerts at the top of the GitHub and GitHub enterprise repo lists.

