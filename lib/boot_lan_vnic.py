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
module: boot_lan_vnic
short_description: Create, modify or remove boot lan vnic primary and secondary

description:
  - Allows to check if boot lan vnic mo exists. If present, add a secondary boot lan vnic mo. If boot lan vnic mo is not present, create a primary boot lan vnic mo. If the desired state is 'absent', remove boot lan mo if it is currently present. If it is secondary, do nothing. If it is primary, make current secondary vnic primary and remove mo
 
version_added: "0.1.0"
author: 
    - "Cisco UCS Team"
    - "Pavan Koundinya"
'''

EXAMPLES = '''
# Create or modify boot lan vnic 
  - name: Check desired configuration for Boot Lan vnic {{ ucsm_ip }}
    boot_lan_vnic:
      name="newdesmo22"
      vnic_name="newdemo"
      state="present"
      handle={{ handle_output.handle }}

# Remove boot lan vnic
  - name: Check desired configuration for Boot Lan vnic {{ ucsm_ip }}
    boot_lan_vnic:
      name="sampe"
      vnic_name="sample"
      state="absent"
      handle={{ handle_output.handle }}n
'''

from ucsmsdk.mometa.lsboot.LsbootPolicy import LsbootPolicy
from ucsmsdk.mometa.lsboot.LsbootBootSecurity import LsbootBootSecurity
from ucsmsdk.mometa.lsboot.LsbootLan import LsbootLan
from ucsmsdk.mometa.lsboot.LsbootLanImagePath import LsbootLanImagePath
from ucsmsdk.mometa.lsboot.LsbootSan import LsbootSan
from ucsmsdk.ucshandle import UcsHandle
import json
import pickle
import ucs_login
import ucs_logout

def boot_lan_vnic(input):
    ip=input['ip']
    username=input['username']
    password=input['password']
    vnic_name = input['vnic_name']
    name = input['name']
    #mo_bootlan = module.params.get('mo_bootlan')
    state = input['state']
    type_string = "type"
    results = {}

    ucs_handle = pickle.loads(str(ucs_login.main(ip,username,password)))

    #mo_bootlan_parsed = jsonpickle.decode(mo_bootlan)


###-------CHECK IF MO EXISTS------------------------------------------------

    try:

	mo = ucs_handle.query_children(in_dn="org-root/boot-policy-"+name+"/lan", class_id="LsbootLanImagePath")
	
    except:
        print "Could not query children of org-root"


###-------------check if obj is empty or non-empty ------------------------

    obj_exists = lambda obj: True if obj != [] else False

###-------if expected state is "present"----------------------------------

    if state == "present":

		if mo:

			if (len(mo) == 1):
				if (mo[0].vnic_name == vnic_name):

					results['expected'] = True;
					results['present'] = True;
					results['changed'] = False;

				else:
					try:
						mo_lan = LsbootLanImagePath(parent_mo_or_dn="org-root/boot-policy-"+name+"/lan", prov_srv_policy_name="", img_sec_policy_name="", vnic_name=vnic_name, i_scsi_vnic_name="", boot_ip_policy_name="", img_policy_name="", type="secondary")
						ucs_handle.add_mo(mo_lan)
						ucs_handle.commit()
						results['expected'] = True;
						results['present'] = True;
						results['changed'] = False;

					except:
						print "Modify boot policy mo 1 failed"

			if (len(mo) == 2):
				if (mo[0].vnic_name == vnic_name or mo[1].vnic_name == vnic_name):

					results['expected'] = True;
					results['present'] = True;
					results['changed'] = False;
				else:

					results['expected'] = False;
					results['present'] = False;
					results['changed'] = False;

###----------------else create boot policy with desired config ----------------
		else:

			try:
				obj = ucs_handle.query_dn("org-root/boot-policy-"+name)
				if (obj):
					mo = LsbootLanImagePath(parent_mo_or_dn="org-root/boot-policy-"+name+"/lan", prov_srv_policy_name="", img_sec_policy_name="", vnic_name=vnic_name, i_scsi_vnic_name="", boot_ip_policy_name="", img_policy_name="", type="primary")
					ucs_handle.add_mo(mo)
					ucs_handle.commit()
					results['present'] = True;
					results['changed'] = True;
				else:

					results['present'] = False;
					results['changed'] = False;

			except:
				print "Modify boot lan image mo failed"

###-------if expected state is "absent"---------------------------------------

    if state == "absent":

	    if mo:

		if (len(mo) == 1):
			if (mo[0].vnic_name == vnic_name):

		    		try:
				 	mo_primary = ucs_handle.query_dn("org-root/boot-policy-"+name+"/lan/path-primary")
					ucs_handle.remove_mo(mo_primary)
					results['present'] = False;
					results['removed'] = True;
					ucs_handle.commit()

		   		except:
					print "Remove boot lan image mo failed"

		if (len(mo) == 2):

			if (mo[0].vnic_name == vnic_name and mo[0].type == "secondary"):

		    		try:
					mo_2 = ucs_handle.query_dn("org-root/boot-policy-"+name+"/lan/path-secondary")
					ucs_handle.remove_mo(mo_2)
					ucs_handle.commit()

		   		except:
					print "Remove boot lan image secondary failed"

			if (mo[0].vnic_name == vnic_name and mo[0].type == "primary"):

		    		try:
					mo_parent = ucs_handle.query_dn("org-root/boot-policy-"+name+"/lan")

					mo_modify = LsbootLanImagePath(parent_mo_or_dn=mo_parent, prov_srv_policy_name="", img_sec_policy_name="", vnic_name=mo[1].vnic_name, i_scsi_vnic_name="", boot_ip_policy_name="", img_policy_name="", type="primary")
					mo_parent = ucs_handle.query_dn("org-root/boot-policy-"+name+"/lan")
					mo_2 = ucs_handle.query_dn("org-root/boot-policy-"+name+"/lan/path-secondary")
					ucs_handle.remove_mo(mo_2)
					ucs_handle.add_mo(mo_parent, True)
					ucs_handle.commit()
					results['present'] = False;
					results['removed'] = True;

		   		except:
					print "Remove boot lan mo for primary failed"

			if (mo[1].vnic_name == vnic_name and mo[1].type == "secondary"):

		    		try:
					mo_secondary = ucs_handle.query_dn("org-root/boot-policy-"+name+"/lan/path-secondary")
					ucs_handle.remove_mo(mo_secondary)
					ucs_handle.commit()
					results['present'] = False;
					results['removed'] = True;


		   		except:
					print "Remove boot lan image mo for secondary  failed"


			if (mo[1].vnic_name == vnic_name and mo[1].type == "primary"):

		    		try:
					mo_1 = ucs_handle.query_dn("org-root/boot-policy-"+name+"/lan/path-secondary")
					mo_parent = ucs_handle.query_dn("org-root/boot-policy-"+name+"/lan")
					mo_modify = LsbootLanImagePath(parent_mo_or_dn=mo_parent, prov_srv_policy_name="", img_sec_policy_name="", vnic_name=mo[0].vnic_name, i_scsi_vnic_name="", boot_ip_policy_name="", img_policy_name="", type="primary")
					ucs_handle.remove_mo(mo_1)

					ucs_handle.add_mo(mo_modify,True) 	
					results['present'] = False;
					results['removed'] = True;
					ucs_handle.commit()

		   		except:
					print "Remove boot lan image mo for primary failed"


	    else:

    		results['removed'] = False;
		results['present'] = False;

    return results

def main():
    #input='{"name":"bootlandemo","vnic_name":"qwerty","state" :"present","ip":"172.31.219.215","username":"admin","password":"password"}'
    json_input=json.loads(sys.argv[1])
    results = boot_lan_vnic(json_input)
    resultsjson=json.dumps(results)
    print(resultsjson)
    return resultsjson

if __name__ == '__main__':
    main()
