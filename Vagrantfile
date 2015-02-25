# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # vbox name
  config.vm.box = "centos_6_5_64"

  # vbox url
  config.vm.box_url = "https://github.com/2creatives/vagrant-centos/releases/download/v6.5.1/centos65-x86_64-20131205.box"

  # enable package caching
  config.cache.auto_detect = true

  # port forwarding
  config.vm.network :forwarded_port, guest: 80, host: 8000
  config.vm.network :forwarded_port, guest: 5984, host: 5984

  # shared folders
  config.vm.synced_folder "../kratos", "/opt/kratos"
  config.vm.synced_folder "../moirai", "/opt/moirai"
  config.vm.synced_folder "../dash", "/opt/dash"
  
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "ansible/playbook.yml"
    ansible.groups = {
      "vagrant" => ["default"]
    }
  end

  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
  end
end
