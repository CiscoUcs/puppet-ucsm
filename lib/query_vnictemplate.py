
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
module: query_vnictemplate
short_description: Queries UCSPE for a specific vnic template policy managed object .Returns TRUE if object exists else returns FALSE.


description:
  - Allows to check if vnic template policy exists. If vnic template policy with the name exists then the script returns TRUE else it returns FALSE.

 
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

def query_vnictemplate(input):
    name=input['name']
    ip=input['ip']
    username=input['username']
    password=input['password']
    vlan_name=input['vlan_name']
    exists=''
    ucs_handle = pickle.loads(str(ucs_login.main(ip,username,password)))
    try:
        mo = ucs_handle.query_dn("org-root/lan-conn-templ-"+name)
	if(vlan_name <> ""):
		mo_block=ucs_handle.query_dn("org-root/lan-conn-templ-"+name+"/if-"+vlan_name)
	else:
	    mo_block=True
    except:
        print("Could not query children of org-root")
    if (mo and mo_block):
	exists="true"
    else: 
	exists="false"
    ucs_handle=pickle.dumps(ucs_handle)
    ucs_logout.main(ucs_handle)
    return exists

def main():
    
    json_input=json.loads(sys.argv[1])
    results = query_vnictemplate(json_input)
    resultsjson=results
    print(resultsjson)
    #return resultsjson

if __name__ == '__main__':
    main()
