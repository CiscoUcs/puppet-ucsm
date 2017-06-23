ucsm_serverpool{'ComputePool':
policy_name => "puppettest",
descr => "qwert",
pooled_servers => [{"slot_id" => "2","chassis_id" =>"5"},{"slot_id" =>"5","chassis_id"=>"8"},{"slot_id"=>"1","chassis_id" => "4"},{"slot_id" =>"6","chassis_id"=>"7"},{"slot_id"=>"3","chassis_id" => "4"},{"slot_id"=>"2","chassis_id" => "1"}],
ip => "172.28.224.133",
username => "admin",
password => "password",
state => "present",
}
