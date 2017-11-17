#!/usr/bin/python
# -*- mode: python -*-

# Copyright 2015 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

DOCUMENTATION = '''
---
module: ucsm_vhba_template
short_description: Create, modify or remove vhba template

description:
  - Verifies vhba template is present or absent.
  - If present and desired config is not present, apply settings. If vhba template is not present, create and apply desired settings.
  - If the desired state is 'absent', remove vhba template if it is currently present

version_added: "0.1.0"
author:
    - "Cisco UCS Team"
    - "Pavan Koundinya"
'''

import sys
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.mometa.vnic.VnicSanConnTempl import VnicSanConnTempl
from ucsmsdk.mometa.vnic.VnicFcIf import VnicFcIf
import json
import pickle
import ucs_login
import ucs_logout


def vhba_template(input):
    vhba_template = input
    results = {}
    ucs_handle = pickle.loads(str(ucs_login.main(vhba_template['ip'], vhba_template['username'], vhba_template['password'])))

    # set default params
    if not vhba_template.get('descr'):
        vhba_template['descr'] = ''
    if not vhba_template.get('fabric'):
        vhba_template['fabric'] = 'A'
    if not vhba_template.get('redundancy_type'):
        vhba_template['redundancy_type'] = 'none'
    if not vhba_template.get('vsan'):
        vhba_template['vsan'] = 'default'
    if not vhba_template.get('template_type'):
        vhba_template['template_type'] = 'initial-template'
    if not vhba_template.get('max_data'):
        vhba_template['max_data'] = '2048'
    if not vhba_template.get('wwpn_pool'):
        vhba_template['wwpn_pool'] = 'default'
    if not vhba_template.get('qos_policy'):
        vhba_template['qos_policy'] = ''
    if not vhba_template.get('pin_group'):
        vhba_template['pin_group'] = ''
    if not vhba_template.get('stats_policy'):
        vhba_template['stats_policy'] = 'default'
    if not vhba_template.get('org_dn'):
        vhba_template['org_dn'] = 'org-root'

    changed = False
    if vhba_template['state'] == 'present':
        results['expected'] = True
    else:
        results['expected'] = False
    results['name'] = vhba_template['name']
    try:
        exists = False
        # dn is <org_dn>/san-conn-templ-<name>
        dn = vhba_template['org_dn'] + '/san-conn-templ-' + vhba_template['name']

        mo = ucs_handle.query_dn(dn)
        if mo:
            # check top-level mo props
            kwargs = {}
            kwargs['descr'] = vhba_template['descr']
            kwargs['switch_id'] = vhba_template['fabric']
            kwargs['redundancy_pair_type'] = vhba_template['redundancy_type']
            kwargs['templ_type'] = vhba_template['template_type']
            kwargs['max_data_field_size'] = vhba_template['max_data']
            kwargs['ident_pool_name'] = vhba_template['wwpn_pool']
            kwargs['qos_policy_name'] = vhba_template['qos_policy']
            kwargs['pin_to_group_name'] = vhba_template['pin_group']
            kwargs['stats_policy_name'] = vhba_template['stats_policy']
            if (mo.check_prop_match(**kwargs)):
                # top-level props match, check next level mo/props
                child_dn = dn + '/if-default'
                mo_1 = ucs_handle.query_dn(child_dn)
                if mo_1:
                    kwargs = {}
                    kwargs['name'] = vhba_template['vsan']
                    if (mo_1.check_prop_match(**kwargs)):
                        exists = True

        if vhba_template['state'] == 'absent':
            if exists:
                if not vhba_template['check_exists']:
                    ucs_handle.remove_mo(mo)
                    ucs_handle.commit()
                changed = True
                results['removed'] = True
        else:
            # create/modify for state 'present'
            results['removed'] = False
            if not exists:
                if not vhba_template['check_exists']:
                    # create if mo does not already exist
                    mo = VnicSanConnTempl(parent_mo_or_dn=vhba_template['org_dn'],
                                          name=vhba_template['name'],
                                          descr=vhba_template['descr'],
                                          switch_id=vhba_template['fabric'],
                                          redundancy_pair_type=vhba_template['redundancy_type'],
                                          templ_type=vhba_template['template_type'],
                                          max_data_field_size=vhba_template['max_data'],
                                          ident_pool_name=vhba_template['wwpn_pool'],
                                          qos_policy_name=vhba_template['qos_policy'],
                                          pin_to_group_name=vhba_template['pin_group'],
                                          stats_policy_name=vhba_template['stats_policy'])

                    mo_1 = VnicFcIf(parent_mo_or_dn=mo, name=vhba_template['vsan'])

                    ucs_handle.add_mo(mo, True)
                    ucs_handle.commit()
                changed = True
                results['created'] = True

    except Exception as e:
        err = True
        results['msg'] = "setup error: %s " % str(e)

    results['changed'] = changed
    results['present'] = exists

    ucs_handle = pickle.dumps(ucs_handle)
    ucs_logout.main(ucs_handle)
    return results


def main():
    json_input = json.loads(sys.argv[1])
    results = vhba_template(json_input)
    resultsjson = json.dumps(results)
    print(resultsjson)
    return resultsjson

if __name__ == '__main__':
    main()
