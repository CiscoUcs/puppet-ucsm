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


def sp_create(ucs_handle, name, src_templ_name,	parent_dn='org-root'):
	"""
	This method creates Service Profiles from existing templates.
	Args:
        ucs_handle (ucs_handle)
        name(string): Name of SP
        src_templ_name (string): Name of Source template
        parent_dn= Parent DN

	Returns:
		Service Profile: Managed Object

	Raises:
		ValueError: If OrgOrg is not present

	Example:
		sp_create(ucs_handle, name='Test-1', src_templ_name='TestTemplate')
	"""
	from ucsmsdk.mometa.ls.LsServer import LsServer

	obj = ucs_handle.query_dn(parent_dn)
	if not obj:
		raise ValueError("org '%s' does not exist." % parent_dn)

	mo = LsServer(parent_mo_or_dn=obj,
		      name=name,
		      src_templ_name=src_templ_name,
		      type='instance',
		      uuid='derived')

	ucs_handle.add_mo(mo, True)
	ucs_handle.commit()
	return mo


def sp_exists(input):
	results={}
	ucs_handle = input['ucs_handle']
	try:
	        mo = ucs_handle.query_dn("org-root/ls-"+input['name'])
	except:
		return '{"error":"Could not query children of service profile"}'

	if(input['state'] == "present"):
		if(mo is None):
			sp_create(ucs_handle = ucs_handle, name=input["name"], src_templ_name=input['src_templ_name'])
			results['name']=input["name"]
		        results['expected'] = True
			results['changed'] = True
			results['created'] = True
		        results['present'] = True;

		else:
			results['name']=input["name"]
		        results['expected'] = True
			results['changed'] = False
			results['created'] = False
		        results['present'] = True;

		results['removed'] = False;
	elif(input['state'] == "absent"):
		if mo:
			try:
				ucs_handle.remove_mo(mo)
				ucs_handle.commit()
				results['name']=input["name"]
		                results['expected'] = False
				results['changed'] = True
				results['removed'] = True
				results['present'] = False;

			except Exception as e:
				results['error'] = "Removal of service profile failed "+str(e)
		else:
			results['name']=input["name"]
		        results['expected'] = False
			results['changed'] = False
			results['removed'] = False
			results['present'] = False;
	else:
		results['error'] = "Invalid input for State"
	return results
	
import json
import pickle
import ucs_login
import ucs_logout
import sys
def main():
	json_input = json.loads(sys.argv[1])
	ucs_handle = pickle.loads(str(ucs_login.main(json_input['ip'],json_input['username'],json_input['password'])))
	json_input['ucs_handle'] = ucs_handle
	resultsjson = sp_exists(json_input)
	resultsjson=json.dumps(resultsjson)
	ucs_handle=pickle.dumps(ucs_handle)
	ucs_logout.main(ucs_handle)
	print(resultsjson)
	return resultsjson

if __name__ == '__main__':
    main()
