
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
module: query_disk_group_mo
short_description: Queries UCSPE to check whether macpool object exists. 

description:
  - Allows to check if mac pool managed object exists. If present returns true else returns false.
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
import collections

def query_disk_group_mo(input):
	name=input['name']
	ip=input['ip']
	username=input['username']
	password=input['password']
	slot_numbers=input['slot_numbers']
	raid_level=input['raid_level']
	exists=''
	ucs_handle = pickle.loads(str(ucs_login.main(ip,username,password)))
	try:
		slot_numbers_exist=False
		current_slot_numbers=[]
		mo = ucs_handle.query_dn("org-root/disk-group-config-"+name)
		mo_block=ucs_handle.query_children(in_dn="org-root/disk-group-config-"+name,class_id="lstorageLocalDiskConfigRef")
		for obj in mo_block:
			current_slot_numbers.append(obj.slot_num)
		if(collections.Counter(slot_numbers) == collections.Counter(current_slot_numbers)):
			slot_numbers_exist=True
		if(raid_level==mo.raid_level and slot_numbers_exist):
			exists=True
		else:
			exists=False
	except:
		print("Could not query children of org-root")
	ucs_handle=pickle.dumps(ucs_handle)
	ucs_logout.main(ucs_handle)
	return exists

def main():
    
    json_input=json.loads(sys.argv[1])
    results = query_disk_group_mo(json_input)
    resultsjson=results
    print(resultsjson)
    #return resultsjson

if __name__ == '__main__':
    main()
