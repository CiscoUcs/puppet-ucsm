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
module: boot_policy
short_description: Create, modify or remove boot_policy 

description:
  - Allows to check if vnic template exists. If present, check for desired configuration. If desired config is not present, apply settings. If boot policy is not present, create and apply desired settings. If the desired state is 'absent', remove boot policy if it is currently present
 
version_added: "0.1.0"
author: 
    - "Cisco UCS Team"
    - "Pavan Koundinya"
'''

import sys
from ucsmsdk.mometa.lsboot.LsbootPolicy import LsbootPolicy
from ucsmsdk.mometa.lsboot.LsbootLan import LsbootLan
from ucsmsdk.mometa.lsboot.LsbootLanImagePath import LsbootLanImagePath
from ucsmsdk.mometa.lsboot.LsbootStorage import LsbootStorage
from ucsmsdk.mometa.lsboot.LsbootLocalStorage import LsbootLocalStorage
from ucsmsdk.mometa.lsboot.LsbootLocalHddImage import LsbootLocalHddImage
from ucsmsdk.mometa.lsboot.LsbootLocalLunImagePath import LsbootLocalLunImagePath
from ucsmsdk.ucshandle import UcsHandle
import json
import pickle
import ucs_login
import ucs_logout
def query_locallunmo(ucs_handle,mo,device_name,order):
	exists=False
	mo_hierarchy_object = ucs_handle.query_dn("org-root/boot-policy-"+mo.name+"/storage/local-storage/local-hdd")
	if (mo_hierarchy_object and mo_hierarchy_object.order==order):
		mo_block= ucs_handle.query_children(in_dn="org-root/boot-policy-"+mo.name+"/storage/local-storage/local-hdd",hierarchy=True,class_id="lsbootLocalLunImagePath")
		if(mo_block):
			for obj in mo_block:
				if(obj.lun_name == device_name):
					exists=True
		else:
			exists= False
	else:
		exists = False
	return exists
def query_lanmo(ucs_handle,mo,device_name,order):
	exists=False
	mo_hierarchy_object = ucs_handle.query_dn("org-root/boot-policy-"+mo.name+"/lan")
	if (mo_hierarchy_object and mo_hierarchy_object.order==order):
		mo_block= ucs_handle.query_children(in_dn="org-root/boot-policy-"+mo.name+"/lan",hierarchy=True,class_id="lsbootLanImagePath")
		if(mo_block):
			for obj in mo_block:
				if(obj.vnic_name == device_name):
					exists=True
		else:
			exists= False
	else:
		exists = False
	return exists
	
def boot_policy(input):
	name = input['name']
	type =input['type']
	device_name = input['device_name']
	order = input['order']
	state = input['state']
	ip=input['ip']
	username=input['username']
	password=input['password']
	mo=""
	mo_block=""
	results = {}
	ucs_handle = pickle.loads(str(ucs_login.main(ip,username,password)))
###-------CHECK IF MO EXISTS---------------------------------

	try:
		mo = ucs_handle.query_dn("org-root/boot-policy-"+name)
		
	except:
		return '{"error":"Could not query children of boot policy"}'


###----if expected state is "present"------------------------

	if state == "present":


		if (mo and (type == "LAN" or type == "LocalLun")):
			if(type == "LAN"):
				lan_query=query_lanmo(ucs_handle,mo,device_name,order)
				local_lun_query=True
			elif(type == "LocalLun"):
				local_lun_query=query_locallunmo(ucs_handle,mo,device_name,order)
				lan_query=True
			else:
				print("The type mentioned is not supported by this module.")
			if ( mo.name == name and lan_query and local_lun_query ):
				results['name']=name;
				results['expected'] = True;
				results['changed'] = False;
				results['present'] = True;


			else:
				try:
					if (lan_query and ~(local_lun_query)):
						modified_mo = LsbootStorage(parent_mo_or_dn=mo, )
						mo_1 = LsbootLocalStorage(parent_mo_or_dn=modified_mo, )
						mo_1_1 = LsbootLocalHddImage(parent_mo_or_dn=mo_1, order=order)
						mo_1_1_1 = LsbootLocalLunImagePath(parent_mo_or_dn=mo_1_1, lun_name=device_name, type="primary")
						ucs_handle.add_mo(modified_mo, True)
						ucs_handle.commit()
					elif(local_lun_query and ~(lan_query)):
						modified_mo = LsbootLan(parent_mo_or_dn=mo, order=order)
						mo_1_1 = LsbootLanImagePath(parent_mo_or_dn=modified_mo, type="primary", vnic_name=device_name)
						ucs_handle.add_mo(mo, True)
						ucs_handle.commit()
					else:
						modified_mo = LsbootStorage(parent_mo_or_dn=mo, )
						mo_1 = LsbootLocalStorage(parent_mo_or_dn=modified_mo, )
						mo_1_1 = LsbootLocalHddImage(parent_mo_or_dn=mo_1, order=order)
						mo_1_1_1 = LsbootLocalLunImagePath(parent_mo_or_dn=mo_1_1, lun_name=device_name, type="primary")
						ucs_handle.add_mo(mo, True)
						ucs_handle.commit()
						modified_mo = LsbootLan(parent_mo_or_dn=mo, order=order)
						mo_1_1 = LsbootLanImagePath(parent_mo_or_dn=mo_1, type="primary", vnic_name=device_name)
						ucs_handle.add_mo(mo, True)
						ucs_handle.commit()
					results['name']=name
					results['present'] = True
					results['removed'] = False
					results['changed'] = True

		   		except Exception,e:
					return '{"error":"%s" %e}'
		elif(mo and type ==""):
		    results['name'] = name
		    results['present'] = True
		    results['removed'] = False
		    results['changed'] = False

###----------if not, create boot policy with desired config ----------------

		else:
			try:
				
				mo = LsbootPolicy(parent_mo_or_dn="org-root", name=name, descr="")
				if(type  != ""):
				    if(type == "LAN"):
					    mo_1 = LsbootLan(parent_mo_or_dn=mo, order=order)
					    mo_1_1 = LsbootLanImagePath(parent_mo_or_dn=mo_1, type="primary", vnic_name=device_name)
				    else:
					    mo_2 = LsbootStorage(parent_mo_or_dn=mo, order=order)
					    mo_2_1 = LsbootLocalStorage(parent_mo_or_dn=mo_2, )
					    mo_2_1_1 = LsbootLocalHddImage(parent_mo_or_dn=mo_2_1, order=order)
					    mo_2_1_1_1 = LsbootLocalLunImagePath(parent_mo_or_dn=mo_2_1_1, lun_name=device_name, type="primary")
				ucs_handle.add_mo(mo)
				ucs_handle.commit()				
				results['name']=name;
				results['present'] = False;
				results['created'] = True;
				results['changed'] = True;


			except:
				return '{"error":"boot policy creation failed"}'


###------if expected state is "absent"----------------------------

	if state == "absent":

		if mo:

			try:
				ucs_handle.remove_mo(mo)
				ucs_handle.commit()
				results['name']=name;
				results['present'] = False;
				results['removed'] = True;
				

			except:
				return '{"error":"Removal boot policy mo failed"}'

		else:
			results['name']=name;
			results['removed'] = False;
			results['present'] = False;
	ucs_handle=pickle.dumps(ucs_handle)
	ucs_logout.main(ucs_handle)
	return results
def main():
	json_input=json.loads(sys.argv[1])
	results = boot_policy(json_input)
	resultsjson=json.dumps(results)
	print(resultsjson)
	return resultsjson
	print(exists)
	
	
	

if __name__ == '__main__':
    main()

