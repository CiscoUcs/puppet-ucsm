
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
module: query_service_profile_template
short_description: Queries UCSPE for a specific service profile template managed object .Returns TRUE if object exists else returns FALSE. 

description:
  - Allows to check if service profile template exists. If service profile template with the name exists then the script returns TRUE else it returns FALSE.
 
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

def query_service_profile_template(input):
    name=input['name']
    ip=input['ip']
    username=input['username']
    password=input['password']
    exists=''
    ucs_handle = pickle.loads(str(ucs_login.main(ip,username,password)))
    try:
        mo = ucs_handle.query_dn("org-root/ls-"+name)
    except:
        print("Could not query children of org-root")
    if (mo):
		if(input['storage_profile_name'] <> ""):
			mo_storage_profile =  ucs_handle.query_children(in_dn = "org-root/ls-"+input['name'],class_id = "lstorageProfileBinding")
			if(len(mo_storage_profile) <> 0):
				mo_storage_prof_name_preset = mo_storage_profile[0].storage_profile_name
			else:
				mo_storage_prof_name_preset = None
		else:
			mo_storage_prof_name_preset = None

		if(input['maint_policy_name'] <>""):
			mo_maint_policy_name = "org-root/maint-"+input['maint_policy_name']
		else:
			mo_boot_policy = None
		if(input['server_pool_name'] <> ""):
			mo_server_pool_name =  ucs_handle.query_children(in_dn = "org-root/ls-"+input['name'],class_id = "lsRequirement")
			if(len(mo_server_pool_name)<>0):
				mo_server_pool_name_preset = mo_server_pool_name[0].name
			else:
				mo_server_pool_name_preset = None
		else:
			mo_server_pool_name_preset =None
		mo_vnic_ether = ucs_handle.query_children(in_dn = "org-root/ls-"+input['name'],class_id = "vnicEther")
		vnic_profile_exists =''
		if(input['vnic_name'] <> "" and input['vnic_template_name']<>"" and input['vnic_order']<>""):
			for obj in mo_vnic_ether:
				if(obj.name==input['vnic_name'] and obj.adaptor_profile_name == input['adapter_profile_name'] and obj.nw_templ_name ==input['vnic_template_name'] and obj.order == input['vnic_order']):
					vnic_profile_exists=True
				else:
					vnic_profile_exists=False
		else:
			vnic_profile_exists=True
		if( mo.ident_pool_name == input['ident_pool_name'] and mo.local_disk_policy_name == input['local_disk_policy_name'] 
		and mo.boot_policy_name ==  input['boot_policy_name'] and mo.bios_profile_name == input['bios_profile_name'] and 
		mo.oper_maint_policy_name == mo_maint_policy_name and mo.host_fw_policy_name == input['host_fw_policy_name'] and
		mo_storage_prof_name_preset == input['storage_profile_name'] and mo_server_pool_name_preset == input['server_pool_name'] and
		mo.ext_ip_pool_name == input['mgmt_ip_address']and vnic_profile_exists):
			exists="true"
		else:
			exists = "false"
    else: 
		exists="false"
    ucs_handle=pickle.dumps(ucs_handle)
    ucs_logout.main(ucs_handle)
    return exists

def main():
    json_input=json.loads(sys.argv[1])
    results = query_service_profile_template(json_input)
    resultsjson=results
    print(resultsjson)
    #return resultsjson

if __name__ == '__main__':
    main()
