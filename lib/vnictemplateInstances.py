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
module: vlanInstances
short_description: Retrieve all instances of type vnic template.

description:
  - Queries the UCSPE to retrieve all instances of the vnic template type.Returns a dictionary containing each vnic template instance object as value .The value is again a dictionary that contains the current configuration.
E.g
{"1": {"name": "utility", "descr": "", "reboot_on_update": "no", "policy_owner": "local", "enforce_vnic_name": "no", "boot_mode": "legacy"}, "2": {"name": "default", "descr": "", "reboot_on_update": "no", "policy_owner": "local", "enforce_vnic_name": "no", "boot_mode": "legacy"}}
version_added: "0.1.0"
author: 
    - "Cisco UCS Team"
    - "Pavan Koundinya"
'''

import sys
from ucsmsdk.ucshandle import UcsHandle
import json
import pickle
import ucs_login
import ucs_logout

try_list={}
def query_vnictemplateInstances(input):
    ip=input['ip']
    username=input['username']
    password=input['password']
    exists=''
    temp_dict_obj={}
    ucs_handle = pickle.loads(str(ucs_login.main(ip,username,password)))
    try:
        mo = ucs_handle.query_classid("vnicLanConnTempl")
    except:
        print("Could not query children of org-root")
    if mo:
	count=0
	for obj in mo:
	    mo_children=ucs_handle.query_children(in_dn="org-root/lan-conn-templ-"+obj.name,class_id="vnicEtherIf")
	    if(mo_children):
                temp_dict_obj['vlan_name']=mo_children[0].name
                temp_dict_obj['default_net']=mo_children[0].default_net
	    else:
	        temp_dict_obj['vlan_name']=""
                temp_dict_obj['default_net']=""
		
	    count=count+1
	    temp_dict_obj['name']=obj.name
	    temp_dict_obj['descr']=obj.descr
            temp_dict_obj['switch_id']=obj.switch_id
            temp_dict_obj['redundancy_pair_type']=obj.redundancy_pair_type
            temp_dict_obj['templ_type']=obj.templ_type
            temp_dict_obj['cdn_source']=obj.cdn_source
            temp_dict_obj['admin_cdn_name']=obj.admin_cdn_name
            temp_dict_obj['mtu']=obj.mtu
            temp_dict_obj['ident_pool_name']=obj.ident_pool_name
	    try_list[count]=temp_dict_obj
	    temp_dict_obj={}
    else: 
	exists=""
    ucs_handle=pickle.dumps(ucs_handle)
    ucs_logout.main(ucs_handle)
    return try_list

def main(): 
    json_input=json.loads(sys.argv[1])
    results = query_vnictemplateInstances(json_input)
    resultsjson=json.dumps(results)
    print(resultsjson)
    try_list={}
    #return resultsjson

if __name__ == '__main__':
    main()
