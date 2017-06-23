ucsm_boot_policy{'PXE-Local-Boot':
   	policy_name => "bootutrui",
        order => "1",
	device_name => "Boot-L",
	type => "LocalLun",
        state => "present",
        ip => "172.28.224.121",
        username => "admin",
        password => "paasword",
}


