DevDash
=======
Installation
------------
The easiest way to run the system is to use vagrant.

Prerequisites:
  * [Vagrant](https://www.vagrantup.com/)
  * [Vagrant-Cachier](http://fgrehm.viewdocs.io/vagrant-cachier) - `vagrant plugin install vagrant-cachier`
  * [Virtualbox](https://www.vagrantup.com/)
  * [Ansible](http://www.ansible.com/) (if using mac w/o root install with `brew install ansible`, otherwise use pip)
  * Fork and check out the following repos as siblings of each other:
    * cfpb/devdash (this repo)
    * cfpb/kratos (authorizion microserver)
    * cfpb/moirai (AWS EC2 management microserver)
    * cfpb/dash (web client)

1. add Kratos secret setting to `../kratos/src/config_secret.iced`
1. add Moirai secret setting to `../moirai/src/config_secret.iced`
1. add Django secret settings to `./devdash/devdash/settings_secret.py`
1. `vagrant up`
1. `vagrant ssh`
1. load data from github:
  1. `cd /opt/kratos`
  1. `icake -n devdesign import_from_gh`
1. You can start the worker but **starting the worker will propagate all changes to the resources!**:
  1. `cd /opt/kratos`
  1. `icake runworker`
1. visit the website in your browser: `localhost:8000`
1. visit the database in your browser: `localhost:5984`

Development
-----------
* Commit all node dependencies
* run `/vagrant/devdash/manage.py collectstatic` prior to any commits that change static files
* see `devdash/frontend/README.md` for front-end instructions
