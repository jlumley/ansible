# Ansible

A configuration-as-code repository for managing the jlumley.com domain 


## Getting Started

1. `sudo apt install git vim python3 python3-pip rsync`
1. `python3 -m pip install --user ansible pykeepass`
1. `mkdir git && cd git`
1. `git config --global user.name "Jeremy Lumley"`
1. `git config --global user.email "Jeremy.lumley96@gmail.com"`
1. `git config --global core.editor vim`
1. `ssh-keygen`
1. `echo "add ssh keys to github"`
1. `git clone git@github.com:jlumley/ansible.git`
1. `git clone git@github.com:jlumley/dotfiles.git`
1. `ansible-galaxy install -r requirements.yml`
1. `ssh-copy-id -i ~/.ssh/id_rsa.pub jlumley@<host>`
1. `ansible-playbook -i inventory/hosts.yml playbooks/playbook.yml`
