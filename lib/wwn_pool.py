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
module: ucsm_wwn_pool
short_description: Create, modify or remove wwn pool

description:
  - Verifies wwn pool is present or absent.
  - If present and desired config is not present, apply settings. If wwn pool is not present, create and apply desired settings.
  - If the desired state is 'absent', remove wwn pool if it is currently present

version_added: "0.1.0"
author:
    - "Cisco UCS Team"
    - "Pavan Koundinya"
'''

import sys
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.mometa.fcpool.FcpoolInitiators import FcpoolInitiators
from ucsmsdk.mometa.fcpool.FcpoolBlock import FcpoolBlock
import json
import pickle
import ucs_login
import ucs_logout


def wwn_pool(input):
    wwn = input
    results = {}
    ucs_handle = pickle.loads(str(ucs_login.main(wwn['ip'], wwn['username'], wwn['password'])))

    # set default params
    if not wwn.get('descr'):
        wwn['descr'] = ''
    if not wwn.get('order'):
        wwn['order'] = 'default'
    if not wwn.get('org_dn'):
        wwn['org_dn'] = 'org-root'
    if not wwn.get('state'):
        wwn['state'] = 'present'
    # append purpose param with suffix used by UCSM
    purpose_param = wwn['purpose'] + '-wwn-assignment'
    changed = False
    if wwn['state'] == 'present':
        results['expected'] = True
    else:
        results['expected'] = False
    results['name'] = wwn['name']
    try:
        exists = False
        # dn is <org_dn>/wwn-pool-<name> for WWNN or WWPN
        dn = wwn['org_dn'] + '/wwn-pool-' + wwn['name']

        mo = ucs_handle.query_dn(dn)
        if mo:
            obj = {}
            obj['name'] = mo.name
            obj['descr'] = mo.descr
            # check top-level mo props
            kwargs = {}
            kwargs['assignment_order'] = wwn['order']
            kwargs['descr'] = wwn['descr']
            kwargs['purpose'] = purpose_param
            if (mo.check_prop_match(**kwargs)):
                # top-level props match, check next level mo/props
                if 'to' in wwn and 'r_from' in wwn:
                    block_dn = dn + '/block-' + wwn['r_from'].upper() + '-' + wwn['to'].upper()
                    mo_1 = ucs_handle.query_dn(block_dn)
                    if mo_1:
                        exists = True
                else:
                    exists = True

        if wwn['state'] == 'absent':
            if exists:
                if not wwn['check_exists']:
                    ucs_handle.remove_mo(mo)
                    ucs_handle.commit()
                changed = True
                results['removed'] = True
        else:
            # create/modify for state 'present'
            results['removed'] = False
            if not exists:
                if not wwn['check_exists']:
                    # create if mo does not already exist
                    mo = FcpoolInitiators(parent_mo_or_dn=wwn['org_dn'],
                                          name=wwn['name'],
                                          assignment_order=wwn['order'],
                                          purpose=purpose_param)
                    if 'to' in wwn and 'r_from' in wwn:
                        mo_1 = FcpoolBlock(parent_mo_or_dn=mo,
                                           to=wwn['to'],
                                           r_from=wwn['r_from'])

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
    results = wwn_pool(json_input)
    resultsjson = json.dumps(results)
    print(resultsjson)
    return resultsjson

if __name__ == '__main__':
    main()
