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
module: biospolicyInstances
short_description: Retrieve all instances of type bios policy.  

description:
  - Allows to retrieve all instances of bios policy type. Also retrieves consistent device naming object if it exists .
 
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

try_list={}
def query_biospolicyInstances(input):
    ip=input['ip']
    username=input['username']
    password=input['password']
    exists=''
    temp_dict_obj={}
    ucs_handle = pickle.loads(str(ucs_login.main(ip,username,password)))
    try:
        mo = ucs_handle.query_classid("biosVProfile")
    except:
	results['error'] = "Could not query children of org-root"
        return results
    if mo:
	count=0
	for obj in mo:
            mo_children=ucs_handle.query_children(in_dn="org-root/bios-prof-"+obj.name,class_id="biosVfConsistentDeviceNameControl")

	    count=count+1
	    temp_dict_obj['consistent_device_naming']=mo_children[0].vp_cdn_control
	    temp_dict_obj['name']=obj.name
	    temp_dict_obj['descr']=obj.descr
	    try_list[count]=temp_dict_obj
	    temp_dict_obj={}
    else: 
	exists=""
    ucs_handle=pickle.dumps(ucs_handle)
    ucs_logout.main(ucs_handle)
    return try_list

def main(): 
    json_input=json.loads(sys.argv[1])
    results = query_biospolicyInstances(json_input)
    resultsjson=json.dumps(results)
    print(resultsjson)
    try_list={}

if __name__ == '__main__':
    main()
