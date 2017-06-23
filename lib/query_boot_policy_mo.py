
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
module: query_boot_policymo
short_description: Checks if boot policy mo with the name exists.

description:
  - Allows to check if boot policy exists. If present, returns true else returns false.
 
version_added: "0.1.0"
author: 
    - "Cisco UCS Team"
    - "Pavan Koundinya"
'''

import sys
from ucsmsdk.mometa.lsboot.LsbootPolicy import LsbootPolicy
from ucsmsdk.mometa.lsboot.LsbootBootSecurity import LsbootBootSecurity
from ucsmsdk.mometa.lsboot.LsbootLan import LsbootLan
from ucsmsdk.mometa.lsboot.LsbootLanImagePath import LsbootLanImagePath
from ucsmsdk.mometa.lsboot.LsbootSan import LsbootSan
from ucsmsdk.ucshandle import UcsHandle
import json
import pickle
import ucs_login
import ucs_logout

def query_mo(input):
    name=input['name']
    ip=input['ip']
    username=input['username']
    password=input['password']
    temp_dict_obj={}
    ucs_handle = pickle.loads(str(ucs_login.main(ip,username,password)))
    try:
        mo = ucs_handle.query_dn("org-root/boot-policy-"+name)
    except:
        print("Could not query children of org-root")
    if mo:
	temp_dict_obj['name']=mo.name
        temp_dict_obj['descr']=mo.descr
        temp_dict_obj['reboot_on_update']=mo.reboot_on_update
        temp_dict_obj['policy_owner']=mo.policy_owner
        temp_dict_obj['enforce_vnic_name']=mo.enforce_vnic_name
        temp_dict_obj['boot_mode']=mo.boot_mode
        return temp_dict_obj
    else: 
	print("No boot policy object with the name "+name)
    ucs_handle=pickle.dumps(ucs_handle)
    ucs_logout.main(ucs_handle)
    return temp_dict_obj

def main():
    
    json_input=json.loads(sys.argv[1])
    results = query_mo(json_input)
    resultsjson=json.dumps(results)
    print(resultsjson)
    #return resultsjson

if __name__ == '__main__':
    main()
