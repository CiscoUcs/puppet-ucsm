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
module: vlan
short_description: Create, modify or remove vlan policy 

description:
  - Allows to check if vlan policy  exists. If present, check for desired configuration. If desired config is not present, apply settings. If vlan policy is not present, create and apply desired settings. If the desired state is 'absent', remove vlan policy if it is currently present
 
version_added: "0.1.0"
author: 
    - "Cisco UCS Team"
    - "Pavan Koundinya"
'''

import sys
from ucsmsdk.mometa.fabric.FabricVlan import FabricVlan
from ucsmsdk.ucshandle import UcsHandle
import json
import pickle
import ucs_login
import ucs_logout
def vlan(input):
	name = input['name']
	sharing="none"
	id=input['id']
	mcast_policy_name = ""
	policy_owner="local"
	default_net=input['default_net']
	pub_nw_name=""
	compression_type="included"
	state = input['state']
	ip=input['ip']
	username=input['username']
	password=input['password']
	results = {}
	ucs_handle = pickle.loads(str(ucs_login.main(ip,username,password)))
###-------CHECK IF MO EXISTS---------------------------------

	try:
		mo = ucs_handle.query_dn("fabric/lan/net-"+name)
	except:
		print("Could not query children of vlan")


###----if expected state is "present"------------------------

	if state == "present":
		if mo:

			if (mo.name == name and mo.sharing == sharing and 	mo.id == id and mo.mcast_policy_name == mcast_policy_name and 
			mo.policy_owner == policy_owner and mo.default_net == default_net and mo.pub_nw_name == pub_nw_name and 
			mo.compression_type == compression_type ):
				results['name']=name;
				results['expected'] = True;
				results['changed'] = False;
				results['present'] = True;
				#results['mo_bootpolicy'] = json.dumps(json.loads(jsonpickle.encode(mo)));


			else:
		    		try:
					mo.sharing = sharing
					mo.id = id
					mo.mcast_policy_name = mcast_policy_name
					mo.policy_owner = policy_owner
					mo.default_net = default_net
					mo.pub_nw_name = pub_nw_name
					mo.compression_type=compression_type
					results['name']=name;
					results['expected'] = False;
					results['changed'] = True;
					results['present'] = True;
					ucs_handle.set_mo(mo)
					ucs_handle.commit()
					#results['mo_bootpolicy'] = json.dumps(json.loads(jsonpickle.encode(mo)));


		   		except:
					module.fail_json(msg="Modification of vlan mo failed")

###----------if not, create boot policy with desired config ----------------

		else:
			try:
				mo = FabricVlan(parent_mo_or_dn="fabric/lan", name=name,sharing = sharing,id = id , mcast_policy_name = mcast_policy_name , policy_owner = policy_owner , default_net = default_net, pub_nw_name = pub_nw_name,compression_type = compression_type)
				results['name']=name;
				results['present'] = False;
				results['created'] = True;
				results['changed'] = True;
			#results['mo_bootpolicy'] = json.dumps(json.loads(jsonpickle.encode(mo)));

				ucs_handle.add_mo(mo)
				ucs_handle.commit()
			

			except:
				print("Vlan creation failed")


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
				print("Remove Vlan mo failed")

		else:
			results['name']=name;
			results['removed'] = False;
			results['present'] = False;
	ucs_handle=pickle.dumps(ucs_handle)
	ucs_logout.main(ucs_handle)
	return results
def main():
    json_input=json.loads(sys.argv[1])
    results = vlan(json_input)
    resultsjson=json.dumps(results)
    print(resultsjson)
    return resultsjson

if __name__ == '__main__':
    main()

