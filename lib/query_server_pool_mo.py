
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
module: query_server_pool_mo
short_description: Queries UCSPE to check whether server pool object exists. 

description:
  - Allows to check if server pool managed object exists. If present returns true else returns false.
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

def query_server_pool_mo(input):
    name=input['name']
    ip=input['ip']
    username=input['username']
    password=input['password']
    pooled_servers=input['pooled_servers']
    exists=''
    ucs_handle = pickle.loads(str(ucs_login.main(ip,username,password)))
    try:
		mo = ucs_handle.query_dn("org-root/compute-pool-"+name)
		if(mo and len(pooled_servers) <> 0):
			pooled_server_exists = True
			for obj in pooled_servers:
				mo_block=ucs_handle.query_dn("org-root/compute-pool-"+name+"/blade-"+obj['chassis_id']+"-"+obj['slot_id'])
				pooled_server_exists = (pooled_server_exists and mo_block)
    except Exception as e :
        print("Could not query children of org-root" + str (e))
    if (mo and pooled_server_exists):
		exists="true"
    else: 
		exists="false"
    ucs_handle=pickle.dumps(ucs_handle)
    ucs_logout.main(ucs_handle)
    return exists

def main():
    json_input=json.loads(sys.argv[1])
    results = query_server_pool_mo(json_input)
    resultsjson=results
    print(resultsjson)
    #return resultsjson

if __name__ == '__main__':
    main()
