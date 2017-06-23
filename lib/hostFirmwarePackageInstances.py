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
module: hostFirmwarePackageInstances
short_description: Retrieve all instances of type host firmware package. 

description:
  - Queries the UCSPE to retrieve all instances of the host firmware package type.Returns a dictionary containing each host firmware package instance object as value .The value is again a dictionary that contains the current configuration.
E.g
{"1": {"name": "utility", "descr": "", "reboot_on_update": "no", "policy_owner": "local", "enforce_vnic_name": "no", "boot_mode": "legacy"}, "2": {"name": "default", "descr": "", "reboot_on_update": "no", "policy_owner": "local", "enforce_vnic_name": "no", "boot_mode": "legacy"}}

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

try_list={}
def query_instance(input):
    ip=input['ip']
    username=input['username']
    password=input['password']
    exists=''
    temp_dict_obj={}
    ucs_handle = pickle.loads(str(ucs_login.main(ip,username,password)))
    try:
        mo = ucs_handle.query_classid("firmwareComputeHostPack")
    except:
        print("Could not query children of org-root")
    if mo:
	count=0
	for obj in mo:
	    count=count+1
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
    results = query_instance(json_input)
    resultsjson=json.dumps(results)
    print(resultsjson)
    try_list={}
    #return resultsjson

if __name__ == '__main__':
    main()
