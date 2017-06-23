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
module: macpoolInstances
short_description: Retrieves all instances of type mac pool.

description:
  - Queries the UCSPE to retrieve all instances of the mac pool type.Returns a dictionary containing each mac pool instance object as value .The value is again a dictionary that contains the current configuration.
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

final_dict= {}
try_list={}
def query_storageprofileInstances(input):
	ip=input['ip']
	username=input['username']
	password=input['password']
	exists=''
	temp_dict_obj={}
	ucs_handle = pickle.loads(str(ucs_login.main(ip,username,password)))
	try:
		mo = ucs_handle.query_classid("lstorageProfile")
	except:
		print("Could not query children of org-root")
	if mo:
		count=0
		for obj in mo:
			count = count+1
			try_list['name'] = obj.name
			mo_children=ucs_handle.query_children(in_dn="org-root/profile-"+obj.name,class_id="lstorageDasScsiLun")
			if(mo_children):
				temp_list=[]
				local_lun_dict={}
				for mo_children_object in mo_children:
					local_lun_dict['name'] = mo_children_object.name
					local_lun_dict['size'] = mo_children_object.size
					temp1 =str(mo_children_object.oper_local_disk_policy_name)
					if(temp1 != ""):
						mo_disk_group_policy = ucs_handle.query_dn(temp1)
						if(mo_disk_group_policy):
							local_lun_dict['disk_group_configuration_name'] = mo_disk_group_policy.name
						else:
							local_lun_dict['disk_group_configuration_name'] = ""
							
					else:
						local_lun_dict['disk_group_configuration_name'] = ""
							
					temp_list.append(local_lun_dict)
					local_lun_dict = {}
				try_list['local_lun_list'] = temp_list
				#print(try_list)
			else:
				try_list['local_lun_list'] = []	
			final_dict[count] = try_list
	ucs_handle=pickle.dumps(ucs_handle)
	ucs_logout.main(ucs_handle)
	return final_dict

def main(): 
	json_input=json.loads(sys.argv[1])
	results = query_storageprofileInstances(json_input)
	resultsjson=json.dumps(results)
	print(resultsjson)
	final_dict={}
	#return resultsjson

if __name__ == '__main__':
    main()
