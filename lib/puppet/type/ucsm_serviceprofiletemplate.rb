Puppet::Type.newtype(:ucsm_serviceprofiletemplate) do
  desc "Puppet type that manages service profile template object"
  ensurable
  newparam(:typename ,:namevar => true) do
	desc "namevar for puppet object"
  end

  newproperty(:ip) do
	desc "The IP address of the ucspe server"
        validate do |value|
          begin
            ip = IPAddr.new "%s" % value
          rescue Exception
                raise  ArgumentError, "%s is not a valid IP address" % value
          end
        end

  end

  newproperty(:username) do
      validate do |value|
        unless value =~ /^\w+/
          raise ArgumentError, "%s is not a valid user name" % value
        end
	end
        desc "The username of ucspe user"
  end


  newproperty(:password) do
        desc "The password of ucspe user"
  end

  newproperty(:policy_name) do
    desc "The name of the managed object(This is with respect to ucspe)"
        validate do |value|
          if value.length > 16
            raise  ArgumentError, "The policy name exceeds maximum character length of 16"
          end
        end

  end

  newproperty(:type) do
    desc "Type of the template .'initial or updating'"
  end

  newproperty(:ident_pool_name) do
    desc "UUID Pool name"
  end

  newproperty(:local_disk_policy_name) do
    desc "Local disk Policy name"
  end

  newproperty(:boot_policy_name) do
    desc "Boot policy name"
  end

  newproperty(:bios_profile_name) do
    desc "Bios Profile name"
  end

  newproperty(:host_fw_policy_name) do
    desc "Host firmware package policy name"
  end

  newproperty(:mgmt_ip_address) do
    desc "Management IP address name"
  end

  newproperty(:maint_policy_name) do
    desc "Maintenance policy name"
  end

  newproperty(:vnic_name) do
    desc "vnic name"
  end

  newproperty(:vnic_template_name) do
    desc "Vnic template name"
  end

  newproperty(:adapter_profile_name) do
    desc "Adapter profile name"
  end

  newproperty(:storage_profile_name) do
    desc "Storage profile policy name"
  end

  newproperty(:server_pool_name) do
    desc "Server pool name"
  end

  newproperty(:vnic_order) do
    desc "Order of Vnic"
  end

  newproperty(:state) do
    desc "ensure whether the managed object is present or absent"
    newvalue(:present)
    newvalue(:absent)
  end

  validate do
    fail ("The 'IP address' parameter must be set in the manifest.") if self[:ip].to_s.strip.empty?
    fail ("The 'Policy name' parameter must be set in the manifest.") if self[:policy_name].to_s.strip.empty?
    fail ("The 'state' parameter must be set in the manifest.") if self[:state].to_s.strip.empty?
    fail ("The 'username' parameter must be set in the manifest.") if self[:username].to_s.strip.empty?
    fail ("The 'password' parameter must be set in the manifest.") if self[:password].to_s.strip.empty?
  end
end

