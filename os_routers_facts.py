#!/usr/bin/python

# Copyright (c) Atos Global Delivery Center
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '0.1',
                    'status': ['preview']}

DOCUMENTATION = '''
---
module: os_routers_facts
short_description: Retrieve facts about one or more OpenStack routers.
author: "Piotr Kochanowski"
description:
    - Retrieve facts about one or more routerss from OpenStack.
requirements:
    - "python >= 2.7"
    - "openstacksdk"
options:
   name:
     description: 
        - Name of the router
   filters:
     description:
        - A dictionary of meta data to use for filtering.  Elements of
          this dictionary may be additional dictionaries.
     required: false
   availability_zone:
     description:
       - Ignored. Present for backwards compatibility
     required: false
'''

EXAMPLES = '''
- name: Gather facts about previously created routers
  os_routers_facts:
    auth:
      auth_url: https://identity.example.com
      username: user
      password: password
      project_name: someproject

- name: Show openstack routers
  debug:
    var: openstack_routers

- name: Gather facts about a previously created router by name
  os_routers_facts:
    auth:
      auth_url: https://identity.example.com
      username: user
      password: password
      project_name: someproject
    name:  router1

- name: Show openstack routers
  debug:
    var: openstack_routers

- name: Gather facts about a previously created router with other filter
  # Note: name and filters parameters are Not mutually exclusive
  os_routers_facts:
    auth:
      auth_url: https://identity.example.com
      username: user
      password: password
      project_name: someproject
    filters:
      project_id: 55e2ce24b2a245b09f181bf025724cbe

- name: Show openstack routers
  debug:
    var: openstack_routers
'''

RETURN = '''
openstack_routers:
    description: has all the openstack facts about the routers
    returned: always, but can be null
    type: complex
    contains:
        id:
            description: Unique UUID.
            returned: success
            type: string
        name:
            description: Name given to the router.
            returned: success
            type: string
        status:
            description: Router status.
            returned: success
            type: string
        routes:
            description: Routes configured in this router.
            returned: success
            type: list of strings
        external_gateway_info:
            description: Information about external IPs and SNAT.
            returned: success
            type: dictionaries
        tenant_id:
            description: Tenant id associated with this router.
            returned: success
            type: string
        description:
            description: Description of the router.
            returned: success
            type: string
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.openstack import openstack_full_argument_spec, openstack_cloud_from_module


def main():

    argument_spec = openstack_full_argument_spec(
        name=dict(required=False, default=None),
        filters=dict(required=False, type='dict', default=None)
    )
    module = AnsibleModule(argument_spec)

    sdk, cloud = openstack_cloud_from_module(module)
    try:
        routers = cloud.search_routers(module.params['name'], module.params['filters'])
        module.exit_json(changed=False, ansible_facts=dict(
            openstack_routers=routers))

    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
