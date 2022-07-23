# Ansible

A configuration-as-code repository for managing the jlumley.com domain 


## Getting Started

1. `sudo apt install git vim python3 python3-pip`
2. `python3 -m pip install --user ansible`
3. `mkdir git && cd git`
4. `git config --global user.name "Jeremy Lumley"`
5. `git config --global user.email "Jeremy.lumley96@gmail.com"`
6. `git config --global core.editor vim`
7. `ssh-keygen`
8. `echo "add ssh keys to github"`
4. `git clone git@github.com:jlumley/ansible.git`
5. `ansible-galaxy install -r requirements.yml`
6. `ssh-copy-id -i ~/.ssh/id_rsa.pub jlumley@<host>`
7. `ansible-playbook -i inventory/hosts.yml playbooks/playbook.yml`
