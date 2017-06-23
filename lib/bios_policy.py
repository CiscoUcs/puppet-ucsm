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
module: bios_policy
short_description: Create, modify or remove bios  policy 

description:
  - Allows to check if bios policy exists. If present, check for desired configuration. If desired config is not present, apply settings. If bios policy is not present, create and apply desired settings. If the desired state is 'absent', remove bios policy if it is currently present
 
version_added: "0.1.0"
author: 
    - "Cisco UCS Team"
    - "Pavan Koundinya"
'''

import sys
from ucsmsdk.mometa.bios.BiosVProfile import BiosVProfile
from ucsmsdk.mometa.bios.BiosVfQuietBoot import BiosVfQuietBoot
from ucsmsdk.mometa.bios.BiosVfPOSTErrorPause import BiosVfPOSTErrorPause
from ucsmsdk.mometa.bios.BiosVfResumeOnACPowerLoss import BiosVfResumeOnACPowerLoss
from ucsmsdk.mometa.bios.BiosVfFrontPanelLockout import BiosVfFrontPanelLockout
from ucsmsdk.mometa.bios.BiosVfConsistentDeviceNameControl import BiosVfConsistentDeviceNameControl
from ucsmsdk.mometa.bios.BiosVfIntelTurboBoostTech import BiosVfIntelTurboBoostTech
from ucsmsdk.mometa.bios.BiosVfEnhancedIntelSpeedStepTech import BiosVfEnhancedIntelSpeedStepTech
from ucsmsdk.mometa.bios.BiosVfIntelHyperThreadingTech import BiosVfIntelHyperThreadingTech
from ucsmsdk.mometa.bios.BiosVfCoreMultiProcessing import BiosVfCoreMultiProcessing
from ucsmsdk.mometa.bios.BiosVfExecuteDisableBit import BiosVfExecuteDisableBit
from ucsmsdk.mometa.bios.BiosVfIntelVirtualizationTechnology import BiosVfIntelVirtualizationTechnology
from ucsmsdk.mometa.bios.BiosVfProcessorPrefetchConfig import BiosVfProcessorPrefetchConfig
from ucsmsdk.mometa.bios.BiosVfDirectCacheAccess import BiosVfDirectCacheAccess
from ucsmsdk.mometa.bios.BiosVfProcessorCState import BiosVfProcessorCState
from ucsmsdk.mometa.bios.BiosVfProcessorC1E import BiosVfProcessorC1E
from ucsmsdk.mometa.bios.BiosVfProcessorC3Report import BiosVfProcessorC3Report
from ucsmsdk.mometa.bios.BiosVfProcessorC6Report import BiosVfProcessorC6Report
from ucsmsdk.mometa.bios.BiosVfProcessorC7Report import BiosVfProcessorC7Report
from ucsmsdk.mometa.bios.BiosVfProcessorCMCI import BiosVfProcessorCMCI
from ucsmsdk.mometa.bios.BiosVfCPUPerformance import BiosVfCPUPerformance
from ucsmsdk.mometa.bios.BiosVfMaxVariableMTRRSetting import BiosVfMaxVariableMTRRSetting
from ucsmsdk.mometa.bios.BiosVfLocalX2Apic import BiosVfLocalX2Apic
from ucsmsdk.mometa.bios.BiosVfProcessorEnergyConfiguration import BiosVfProcessorEnergyConfiguration
from ucsmsdk.mometa.bios.BiosVfFrequencyFloorOverride import BiosVfFrequencyFloorOverride
from ucsmsdk.mometa.bios.BiosVfPSTATECoordination import BiosVfPSTATECoordination
from ucsmsdk.mometa.bios.BiosVfDRAMClockThrottling import BiosVfDRAMClockThrottling
from ucsmsdk.mometa.bios.BiosVfInterleaveConfiguration import BiosVfInterleaveConfiguration
from ucsmsdk.mometa.bios.BiosVfScrubPolicies import BiosVfScrubPolicies
from ucsmsdk.mometa.bios.BiosVfAltitude import BiosVfAltitude
from ucsmsdk.mometa.bios.BiosVfPackageCStateLimit import BiosVfPackageCStateLimit
from ucsmsdk.mometa.bios.BiosVfCPUHardwarePowerManagement import BiosVfCPUHardwarePowerManagement
from ucsmsdk.mometa.bios.BiosVfEnergyPerformanceTuning import BiosVfEnergyPerformanceTuning
from ucsmsdk.mometa.bios.BiosVfWorkloadConfiguration import BiosVfWorkloadConfiguration
from ucsmsdk.ucshandle import UcsHandle
import json
import pickle
import ucs_login
import ucs_logout
def bios_policy(input):
	name = input['name']
	descr=input['descr']
	consistent_device_naming=input['consistent_device_naming']
	state = input['state']
	ip=input['ip']
	username=input['username']
	password=input['password']
	results = {}
	ucs_handle = pickle.loads(str(ucs_login.main(ip,username,password)))
###-------CHECK IF MO EXISTS---------------------------------

	try:
		mo = ucs_handle.query_dn("org-root/bios-prof-"+name)
		mo_block=ucs_handle.query_dn("org-root/bios-prof-"+name+"/Consistent-Device-Name-Control")
	except:
		results['error'] = "Could not query children of bios_policy"
		return results
###----if expected state is "present"------------------------

	if state == "present":
		if mo:
			if (mo.name == name and mo.descr == descr and mo_block.vp_cdn_control == consistent_device_naming ):
				results['name']=name;
				results['expected'] = True;
				results['changed'] = False;
				results['present'] = True;


			else:
		    		try:
					mo = BiosVProfile(parent_mo_or_dn="org-root", name=name, descr=descr)                                    
					modified_mo = BiosVfConsistentDeviceNameControl(parent_mo_or_dn=mo, vp_cdn_control=consistent_device_naming)
					results['name']=name;
					results['expected'] = False;
					results['changed'] = True;
					results['present'] = True;
					ucs_handle.add_mo(mo,True)
					ucs_handle.commit()
					#results['mo_bootpolicy'] = json.dumps(json.loads(jsonpickle.encode(mo)));


		   		except Exception as e:
					results['error'] = "Modification of bios policy mo failed"+str(e)
					return results
###----------if not, create boot policy with desired config ----------------

		else:
			try:
				mo = BiosVProfile(parent_mo_or_dn="org-root", name=name, descr=descr)
				mo_1 = BiosVfQuietBoot(parent_mo_or_dn=mo, vp_quiet_boot="platform-default")
				mo_2 = BiosVfPOSTErrorPause(parent_mo_or_dn=mo, vp_post_error_pause="platform-default")
				mo_3 = BiosVfResumeOnACPowerLoss(parent_mo_or_dn=mo, vp_resume_on_ac_power_loss="platform-default")
				mo_4 = BiosVfFrontPanelLockout(parent_mo_or_dn=mo, vp_front_panel_lockout="platform-default")
				mo_5 = BiosVfConsistentDeviceNameControl(parent_mo_or_dn=mo, vp_cdn_control=consistent_device_naming)
				mo_6 = BiosVfIntelTurboBoostTech(parent_mo_or_dn=mo, vp_intel_turbo_boost_tech="platform-default")
				mo_7 = BiosVfEnhancedIntelSpeedStepTech(parent_mo_or_dn=mo, vp_enhanced_intel_speed_step_tech="platform-default")
				mo_8 = BiosVfIntelHyperThreadingTech(parent_mo_or_dn=mo, vp_intel_hyper_threading_tech="platform-default")
				mo_9 = BiosVfCoreMultiProcessing(parent_mo_or_dn=mo, vp_core_multi_processing="platform-default")
				mo_10 = BiosVfExecuteDisableBit(parent_mo_or_dn=mo, vp_execute_disable_bit="platform-default")
				mo_11 = BiosVfIntelVirtualizationTechnology(parent_mo_or_dn=mo, vp_intel_virtualization_technology="platform-default")
				mo_12 = BiosVfProcessorPrefetchConfig(parent_mo_or_dn=mo, vp_dcuip_prefetcher="platform-default", vp_adjacent_cache_line_prefetcher="platform-default", vp_hardware_prefetcher="platform-default", vp_dcu_streamer_prefetch="platform-default")
				mo_13 = BiosVfDirectCacheAccess(parent_mo_or_dn=mo, vp_direct_cache_access="platform-default")
				mo_14 = BiosVfProcessorCState(parent_mo_or_dn=mo, vp_processor_c_state="platform-default")
				mo_15 = BiosVfProcessorC1E(parent_mo_or_dn=mo, vp_processor_c1_e="platform-default")
				mo_16 = BiosVfProcessorC3Report(parent_mo_or_dn=mo, vp_processor_c3_report="platform-default")
				mo_17 = BiosVfProcessorC6Report(parent_mo_or_dn=mo, vp_processor_c6_report="platform-default")
				mo_18 = BiosVfProcessorC7Report(parent_mo_or_dn=mo, vp_processor_c7_report="platform-default")
				mo_19 = BiosVfProcessorCMCI(parent_mo_or_dn=mo, vp_processor_cmci="platform-default")
				mo_20 = BiosVfCPUPerformance(parent_mo_or_dn=mo, vp_cpu_performance="platform-default")
				mo_21 = BiosVfMaxVariableMTRRSetting(parent_mo_or_dn=mo, vp_processor_mtrr="platform-default")
				mo_22 = BiosVfLocalX2Apic(parent_mo_or_dn=mo, vp_local_x2_apic="platform-default")
				mo_23 = BiosVfProcessorEnergyConfiguration(parent_mo_or_dn=mo, vp_power_technology="platform-default", vp_energy_performance="platform-default")
				mo_24 = BiosVfFrequencyFloorOverride(parent_mo_or_dn=mo, vp_frequency_floor_override="platform-default")
				mo_25 = BiosVfPSTATECoordination(parent_mo_or_dn=mo, vp_pstate_coordination="platform-default")
				mo_26 = BiosVfDRAMClockThrottling(parent_mo_or_dn=mo, vp_dram_clock_throttling="platform-default")
				mo_27 = BiosVfInterleaveConfiguration(parent_mo_or_dn=mo, vp_channel_interleaving="platform-default", vp_rank_interleaving="platform-default", vp_memory_interleaving="platform-default")
				mo_28 = BiosVfScrubPolicies(parent_mo_or_dn=mo, vp_patrol_scrub="platform-default", vp_demand_scrub="platform-default")
				mo_29 = BiosVfAltitude(parent_mo_or_dn=mo, vp_altitude="platform-default")
				mo_30 = BiosVfPackageCStateLimit(parent_mo_or_dn=mo, vp_package_c_state_limit="platform-default")
				mo_31 = BiosVfCPUHardwarePowerManagement(parent_mo_or_dn=mo, vp_cpu_hardware_power_management="platform-default")
				mo_32 = BiosVfEnergyPerformanceTuning(parent_mo_or_dn=mo, vp_pwr_perf_tuning="platform-default")
				mo_33 = BiosVfWorkloadConfiguration(parent_mo_or_dn=mo, vp_workload_configuration="platform-default")
				ucs_handle.add_mo(mo)
				ucs_handle.commit()
				results['name']=name;
				results['present'] = False;
				results['created'] = True;
				results['changed'] = True;
			#results['mo_bootpolicy'] = json.dumps(json.loads(jsonpickle.encode(mo)));


			

			except Exception as e:
				results['error'] = "Bios Policy creation failed"+str(e)
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

			except Exception as e:
				results['error'] = "Remove of bios policy mo failed"+str(e)
				return results
		else:
			results['name']=name;
			results['removed'] = False;
			results['present'] = False;
	ucs_handle=pickle.dumps(ucs_handle)
	ucs_logout.main(ucs_handle)
	return results
def main():
    json_input=json.loads(sys.argv[1])
    results = bios_policy(json_input)
    resultsjson=json.dumps(results)
    print(resultsjson)
    return resultsjson

if __name__ == '__main__':
    main()

