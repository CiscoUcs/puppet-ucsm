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
module: serverpoolInstances
short_description: Retrieves all instances of type server pool.

description:
  - Queries the UCSPE to retrieve all instances of the server pool type.Returns a dictionary containing each server pool instance object as value .The value is again a dictionary that contains the current configuration.
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
def query_serverpoolInstances(input):
    ip=input['ip']
    username=input['username']
    password=input['password']
    exists=''
    temp_dict_obj={}
    ucs_handle = pickle.loads(str(ucs_login.main(ip,username,password)))
    try:
        mo = ucs_handle.query_classid("computePool")
    except:
        print("Could not query children of org-root")
    if mo:
	count=0
	for obj in mo:
		mo_children=ucs_handle.query_children(in_dn="org-root/compute-pool-"+obj.name,class_id="computePooledSlot")
		temp_list=[]
		temp_dict ={}
		if(mo_children):	
			for object in mo_children:
					temp_dict['slot_id'] = object.slot_id
					temp_dict['chassis_id'] = object.chassis_id		
					temp_list.append(temp_dict)
					temp_dict ={}
		else:
			temp_dict['slot_id']=""
			temp_dict['chassis_id']=""
			temp_list.append(temp_dict)
			temp_dict ={}
		count=count+1
		temp_dict_obj['name']=obj.name
		temp_dict_obj['descr']=obj.descr
		temp_dict_obj['pooled_servers'] = temp_list
		try_list[count]=temp_dict_obj
		temp_dict_obj={}
    else: 
	exists=""
    ucs_handle=pickle.dumps(ucs_handle)
    ucs_logout.main(ucs_handle)
    return try_list

def main(): 
	json_input=json.loads(sys.argv[1])
	results = query_serverpoolInstances(json_input)
	resultsjson=json.dumps(results)
	print(resultsjson)
	try_list={}
    #return resultsjson

if __name__ == '__main__':
    main()
