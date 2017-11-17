ucsm_san_connectivity{'san_connectivity':
policy_name => 'SAN_Ex',
wwnn_pool   => 'WWNN_Pool',
vhba_list   => [{'name' => 'Fabric-A','vhba_template' => 'vHBA_A','adapter_policy' => 'Linux','order' => '1'},{'name' => 'Fabric-B','vhba_template' => 'vHBA_B','adapter_policy' => 'Linux','order' => '2'}],
ip          => '172.16.143.139',
username    => 'admin',
password    => 'password',
state       => 'present',
}
