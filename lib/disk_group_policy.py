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
module: disk_group_policy
short_description: Create, modify or remove disk group  policy

description:
  - Allows to check if disk group policy policy exists. If present, check for desired configuration. If desired config is not present, apply settings. If mac pool policy is not present, create and apply desired settings. If the desired state is 'absent', remove mac pool policy if it is currently present
 
version_added: "0.1.0"
author: 
    - "Cisco UCS Team"
    - "Pavan Koundinya"
'''

import sys
from ucsmsdk.mometa.lstorage.LstorageDiskGroupConfigPolicy import LstorageDiskGroupConfigPolicy
from ucsmsdk.mometa.lstorage.LstorageVirtualDriveDef import LstorageVirtualDriveDef
from ucsmsdk.mometa.lstorage.LstorageLocalDiskConfigRef import LstorageLocalDiskConfigRef
from ucsmsdk.ucshandle import UcsHandle
import json
import collections
import pickle
import ucs_login
import ucs_logout
def disk_group_policy(input):
	name = input['name']
	raid_level=input['raid_level']
	slot_numbers=input['slot_numbers']
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
		mo = ucs_handle.query_dn("org-root/disk-group-config-"+name)
		mo_block=ucs_handle.query_children(in_dn="org-root/disk-group-config-"+name,class_id="lstorageLocalDiskConfigRef")
	except:
		print("Could not query children of disk group policy")


###----if expected state is "present"------------------------

	if state == "present":
		if mo:
			slot_numbers_exist=False
			current_slot_numbers=[]
			for obj in mo_block:
				current_slot_numbers.append(obj.slot_num)
			if(collections.Counter(slot_numbers) == collections.Counter(current_slot_numbers)):
				slot_numbers_exist=True
			if(mo.raid_level==raid_level and slot_numbers_exist):
				
				results['name']=name;
				results['expected'] = True;
				results['changed'] = False;
				results['present'] = True;
			else:
				for slot_num in slot_numbers:
					query_slot=ucs_handle.query_dn("org-root/disk-group-config-"+name+"/slot-"+slot_num)
					if(query_slot == None):
						mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, slot_num=slot_num)	
						ucs_handle.add_mo(mo, True)
						ucs_handle.commit()
				mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn="org-root", raid_level=raid_level, name=name)
				ucs_handle.add_mo(mo, True)
				ucs_handle.commit()
				results['name']=name;
				results['expected'] = True;
				results['changed'] = True;
				results['present'] = True;
###----------if not, create boot policy with desired config ----------------

		else:
			try:
				mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn="org-root", raid_level=raid_level, name=name)
				mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="platform-default", drive_cache="platform-default",
				strip_size="platform-default", io_policy="platform-default", write_cache_policy="platform-default", 
				access_policy="platform-default")
				if(len(slot_numbers) > 0):
					for slot_num in slot_numbers:
						mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, slot_num=slot_num)
				ucs_handle.add_mo(mo)
				ucs_handle.commit()
				results['name']=name;
				results['present'] = False;
				results['created'] = True;
				results['changed'] = True;


			except Exception as e:
				print("disk group configuration policy  creation failed "+ str(e))


###------if expected state is "absent"----------------------------

	if state == "absent":

		if mo:

			try:
				ucs_handle.remove_mo(mo)
				results['name']=name;
				results['present'] = False;
				results['removed'] = True;
				ucs_handle.commit()

			except:
				print("Removal Mac-pool mo failed")

		else:
			results['name']=name;
			results['removed'] = False;
			results['present'] = False;
	ucs_handle=pickle.dumps(ucs_handle)
	ucs_logout.main(ucs_handle)
	return results
def main():
	
	json_input=json.loads(sys.argv[1])
	results = disk_group_policy(json_input)
	resultsjson=json.dumps(results)
	print(resultsjson)
	return resultsjson

if __name__ == '__main__':
    main()

