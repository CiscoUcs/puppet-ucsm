ucsm_wwn_pool{'wwnn_pool':
policy_name => 'WWNN_Pool',
purpose     => 'node',
r_from      => '20:00:00:25:B5:FF:00:00',
to          => '20:00:00:25:B5:FF:01:FF',
ip          => '172.16.143.139',
username    => 'admin',
password    => 'password',
state       => 'present',
}
ucsm_wwn_pool{'wwpn_pool_a':
policy_name => 'WWPN_Pool_A',
purpose     => 'port',
r_from      => '20:00:00:25:B5:0A:00:00',
to          => '20:00:00:25:B5:0A:01:FF',
ip          => '172.16.143.139',
username    => 'admin',
password    => 'password',
state       => 'present',
}
ucsm_wwn_pool{'wwpn_pool_b':
policy_name => 'WWPN_Pool_B',
purpose     => 'port',
r_from      => '20:00:00:25:B5:0B:00:00',
to          => '20:00:00:25:B5:0B:01:FF',
ip          => '172.16.143.139',
username    => 'admin',
password    => 'password',
state       => 'present',
}
