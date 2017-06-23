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
module: vnic_template
short_description: Create, modify or remove vnic_template 

description:
  - Allows to check if vnic template exists. If present, check for desired configuration. If desired config is not present, apply settings. If vnic template is not present, create and apply desired settings. If the desired state is 'absent', remove vnic template if it is currently present
 
version_added: "0.1.0"
author: 
    - "Cisco UCS Team"
    - "Pavan Koundinya"
'''

import sys
from ucsmsdk.mometa.vnic.VnicLanConnTempl import VnicLanConnTempl
from ucsmsdk.mometa.vnic.VnicEtherIf import VnicEtherIf
from ucsmsdk.ucshandle import UcsHandle
import json
import pickle
import ucs_login
import ucs_logout
def vnic_template(input):
	name = input['name']
	descr=input['descr']
	switch_id=input['switch_id']
	redundancy_pair_type="none"
	templ_type= input['templ_type']
	vlan_name=input['vlan_name']
	default_net=input['default_net']
	cdn_source=input['cdn_source']
	admin_cdn_name=input['admin_cdn_name']
	mtu=input['mtu']
	ident_pool_name= input['ident_pool_name']
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
		mo = ucs_handle.query_dn("org-root/lan-conn-templ-"+name)
		mo_block=ucs_handle.query_dn("org-root/lan-conn-templ-"+name+"/if-"+vlan_name)
		mo_children=ucs_handle.query_children(in_dn="org-root/lan-conn-templ-"+name,class_id="vnicEtherIf")
	except:
		print("Could not query children of macpool")


###----if expected state is "present"------------------------

	if state == "present":
		block_temp=False
		if(mo_block and mo_block.name ==vlan_name and mo_block.default_net ==default_net):
				
			block_temp=True
		elif (vlan_name == "" and not(mo_children)):
			block_temp=True
		elif (mo_children):
			block_temp=False
		else:
			block_temp=False
				
		if (mo):
			if ( mo.name == name and mo.descr == descr and mo.switch_id ==switch_id and mo.redundancy_pair_type == redundancy_pair_type and mo.templ_type ==templ_type and mo.cdn_source == cdn_source and mo.admin_cdn_name == admin_cdn_name and mo.mtu ==mtu and mo.ident_pool_name == ident_pool_name   and block_temp):
				results['name']=name;
				results['expected'] = True;
				results['changed'] = False;
				results['present'] = True;


			else:
				try:
					modified_mo =  VnicLanConnTempl(parent_mo_or_dn="org-root", name=name, descr=descr ,switch_id =switch_id , redundancy_pair_type = redundancy_pair_type ,templ_type = templ_type , cdn_source = cdn_source , admin_cdn_name = admin_cdn_name , mtu =mtu ,ident_pool_name = ident_pool_name )
					if(vlan_name):
						mo_1= VnicEtherIf(parent_mo_or_dn=modified_mo,default_net=default_net, name=vlan_name)					
					ucs_handle.add_mo(modified_mo,True)
					ucs_handle.commit()
					results['name']=name;
					results['present'] = True;
					results['removed'] = False;
					results['changed'] = True

		   		except Exception,e:
					print(e)

###----------if not, create boot policy with desired config ----------------

		else:
			try:
			    mo =  VnicLanConnTempl(parent_mo_or_dn="org-root", name=name, descr=descr ,switch_id =switch_id , redundancy_pair_type = redundancy_pair_type ,templ_type = templ_type , cdn_source = cdn_source , admin_cdn_name = admin_cdn_name , mtu=mtu ,ident_pool_name = ident_pool_name )
			    if(vlan_name):
				mo_1= VnicEtherIf(parent_mo_or_dn=mo,default_net=default_net, name=vlan_name)
			    ucs_handle.add_mo(mo)
                            ucs_handle.commit()
			    results['name']=name;
			    results['present'] = False;
			    results['created'] = True;
			    results['changed'] = True;

			except:
			    results['error'] = "Vnic template creation failed"
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
	results = vnic_template(json_input)
	resultsjson=json.dumps(results)
	print(resultsjson)
	return resultsjson

if __name__ == '__main__':
    main()

