require 'json'

Puppet::Type.type(:ucsm_serviceprofiletemplate).provide :ruby do
 
  mk_resource_methods
  def handle
     # Retriving all the parameters from the manifests
     param_obj=Hash.new
     param_obj[:name]=@resource[:policy_name]
     param_obj[:ip]=@resource[:ip]
     param_obj[:username]=@resource[:username]
     param_obj[:password]=@resource[:password]
     param_obj[:type] = @resource[:type]
     param_obj[:ident_pool_name] = @resource[:ident_pool_name]
     param_obj[:local_disk_policy_name] = @resource[:local_disk_policy_name]
     param_obj[:boot_policy_name] = @resource[:boot_policy_name]
     param_obj[:bios_profile_name] = @resource[:bios_profile_name]
     param_obj[:host_fw_policy_name] = @resource[:host_fw_policy_name]
     param_obj[:mgmt_ip_address] = @resource[:mgmt_ip_address]
     param_obj[:maint_policy_name] = @resource[:maint_policy_name]
     param_obj[:vnic_name] = @resource[:vnic_name]
     param_obj[:vnic_template_name] = @resource[:vnic_template_name]
     param_obj[:adapter_profile_name] = @resource[:adapter_profile_name]
     param_obj[:storage_profile_name] = @resource[:storage_profile_name]
     param_obj[:server_pool_name] = @resource[:server_pool_name]
     param_obj[:vnic_order]=@resource[:vnic_order]
     param_obj[:state]=@resource[:state]
     #converting object to JSON string
     json_object=JSON.dump param_obj.to_json
     #Call to the python script using puppet execute along with all the parameters 
     path = File.join(File.dirname(__FILE__), '..', '..', '..')
     current = Puppet::Util::Execution.execute(
      "python #{path}/service_profile.py #{json_object}",
      :failonfail => true
    )
Puppet.debug("#{current}")
Puppet.debug("After execution")
#Parse and send notice of the output of the execute command
json=JSON.parse(current)
if(json['changed'] or json['removed'] or json['error'])
	notice(red(current))
else
	notice(green(current))
end


end

def colorize(text, color_code)
  "\e[#{color_code}m#{text}\e[0m"
end

def red(text); colorize(text, 31); end
def green(text); colorize(text, 32); end
    

  def exists?
     	param_obj=Hash.new
     	param_obj[:name]=@resource[:policy_name]
     	param_obj[:ip]=@resource[:ip]
     	param_obj[:username]=@resource[:username]
     	param_obj[:password]=@resource[:password]
    	param_obj[:type] = @resource[:type]
    	param_obj[:ident_pool_name] = @resource[:ident_pool_name]
    	param_obj[:local_disk_policy_name] = @resource[:local_disk_policy_name]
    	param_obj[:boot_policy_name] = @resource[:boot_policy_name]
     	param_obj[:bios_profile_name] = @resource[:bios_profile_name]
     	param_obj[:host_fw_policy_name] = @resource[:host_fw_policy_name]
     	param_obj[:mgmt_ip_address] = @resource[:mgmt_ip_address]
     	param_obj[:maint_policy_name] = @resource[:maint_policy_name]
     	param_obj[:vnic_name] = @resource[:vnic_name]
     	param_obj[:vnic_template_name] = @resource[:vnic_template_name]
     	param_obj[:adapter_profile_name] = @resource[:adapter_profile_name]
     	param_obj[:storage_profile_name] = @resource[:storage_profile_name]
     	param_obj[:server_pool_name] = @resource[:server_pool_name]
     	param_obj[:vnic_order]=@resource[:vnic_order]

     	json_object=JSON.dump param_obj.to_json	
	path = File.join(File.dirname(__FILE__), '..', '..', '..')
     	current = Puppet::Util::Execution.execute(
      	"python #{path}/query_service_profile_template.py #{json_object}",
      	:failonfail => true
    	)
 	if(current.eql? "true")
	return true
	else
 	return false
	end
  end

  def initialize(value={})
    super(value)
    @property_flush = {}
  end

  def create
    	handle
	@property_hash[:state] == :present
  end
  def destroy
	@property_flush[:state]= :absent
  end

  def self.get_instance(resource)
	param_obj=Hash.new
        param_obj[:ip]=resource[:ip]
        param_obj[:username]=resource[:username]
        param_obj[:password]=resource[:password]
	json_object=JSON.dump param_obj.to_json
        path = File.join(File.dirname(__FILE__), '..', '..', '..')
        current = Puppet::Util::Execution.execute(
        "python #{path}/serviceProfileTemplateInstances.py #{json_object}",
        :failonfail => true
        )
  end

  def self.instances(resource)
    #creating a dummy instance for the purpose of populating the resource values
    #Not exactly sure but its working !!!!
    arr=Array.new
    conf=self.get_instance(resource)
    #notice("After call to self.get_ instance :::: #{conf} ")
    list_objects=JSON.parse(conf)
    list_objects.each do |key,json_obj|
	temp=json_obj
	arr.push(json_obj)
    end	
  arr
  end

def self.prefetch(resources)
#retriving the dummy instance comparing the name and then setting the al
#property values for later access  
  resources.each do |name,res|
	list_instances=instances(res)
	list_instances.each do |a| 
		if @resource = resources[a['name']]
			resource.provider=a
		end 
	end
  end   
end
end

