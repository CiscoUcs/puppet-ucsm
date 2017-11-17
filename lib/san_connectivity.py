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
module: ucsm_san_connectivity
short_description: Create, modify or remove san connectivity

description:
  - Verifies san connectivity is present or absent.
  - If present and desired config is not present, apply settings. If san connectivity is not present, create and apply desired settings.
  - If the desired state is 'absent', remove san connectivity if it is currently present

version_added: "0.1.0"
author:
    - "Cisco UCS Team"
    - "Pavan Koundinya"
'''

import sys
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.mometa.vnic.VnicSanConnPolicy import VnicSanConnPolicy
from ucsmsdk.mometa.vnic.VnicFcNode import VnicFcNode
from ucsmsdk.mometa.vnic.VnicFc import VnicFc
from ucsmsdk.mometa.vnic.VnicFcIf import VnicFcIf
import json
import pickle
import ucs_login
import ucs_logout


def san_connectivity(input):
    san_connectivity = input
    results = {}
    ucs_handle = pickle.loads(str(ucs_login.main(san_connectivity['ip'], san_connectivity['username'], san_connectivity['password'])))

    # set default params
    if not san_connectivity.get('descr'):
        san_connectivity['descr'] = ''
    if not san_connectivity.get('wwnn_pool'):
        san_connectivity['wwnn_pool'] = 'default'
    if not san_connectivity.get('org_dn'):
        san_connectivity['org_dn'] = 'org-root'
    for vhba in san_connectivity['vhba_list']:
        if not vhba.get('adapter_policy'):
            vhba['adapter_policy'] = ''

    changed = False
    if san_connectivity['state'] == 'present':
        results['expected'] = True
    else:
        results['expected'] = False
    results['name'] = san_connectivity['name']
    try:
        exists = False
        # dn is <org_dn>/san-conn-pol-<name>
        dn = san_connectivity['org_dn'] + '/san-conn-pol-' + san_connectivity['name']

        mo = ucs_handle.query_dn(dn)
        if mo:
            # check top-level mo props
            kwargs = {}
            kwargs['descr'] = san_connectivity['descr']
            if (mo.check_prop_match(**kwargs)):
                # top-level props match, check next level mo/props
                # vnicFcNode object
                child_dn = dn + '/fc-node'
                mo_1 = ucs_handle.query_dn(child_dn)
                if mo_1:
                    kwargs = {}
                    kwargs['ident_pool_name'] = san_connectivity['wwnn_pool']
                    if (mo_1.check_prop_match(**kwargs)):
                        if len(san_connectivity['vhba_list']) == 0:
                            exists = True
                        else:
                            # check vnicFc props
                            for vhba in san_connectivity['vhba_list']:
                                child_dn = dn + '/fc-' + vhba['name']
                                mo_2 = ucs.login_handle.query_dn(child_dn)
                                kwargs = {}
                                kwargs['adaptor_profile_name'] = vhba['adapter_policy']
                                kwargs['order'] = vhba['order']
                                kwargs['nw_templ_name'] = vhba['vhba_template']
                                if (mo_2.check_prop_match(**kwargs)):
                                    exists = True

        if san_connectivity['state'] == 'absent':
            if exists:
                if not san_connectivity['check_exists']:
                    ucs_handle.remove_mo(mo)
                    ucs_handle.commit()
                changed = True
                results['removed'] = True
        else:
            # create/modify for state 'present'
            results['removed'] = False
            if not exists:
                if not san_connectivity['check_exists']:
                    # create if mo does not already exist
                    mo = VnicSanConnPolicy(parent_mo_or_dn=san_connectivity['org_dn'],
                                           name=san_connectivity['name'],
                                           descr=san_connectivity['descr'])
                    mo_1 = VnicFcNode(parent_mo_or_dn=mo,
                                      ident_pool_name=san_connectivity['wwnn_pool'],
                                      addr='pool-derived')
                    for vhba in san_connectivity['vhba_list']:
                        mo_2 = VnicFc(parent_mo_or_dn=mo,
                                      name=vhba['name'],
                                      adaptor_profile_name=vhba['adapter_policy'],
                                      nw_templ_name=vhba['vhba_template'],
                                      order=vhba['order'])
                        mo_2_1 = VnicFcIf(parent_mo_or_dn=mo_2, name='default')

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
    results = san_connectivity(json_input)
    resultsjson = json.dumps(results)
    print(resultsjson)
    return resultsjson

if __name__ == '__main__':
    main()
