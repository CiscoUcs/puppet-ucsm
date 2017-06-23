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
module: host_firmware_policy
short_description: Create, modify or remove host firmware policy 

description:
  - Allows to check if host firmware policy exists. If present, check for desired configuration. If desired config is not present, apply settings. If host firmware policy is not present, create and apply desired settings. If the desired state is 'absent', remove host firware policy if it is currently present
 
version_added: "0.1.0"
author: 
    - "Cisco UCS Team"
    - "Pavan Koundinya"
'''

import sys
from ucsmsdk.mometa.firmware.FirmwareComputeHostPack import FirmwareComputeHostPack
from ucsmsdk.mometa.firmware.FirmwareExcludeServerComponent import FirmwareExcludeServerComponent
from ucsmsdk.ucshandle import UcsHandle
import json
import pickle
import ucs_login
import ucs_logout
def host_firmware_package(input):
	name = input['name']
	descr = input['descr']
	state = input['state']
	ip=input['ip']
	username=input['username']
	password=input['password']
	results = {}
	ucs_handle = pickle.loads(str(ucs_login.main(ip,username,password)))
###-------CHECK IF MO EXISTS---------------------------------

	try:
		mo = ucs_handle.query_dn("org-root/fw-host-pack-"+name)
	except Exception as e:
		results['error'] = "Could not query children of host firware package " + str(e)
		return results


###----if expected state is "present"------------------------

	if state == "present":
		if mo:

			if (mo.name == name and mo.descr == descr ):
				results['name']=name;
				results['expected'] = True;
				results['changed'] = False;
				results['present'] = True;
				#results['mo_bootpolicy'] = json.dumps(json.loads(jsonpickle.encode(mo)));


			else:
		    		try:
					mo = FirmwareComputeHostPack(parent_mo_or_dn="org-root", name=name, descr=descr)
					ucs_handle.add_mo(mo, True)
					ucs_handle.commit()
					results['name']=name;
					results['expected'] = False;
					results['changed'] = True;
					results['present'] = True;
					#results['mo_bootpolicy'] = json.dumps(json.loads(jsonpickle.encode(mo)));


		   		except Exception as e:
					results['error'] = "Modification of host firmware package mo failed "+ str(e)
					return results

###----------if not, create boot policy with desired config ----------------

		else:
			try:
				mo = FirmwareComputeHostPack(parent_mo_or_dn="org-root", name=name, descr=descr, override_default_exclusion="yes")
				mo_1 = FirmwareExcludeServerComponent(parent_mo_or_dn=mo, server_component="local-disk")
				ucs_handle.add_mo(mo)
				ucs_handle.commit()
				results['name']=name;
				results['present'] = False;
				results['created'] = True;
				results['changed'] = True;
			except Exception as e:
				results['error'] = "host firmware package creation failed "+str(e)
				return results


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
				results['error'] = "Removal of host firmware package mo failed" + str(e)
				return results

		else:
			results['name']=name;
			results['removed'] = False;
			results['present'] = False;
	ucs_handle=pickle.dumps(ucs_handle)
	ucs_logout.main(ucs_handle)
	return results
def main():
	input = sys.argv[1]
	json_input=json.loads(input)
	results = host_firmware_package(json_input)
	resultsjson=json.dumps(results)
	print(resultsjson)
	return resultsjson

if __name__ == '__main__':
    main()

