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
module: query_boot_policymo
short_description: Checks if boot policy mo with the name exists.

description:
  - Allows to check if boot policy exists. If present, returns true else returns false.
 
version_added: "0.1.0"
author: 
    - "Cisco UCS Team"
    - "Pavan Koundinya"
'''

import sys
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

def query_mo(input):
    name=input['name']
    type=input['type']
    device_name=input['device_name']
    ip=input['ip']
    username=input['username']
    password=input['password']
    exists=''
    mo_children_exists=False
    ucs_handle = pickle.loads(str(ucs_login.main(ip,username,password)))
    try:
        mo = ucs_handle.query_dn("org-root/boot-policy-"+name)
	if(type == "LAN"):
	    mo_children =ucs_handle.query_children(in_dn="org-root/boot-policy-"+name+"/lan",hierarchy=True)
	    for obj in mo_children:
	    	if(obj.vnic_name==device_name):
		    mo_children_exists=True
	elif(type == "LocalLun"):
	    mo_children = ucs_handle.query_children(in_dn="org-root/boot-policy-"+name+"/storage/local-storage/local-hdd",hierarchy=True)
	    for obj in mo_children:
		if(obj.lun_name == device_name):
		    mo_children_exists=True	    	
    except Exception,e:
	print(Exception)
	print(e)
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
    results = query_mo(json_input)
    resultsjson=results
    print(resultsjson)
    #return resultsjson

if __name__ == '__main__':
    main()
