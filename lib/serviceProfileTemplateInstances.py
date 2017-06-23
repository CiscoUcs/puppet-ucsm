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
module: serviceprofileTemplateInstances
short_description: Retrieves all instances of type mac pool.

description:
  - Queries the UCSPE to retrieve all instances of the service profile template type.Returns a dictionary containing each service profile template instance object as value .The value is again a dictionary that contains the current configuration.
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
def query_serviceprofileTemplateInstances(input):
	ip=input['ip']
	username=input['username']
	password=input['password']
	exists=''
	temp_dict_obj={}
	ucs_handle = pickle.loads(str(ucs_login.main(ip,username,password)))
	try:
		mo = ucs_handle.query_classid("lsServer")
	except:
		print("Could not query children of org-root")
	if mo:
		count=0
		for obj in mo:
			count = count+1
			try_list['name'] = obj.name
			mo_storage_profile =  ucs_handle.query_children(in_dn = "org-root/ls-"+obj.name,class_id = "lstorageProfileBinding")
			if(mo_storage_profile):
				try_list['storage_profile_name'] = mo_storage_profile[0].storage_profile_name
			else:
				try_list['storage_profile_name'] = ""
			mo_server_pool_name =  ucs_handle.query_children(in_dn = "org-root/ls-"+obj.name,class_id = "lsRequirement")
			if(mo_server_pool_name):
				try_list['server_pool_name'] = mo_server_pool_name[0].name
			else:
				try_list['server_pool_name'] = None
			mo_vnic_templ = ucs_handle.query_children(in_dn = "org-root/ls-"+obj.name,class_id = "vnicEther")
			if(mo_vnic_templ):
				try_list['vnic_name'] = mo_vnic_templ[0].name
				try_list['vnic_template_name'] = mo_vnic_templ[0].nw_templ_name
				try_list['adapter_profile_name'] =mo_vnic_templ[0].adaptor_profile_name
				try_list['vnic_order'] = mo_vnic_templ[0].order
				
			else:
				try_list['vnic_name'] = ""
				try_list['vnic_template_name'] = ""
				try_list['adapter_profile_name'] =""
			
			
			try_list['ident_pool_name'] = obj.ident_pool_name
			try_list['local_disk_policy_name'] = obj.local_disk_policy_name
			try_list['boot_policy_name'] = obj.boot_policy_name
			try_list['bios_profile_name'] = obj.bios_profile_name
			try_list['host_fw_policy_name'] = obj.host_fw_policy_name
			try_list['mgmt_ip_address']=obj.ext_ip_pool_name
			try_list['type']=obj.type
			try_list['maint_policy_name']=obj.maint_policy_name
			
			final_dict[count] = try_list
	ucs_handle=pickle.dumps(ucs_handle)
	ucs_logout.main(ucs_handle)
	return final_dict

def main(): 
	json_input=json.loads(sys.argv[1])
	results = query_serviceprofileTemplateInstances(json_input)
	resultsjson=json.dumps(results)
	print(resultsjson)
	final_dict={}
    #return resultsjson

if __name__ == '__main__':
    main()
