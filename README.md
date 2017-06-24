# puppet-ucsm

#### Table of Contents
1. [Module Description](#Module-Description)
2. [Setup - The basics of getting started with ucsm](#setup)
3. [Example-Manifests](#Example-Manifests)
4. [Reference - An under-the-hood peek at what the module is doing and how](#reference)
5. [Limitations - OS compatibility, etc.](#limitations)
6. [Development - Guide for contributing to the module](#development)

## Module-Description
The Cisco Puppet module for UCSM allows administrators to automate all aspects of Cisco UCS management including server, network, storage and hypervisor management. The bulk of the Cisco UCSM Puppet module workon the UCS Manager’s Management Information Tree (MIT), performing create, modify or delete actions on the Managed Objects (MO) in the tree. 
The resources and capabilities provided by this Puppet Module will grow with contributions from Cisco, Puppet Labs and the open source community.

##### Dependencies

The ucsm module has a dependency on the ucsmsdk python library. See the Setup section that follows for more information on ucsmsdk.

##### Contributing

Contributions to the ciscopuppet module are welcome. See CONTRIBUTING.md for guidelines.

## Setup
###### Puppet Master

To install git use the following command :
   ``` 
   yum install git -y
   ```
The ucsm module must be cloned on the Puppet Master server. We recommend cloning in the modules directory.

   ```
   git clone https://github.com/CiscoUcs/puppet-ucsm ucsm
   ``` 
  
To install pip package installer use the following commands.
   - ``` curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py ```
   - ``` python get-pip.py  ```
After pip is installed successfully install the ucsmsdk package using the following command.
   - ```pip install ucsmsdk  ```
   
   


Software version Dependencies
   - Puppet 4.x
   - Python 2.7.x
   


## Example-Manifests

##### Bios Policy example manifest:
The following example demonstrates how to define a manifest that uses the ucsm module  to configure bios policy on a Cisco UCS.

```
ucsm_bios_policy{'biosVProfile':                                                                              
policy_name => "Docker-BiosPol",                                                                                   
descr =>"",                                                                                              
consistent_device_naming => "enabled",                                                                       
ip => "IP address of the UCS server",                                                                                       
username => "",                                                                                          
password => "",                                                                                       
state => "present",                                                                                           
} 
```

###### Description of parameters :

ucsm_bios_profile => The bios policy resource type defined in Puppet DSL. This is required to identify which resource we intend to configure.

policy_name => The name of the policy to be configured.

descr => Description for the policy.

consistent_device_naming => This parameter defines whether device naming should be consistent across all platforms.Allowed values are "enabled" or "disabled".

ip => the IP address of the UCS server.

username => The administrative username

password => The administrative password

state => This parameter ensures whether the policy should be present or absent on the UCS server.

##### Vlan example manifest :
The following example demonstrates how to define a manifest that uses the ucsm module  to configure Vlan on a Cisco UCS.

```
ucsm_vlan{'fabricVlan':
policy_name => "vlan603",
id => "603",
default_net => "yes",
ip => "IP address of the UCS server",
username => "",
password => "",
state => "present",
}
```

###### Description of parameters :

ucsm_vlan => The Vlan resource type defined in Puppet DSL. This is required to identify which resource we intend to configure.

policy_name => The name of the policy to be configured.

default_net => If the newly created VLAN is a native VLAN then this parameter has to be set to "yes". Otherwise it should be set to "no".

id => The range of Vlan id's (e.g. "2009-2019","29,35,40-45","23","23,34-45")

ip => "the IP address of the UCS server"

username => The administrative username

password => The administrative password

state => This parameter ensures whether the policy should be present or absent on the UCS server.

##### Boot Policy example manifest :
The following example demonstrates how to define a manifest that uses the ucsm module  to configure boot policy on a Cisco UCS.

```
ucsm_boot_policy{'PXE-Local-Boot':
        policy_name => "Docker-LocalBoot",
        order => "1",
        device_name => "Boot-Lun",
        type => "LocalLun",
        state => "present",
        ip => "the IP address of the UCS server",
        username => "",
        password => "",
}
```

###### Description of parameters :

ucsm_boot_policy => The boot policy resource type defined in Puppet DSL. This is required to identify which resource we intend to configure.

policy_name => The name of the policy to be configured.

order => The boot order for the boot device. 

device_name => The name of the device

type => The type of device (e.g. Local-Lun , Lan-Boot etc)

ip => the IP address of the UCS server.

username => The administrative username

password => The administrative password

state => This parameter ensures whether the policy should be present or absent on the UCS server.

##### Macpool example manifest :
The following example demonstrates how to define a manifest that uses the ucsm module  to configure mac pool on a Cisco UCS.

```
ucsm_macpool{'macpoolPool':
policy_name => "macpool12",
descr =>"em",
to => "00:25:B5:00:00:14",
r_from => "00:25:B5:00:00:12",
ip => "IP address of UCS server",
username => "",
password => "",
state => "present",
}
```

###### Description of parameters :

ucsm_macpool => The mac pool resource type defined in Puppet DSL. This is required to identify which resource we intend to configure.

policy_name => The name of the policy to be configured.

descr => The description for the macpool. 

to => The end of mac pool address range

r_from => The start of mac pool address range

ip => the IP address of the UCS server.

username => The administrative username

password => The administrative password

state => This parameter ensures whether the policy should be present or absent on the UCS server.

##### Uuidpool example manifest :
The following example demonstrates how to define a manifest that uses the ucsm module  to configure uuid pool on a Cisco UCS.

```
ucsm_uuid_pool{'Pool':
policy_name => "uuidPool1",
descr =>"",
to => "0000-000000000009",
r_from => "0000-000000000008",
ip => "IP address of UCS Server",
username => "",
password => "",
state => "present",
}
```

###### Description of parameters :

ucsm_uuid_pool => The uuid pool resource type defined in Puppet DSL. This is required to identify which resource we intend to configure.

policy_name => The name of the policy to be configured.

descr => The description for the uuidpool. 

to => The end of uuid pool address range

r_from => The start of uuid pool address range

ip => the IP address of the UCS server.

username => The administrative username

password => The administrative password

state => This parameter ensures whether the policy should be present or absent on the UCS server.

##### Disk group configuration policy example manifest :
The following example demonstrates how to define a manifest that uses the ucsm module  to configure disk group configuration policy on Cisco UCS.

```
ucsm_disk_group_policy{'diskgroupconfiguration':
policy_name => "",
slot_numbers => ["1","2","3","4","5","6"],
raid_level => "stripe-parity",
ip => "",
username => "",
password => "",
state => "present",
}
```

###### Description of parameters :


ucsm_disk_group_policy => The ucsm_disk_group_policy resource type defined in Puppet DSL. This is required to identify which resource we intend to configure.

policy_name => The name of the policy to be configured.

descr => The description for the uuidpool. 

slot_numbers => A list of slot numbers to be assigned to the disk group configuration.

raid_level => e.g. "mirror" ,"striped-parity"

ip => the IP address of the UCS server.

username => The administrative username

password => The administrative password

state => This parameter ensures whether the policy should be present or absent on the UCS server.

##### Host firmware package example manifest :
The following example demonstrates how to define a manifest that uses the ucsm module  to configure Host firmware package on Cisco UCS.

```
ucsm_hostfirmwarepackage{'firmwareComputeHostPack':
        policy_name => "package",
        descr => "",
        state => "present",
        ip => "",
        username => "",
        password => "",
}
```

Description of parameters :

ucsm_hostfirmwarepackage => The ucsm_hostfirmwarepackage resource type defined in Puppet DSL. This is required to identify which resource we intend to configure.

policy_name => The name of the policy to be configured.

descr => The description for the uuidpool. 

ip => the IP address of the UCS server.

username => The administrative username

password => The administrative password

state => This parameter ensures whether the policy should be present or absent on the UCS server.

##### Server pool example manifest :
The following example demonstrates how to define a manifest that uses the ucsm module  to configure server pool on Cisco UCS.

```
ucsm_serverpool{'ComputePool':
policy_name => "",
descr => "",
pooled_servers => [{"slot_id" => "2","chassis_id" =>"5"},{"slot_id" =>"5","chassis_id"=>"8"}],
ip => "",
username => "",
password => "",
state => "",
}
```

###### Description of parameters :

ucsm_serverpool => The ucsm_serverpool resource type defined in Puppet DSL. This is required to identify which resource we intend to configure.

policy_name => The name of the policy to be configured.

descr => The description for the uuidpool. 

pooled_servers => A list of dictionary objects. Each dictionary object contains slot id and chassis id.

ip => the IP address of the UCS server.

username => The administrative username

password => The administrative password

state => This parameter ensures whether the policy should be present or absent on the UCS server.

##### Vnic template example manifest :
The following example demonstrates how to define a manifest that uses the ucsm module  to configure vnic template on Cisco UCS.

```
ucsm_vnic_template {"vnicLanConnTempl":
policy_name =>"puppetdslmo",
descr => "",
switch_id =>"A",
templ_type => "updating-template",
vlan_name => "",
default_net =>"",
cdn_source => "user-defined",
admin_cdn_name =>"cdnnam",
mtu => "1600",
ident_pool_name => "",
ip => "172.28.224.121",
username => "admin",
password => "password",
state => "present",
}
```

###### Description of parameters :

ucsm_vnic_template => The ucsm_vnic_template resource type defined in Puppet DSL. This is required to identify which resource we intend to configure.

policy_name => The name of the policy to be configured.

descr => The description for the vnic template. 

switch_id => e.g. "A" or "B" or "A-B"

templ_type => The template type ."initial-template" or "updating-template"

vlan_name => The vlan name to be associated with the template

default_net => "yes" to set as native LAN otherwise "no"

cdn_source => Set to either "vnic-name" or "user-defined"

admin_cdn_name => Name of the CDN

mtu => MTU size between 1500-9000

ident_pool_name => Identical pool name

ip => the IP address of the UCS server.

username => The administrative username

password => The administrative password

state => This parameter ensures whether the policy should be present or absent on the UCS server.

##### Storage profile example manifest :
The following example demonstrates how to define a manifest that uses the ucsm module  to configure storage profile on Cisco UCS.

```
ucsm_storageprofile{'storageprofile':
policy_name => "Docker-storage",
local_lun_list => [{"name" => "Boot-Lun","size" => "50","disk_group_configuration_name" => "pte88","slot_number" => ["1","2"]}, {"name" => "Data-Lun","size" => "20","disk_group_configuration_name" => "puppettes","slot_number" => ["1","2"]}],
ip => "",
username => "",
password => "",
state => "present",
}
```

###### Description of parameters :

ucsm_storageprofile => The ucsm_storageprofile resource type defined in Puppet DSL. This is required to identify which resource we intend to configure.

policy_name => The name of the policy to be configured.

local_lun_list => A list of dictionary objects. Each object consists of following variables.
                  name => Name of Local Lun
                  size => Size in GB.
                  disk_group_configuration_name => The disk group configuration policy name to associate with the Local LUN.

ip => the IP address of the UCS server.

username => The administrative username

password => The administrative password

state => This parameter ensures whether the policy should be present or absent on the UCS server.

##### Service profile template example manifest :
The following example demonstrates how to define a manifest that uses the ucsm module  to configure service profile template on Cisco UCS.

```
ucsm_serviceprofiletemplate{'serviceprofiletemplate':
policy_name => "",
type  => "",
storage_profile_name => "",
vnic_name => "",
vnic_template_name => "",
adapter_profile_name => "Linux",
vnic_order => "",
server_pool_name => "",
local_disk_policy_name => "",
ident_pool_name=> "",
host_fw_policy_name => "",
boot_policy_name => "",
bios_profile_name => "",
maint_policy_name => "",
mgmt_ip_address => "",
ip => "",
username => "",
password => "",
state => "present",
}
```

###### Description of parameters :

ucsm_serviceprofiletemplate => The ucsm_serviceprofiletemplate resource type defined in Puppet DSL. This is required to identify which resource we intend to configure.

policy_name => The name of the policy to be configured.

type => The type of template."updating-template" or "initial-template".

storage_profile_name => Name of storage profile to be associated with the service profile.

vnic_name => New VNIC name .

vnic_template_name => VNIC template to be associated with the service profile template.

adapter_profile_name => The Name of  adaptor profile to be associated with the service profile template.

vnic_order => The order of VNIC being associated with the service profile template. 1 for primary and 2 for secondary.

server_pool_name => The name of server pool to be associated with the service profile template.

local_disk_policy_name => The name of local disk policy to be associated with the service profile template.

ident_pool_name => The name of uuid pool to be associated with the service profile template.

host_fw_policy_name => The name of host firmware policy to be associated with the service profile template.

boot_policy_name => The name of boot policy  to be associated with the service profile template.

bios_profile_name => The name of bios policy  to be associated with the service profile template.

maint_policy_name => The name of maintenance policy  to be associated with the service profile template.

mgmt_ip_address => The name of management ip address pool  to be associated with the service profile template.

ip => the IP address of the UCS server.

username => The administrative username

password => The administrative password

state => This parameter ensures whether the policy should be present or absent on the UCS server.

## Reference

Here, include a complete list of your module's classes, types, providers,
facts, along with the parameters for each. Users refer to this section (thus
the name "Reference") to find specific details; most users don't read it per
se.

## Limitations

This is where you list OS compatibility, version compatibility, etc. If there
are Known Issues, you might want to include them under their own heading here.

## Development

Since your module is awesome, other users will want to play with it. Let them
know what the ground rules for contributing are.

## Release Notes/Contributors/Etc. **Optional**

If you aren't using changelog, put your release notes here (though you should
consider using changelog). You can also add any additional sections you feel
are necessary or important to include here. Please use the `## ` header.
