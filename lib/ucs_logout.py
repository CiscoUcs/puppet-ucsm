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

from ucsmsdk.ucshandle import UcsHandle
import json
import ucs_login
import pickle

class ucs_logout:
    def ucs_logout(self,handle):
	handle=pickle.loads(str(handle))

    	results = {}

    	try:
            handle.logout()
            results['logged_out'] = True
	    #print("Logged out successfully")
    	except:
            results['logged_out'] = True

        return results

def main(handle):
    logoutInstance=ucs_logout()
    results = logoutInstance.ucs_logout(handle)
if __name__ == '__main__':
    main()
