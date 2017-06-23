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
module: storage profile
short_description: Create, modify or remove storage profile 

description:
  - Allows to check if storage profile exists. If present, check for desired configuration. If desired config is not present, apply settings. If vnic template is not present, create and apply desired settings. If the desired state is 'absent', remove vnic template if it is currently present
 
version_added: "0.1.0"
author: 
    - "Cisco UCS Team"
    - "Pavan Koundinya"
'''

import sys
from ucsmsdk.mometa.lstorage.LstorageDiskGroupConfigPolicy import LstorageDiskGroupConfigPolicy
from ucsmsdk.mometa.lstorage.LstorageVirtualDriveDef import LstorageVirtualDriveDef
from ucsmsdk.mometa.lstorage.LstorageLocalDiskConfigRef import LstorageLocalDiskConfigRef
from ucsmsdk.mometa.lstorage.LstorageProfile import LstorageProfile
from ucsmsdk.mometa.lstorage.LstorageDasScsiLun import LstorageDasScsiLun
from ucsmsdk.ucshandle import UcsHandle
import json
import pickle
import ucs_login
import ucs_logout

def contains(list, filter1,filter2,filter3):
	contains = False
	for object in list:
		if (filter1 == object['name'] and filter2 == object['disk_group_configuration_name'] and filter3 == object['size']):
			contains = True
	return contains
	
results = {}

def local_lun_modify(ucs_handle,parent_mo,local_lun_obj):
	mo_local_lun=ucs_handle.query_dn("org-root/profile-"+parent_mo.name+"/das-scsi-lun-"+local_lun_obj['name'])
	if (mo_local_lun):
		if (mo_local_lun.size <> local_lun_obj['size']):
			try:
				mo = LstorageDasScsiLun(parent_mo_or_dn = parent_mo, name = mo_local_lun.name, size = local_lun_obj['size'])
				ucs_handle.add_mo(mo,True)
				ucs_handle.commit()
			except Exception as e:
				results["error"] = "Could not modify Local Lun object"+str(e)
		if(local_lun_obj['disk_group_configuration_name'] <> ""):
			mo_disk = ucs_handle.query_dn("org-root/disk-group-config-" +local_lun_obj['disk_group_configuration_name'])
			if (mo_disk == None):
				results['error'] = "The given disk group configuration does not exist "
			else:
				try:
					mo = LstorageDasScsiLun(parent_mo_or_dn=parent_mo, local_disk_policy_name=local_lun_obj['disk_group_configuration_name'], name=local_lun_obj['name'])
					ucs_handle.add_mo(mo, True)
					ucs_handle.commit()
				except Exception as e :
					results["error"] = "Could not modify Local Lun object"+str(e)
	else:
		try:
			if(local_lun_obj['disk_group_configuration_name'] <> ""):
				mo_disk = ucs_handle.query_dn("org-root/disk-group-config-" +local_lun_obj['disk_group_configuration_name'])
				if (mo_disk == None):
					results['error'] = "The given disk group configuration does not exist "+str(e)
			mo_1 = LstorageDasScsiLun(parent_mo_or_dn=parent_mo, local_disk_policy_name=local_lun_obj['disk_group_configuration_name'], name=local_lun_obj['name'], size=local_lun_obj['size'])
			ucs_handle.add_mo(mo_1)
			ucs_handle.commit()
		except Exception as e:
			results['error'] = "Modification of local lun failed as "+str(e)

def storage_profile(input):
	name = input['name']
	local_lun_list = input['local_lun_list']
	state = input['state']
	ip = input['ip']
	username = input['username']
	password = input['password']
	mo=""
	mo_block = ""
	ucs_handle = pickle.loads(str(ucs_login.main(ip,username,password)))
###-------CHECK IF MO EXISTS---------------------------------

	try:
		mo = ucs_handle.query_dn("org-root/profile-"+name)
	except Exception as e:
		results['error'] = "Could not query storage profile mo "+ str(e)


###----if expected state is "present"------------------------

	if state == "present":
		if (mo):
			current_conf_dict = {}
			current_conf_dict['name'] = mo.name
			try:
				mo_children = ucs_handle.query_children(in_dn="org-root/profile-"+mo.name,class_id="lstorageDasScsiLun")
			except:
				results['error'] = "Could not query children of storage profile mo "+str(e)
			if (mo_children):
				temp_list=[]
				for object in mo_children:
					temp_dict = {}
					temp_dict['name'] = object.name
					temp_dict['size'] = object.size
					if(object.oper_local_disk_policy_name <> ""):
						local_disk_policy_name = object.oper_local_disk_policy_name.replace('org-root/disk-group-config-','')
					else:
						local_disk_policy_name = ""
					temp_dict['disk_group_configuration_name'] = local_disk_policy_name
					temp_list.append(temp_dict)
				current_conf_dict['local_lun_list'] = temp_list
			else:
				current_conf_dict['local_lun_list'] = ""
				
			if(len(local_lun_list) <>0 ):
				current_local_lun_config_list = current_conf_dict['local_lun_list']
				local_lun_exists = True
				for object in local_lun_list:
						if(contains(current_local_lun_config_list,object['name'],object['disk_group_configuration_name'],object['size'])):
							temp_exists = True
							local_lun_exists = (local_lun_exists and temp_exists)
						else:
							local_lun_exists = False
							local_lun_modify(ucs_handle,mo,object)
				if(local_lun_exists):
					results['name']=name;
					results['present'] = True
					results['removed'] = False
					results['changed'] = False
				else :
					results['name']=name;
					results['present'] = True
					results['removed'] = False
					results['changed'] = True


			else:
				results['name']=name;
				results['present'] = True
				results['removed'] = False
				results['changed'] = False
				

###----------if not, create boot policy with desired config ----------------

		else:
			try:
				parent_mo = LstorageProfile(parent_mo_or_dn="org-root", name=name)
				if(len(local_lun_list) <> 0 ):
					for object in local_lun_list :	

						mo_1 = LstorageDasScsiLun(parent_mo_or_dn=parent_mo, local_disk_policy_name=object['disk_group_configuration_name'], name=object['name'], size=object['size'])
						
				ucs_handle.add_mo(parent_mo)
				ucs_handle.commit()
				results['name']=name
				results['present'] = False
				results['created'] = True
				results['changed'] = True

			except Exception as e:
			    results['error'] = "storage profile creation failed "+str(e)
			    return results


###------if expected state is "absent"----------------------------

	if state == "absent":

		if mo:

			try:
				ucs_handle.remove_mo(mo)
				ucs_handle.commit()
				results['name']=name;
				results['present'] = False;
				results['removed'] = True;

			except Exception as e:
				results['error'] = "Removal of storage profile mo failed "+str(e)

		else:
			results['name']=name;
			results['removed'] = False;
			results['present'] = False;
	ucs_handle=pickle.dumps(ucs_handle)
	ucs_logout.main(ucs_handle)
	return results
def main():
	json_input=json.loads(sys.argv[1])
	results = storage_profile(json_input)
	resultsjson=json.dumps(results)
	print(resultsjson)
	return resultsjson

if __name__ == '__main__':
    main()

