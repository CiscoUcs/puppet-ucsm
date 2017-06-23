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
module: server_pool
short_description: Create, modify or remove server pool policy

description:
  - Allows to check if mac pool policy exists. If present, check for desired configuration. If desired config is not present, apply settings. If mac pool policy is not present, create and apply desired settings. If the desired state is 'absent', remove mac pool policy if it is currently present
 
version_added: "0.1.0"
author: 
    - "Cisco UCS Team"
    - "Pavan Koundinya"
'''

import sys
from ucsmsdk.mometa.compute.ComputePool import ComputePool
from ucsmsdk.mometa.compute.ComputePooledSlot import ComputePooledSlot
from ucsmsdk.ucshandle import UcsHandle
import json
import pickle
import ucs_login
import ucs_logout

def pooled_server_exists(ucs_handle,parent_mo_name,chassis_id,slot_id):
	exists = False
	mo_block = ucs_handle.query_dn("org-root/compute-pool-"+parent_mo_name+"/blade-"+chassis_id+"-"+slot_id)
	if(mo_block):
		exists = True
	return exists

def server_pool(input):
	name = input['name']
	descr=input['descr']
	pooled_servers = input['pooled_servers']
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
		mo = ucs_handle.query_dn("org-root/compute-pool-"+name)
	except:
		results['error'] = "Could not query children of serverpool"


###----if expected state is "present"------------------------

	if state == "present":
		if mo:
			if ( mo.descr == descr ):
				if(len(pooled_servers) != 0):
					local_mo_exists = True
					for obj in pooled_servers:
						mo_exists = pooled_server_exists(ucs_handle,name,obj['chassis_id'],obj['slot_id'])
						local_mo_exists = (local_mo_exists and mo_exists)
					if(local_mo_exists):
						results['name']=name;
						results['expected'] = True;
						results['changed'] = False;
						results['present'] = True;	
					else:
						for obj in pooled_servers:
							mo_exists = pooled_server_exists(ucs_handle,name,obj['chassis_id'],obj['slot_id'])
							if (mo_exists == False):
								mo_1 = ComputePooledSlot(parent_mo_or_dn=mo, slot_id=obj['slot_id'], chassis_id=obj['chassis_id'])
						ucs_handle.add_mo(mo,True)
						ucs_handle.commit()
						results['name']=name;
						results['present'] = True;
						results['removed'] = False;
						results['changed'] = True
				else:
					results['name']=name;
					results['expected'] = True;
					results['changed'] = False;
					results['present'] = True;						


			else:
				try:
					mo = ComputePool(parent_mo_or_dn="org-root", name=name, descr=descr)
					if(len(pooled_servers) != 0):
						local_mo_exists = True
						for obj in pooled_servers:
							mo_exists = pooled_server_exists(ucs_handle,name,obj['chassis_id'],obj['slot_id'])
							local_mo_exists = (local_mo_exists and mo_exists)
						if (local_mo_exists == False):
							for obj in pooled_servers:
								mo_exists = pooled_server_exists(ucs_handle,name,obj['chassis_id'],obj['slot_id'])
								if (mo_exists == False):
									mo_1 = ComputePooledSlot(parent_mo_or_dn=mo, slot_id=obj['slot_id'], chassis_id=obj['chassis_id'])
					ucs_handle.add_mo(mo,True)
					ucs_handle.commit()

					results['name']=name;
					results['present'] = True;
					results['removed'] = False;
					results['changed'] = True

		   		except Exception as e:
					results['error'] = "modification of server pool failed "+ str(e)

###----------if not, create boot policy with desired config ----------------

		else:
			try:
				mo =  ComputePool(parent_mo_or_dn="org-root", name=name, descr=descr)
				if(len(pooled_servers) <> 0):	
					for obj in pooled_servers:
						mo_1= ComputePooledSlot(parent_mo_or_dn=mo, slot_id = obj['slot_id'], chassis_id= obj['chassis_id'])
				ucs_handle.add_mo(mo)
				ucs_handle.commit()
				results['name']=name;
				results['present'] = False;
				results['created'] = True;
				results['changed'] = True;


			except Exception as e:
				results['error'] = "Server pool creation failed " + str(e)


###------if expected state is "absent"----------------------------

	if state == "absent":

		if mo:

			try:
				ucs_handle.remove_mo(mo)
				results['name']=name;
				results['present'] = False;
				results['removed'] = True;
				ucs_handle.commit()

			except Exception as e:
				results['error'] = "Removal server pool mo failed" + str(e)

		else:
			results['name']=name;
			results['removed'] = False;
			results['present'] = False;
	ucs_handle=pickle.dumps(ucs_handle)
	ucs_logout.main(ucs_handle)
	return results
def main():
	json_input=json.loads(sys.argv[1])
	results = server_pool(json_input)
	resultsjson=json.dumps(results)
	print(resultsjson)
	return resultsjson

if __name__ == '__main__':
    main()

