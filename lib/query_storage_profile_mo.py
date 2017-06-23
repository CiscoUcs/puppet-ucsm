
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
module: query_macmo
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

def query_storage_profile_mo(input):
	name=input['name']
	local_lun_list = input['local_lun_list']
	ip=input['ip']
	username=input['username']
	password=input['password']
	exists=''
	ucs_handle = pickle.loads(str(ucs_login.main(ip,username,password)))
	try:
		mo_children_exists = False
		mo = ucs_handle.query_dn("org-root/profile-"+name)
		if(mo):
			if(local_lun_list <> None):
				temp_exists = True
				for object in local_lun_list:
					if(temp_exists == False):
						mo_children_exists = False
						break
					mo_children = ucs_handle.query_dn("org-root/profile-"+name+"/das-scsi-lun-"+object['name'])
					if(mo_children and object['size'] == mo_children.size):
						if(object['disk_group_configuration_name'] <> ""):
							mo_disk_group = ucs_handle.query_dn("org-root/disk-group-config-"+object['disk_group_configuration_name'])
							if(mo_disk_group):
								mo_children_exists = True
							else:
								temp_exists = False
						else:
							mo_children_exists = True
					else:
						temp_exists = False
			else:
				mo_children_exists = True				
		else:
			exists = False
	except:
		print("Could not query children of org-root")
	if (mo and mo_children_exists):
		exists="true"
	else: 
		exists="false"
	ucs_handle=pickle.dumps(ucs_handle)
	ucs_logout.main(ucs_handle)
	return exists

def main():
    json_input=json.loads(sys.argv[1])
    results = query_storage_profile_mo(json_input)
    resultsjson=results
    print(resultsjson)
    #return resultsjson

if __name__ == '__main__':
    main()
