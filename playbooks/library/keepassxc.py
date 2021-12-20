#!/usr/bin/python

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ansible-keepassxc

short_description: Module to read credentials from KeePassXC 

version_added: "0.0.1"

description: Module to read credentials from KeePassXC

options:
    database:
        description: Path to database file
        required: true 
        type: str
    password:
        description: Database Password
        required: true 
        type: str
    keyfile:
        description: Path to key file
        required: false 
        type: str
    entry:
        description: Entry name for the attribute to fetch
        required: true
        type: str
    group:
        decription: Group name that the Entry belongs to
        required: false
        type: str

author:
    - Jeremy Lumley (@jlumley)
'''

EXAMPLES = r'''
# Fetch the credentials for the server_1 entry in any group
- name: Fetch server_1 credentials
  jlumley.jlumley.ansible-keepassxc:
    database: "/secrets/db.kdbx"
    password: "s3cure_p4550rd"
    entry: "server_1"

# Fetch the reddit entry in the social group
- name: Fetching reddit credentials 
  jlumley.jlumley.ansible-keepassxc:
    database: "/secrets/db.kdbx"
    password: "sup3r_s3cure_p4550rd"
    entry: "reddit"
    group: "social"
    
# Fetch a custom strig attribute from the github entry
- name: Fetch Github API Token
  jlumley.jlumley.ansible-keepassxc:
    database: "/secrets/db.kdbx"
    password: "d0pe_s3cure_p4550rd"
    keyfile: "/secrets/top_secret_key"
    entry: "github"
    group: "development"
    
'''

RETURN = r'''
# Return values
username:
    description: Username of entry if present
    type: str
    returned: always
    sample: 's3cr3t_us3r'
password:
    description: Password of entry if present
    type: str
    returned: always
    sample: 's3cr3t_p455word'
url:
    description: Url of entry if present
    type: str
    returned: always
    sample: 'http://reddit.com'
custom_fields:
    description: dictionary containing all custom fields 
    type: dict
    returned: always
    sample: False
'''

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
import traceback

IMPORT_ERR = None
try:
    import pykeepass as keepass
except ImportError:
    IMPORT_ERR = traceback.format_exc()

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        database    = dict(type='str', required=True),
        password    = dict(type='str', required=True),
        keyfile     = dict(type='str', required=False, default=None),
        entry       = dict(type='str', required=True),
        group       = dict(type='str', required=False),
    )

    # seed the result dict in the object
    result = dict(
        changed=False,
        username='',
        password='',
        url='',
        custom_fields={}
    )

    # Currently no support for a check_mode this maybe added later if
    # functionality to modify the database is added later
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )
    
    if IMPORT_ERR:
        module.fail_json(
            msg=missing_required_lib("pykeepass"),
            exception=IMPORT_ERR
        )
    
    # unlock local keepass database 
    try:
        kp = keepass.PyKeePass(
            module.params['database'],
            password=module.params['password'],
            keyfile=module.params['keyfile'])
    except keepass.exceptions.CredentialsError:
        module.fail_json(msg='Invalid Credentials')

    # find entry
    entry = kp.find_entries(
        title=module.params['entry'],
        group=module.params['group']
    )

    # fail is entry is not present
    if not entry:
        module.fail_json(msg=f"Unable to find entry: {module.params['entry']}")

    else:
        entry = entry[0]
        custom_field_keys = entry._get_string_field_keys(exclude_reserved=True)
        custom_fields = dict()
        for key in custom_field_keys:
            custom_fields[key] = entry.get_custom_property(key)
        result = dict (
            changed=False,
            username=entry.username,
            password=entry.password,
            url=entry.url,
            custom_fields=custom_fields
        )

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()


