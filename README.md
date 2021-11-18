# Ansible

A configuration-as-code repository for managing the jlumley.com domain 


## Getting Started

1. `pip install ansible`
2. `git clone https://gitlab.com/jlumley/ansible.git`
3. `ansible-galaxy install -r requirements.yml`
4. `ssh-copy-id -i ~/.ssh/id_rsa.pub root@<host>`
5. `ansible-playbook -i inventory/hosts.yml playbooks/playbook.yml`