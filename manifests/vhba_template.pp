ucsm_vhba_template {'vhba_templ_a':
policy_name => 'vHBA_A',
fabric      => 'A',
vsan        => 'VSAN_A',
wwpn_pool   => 'WWPN_Pool_A',
ip          => '172.16.143.139',
username    => 'admin',
password    => 'password',
state       => 'present',
}
