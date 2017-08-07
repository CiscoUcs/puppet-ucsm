ucsm_storageprofile{'storageprofile':
policy_name    => 'pretest1',
local_lun_list => [{'name' => 'Boot-Lun','size' => '50','disk_group_configuration_name' => 'iptest'},{'name' => 'Data-Lun','size' => '20','disk_group_configuration_name' => 'yt'}],
ip             => '172.28.224.133',
username       => 'admin',
password       => 'password',
state          => 'present',
}
