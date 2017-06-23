Puppet::Type.newtype(:ucsm_vnic_template) do
  desc "Puppet type that manages boot policy object"
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

  newproperty(:descr) do
    desc "The description of the managed object"
        validate do |value|
          if value.length > 256
            raise  ArgumentError, "The policy name exceeds maximum character length of 256"
          end
        end
  end

  newproperty(:switch_id) do
    desc "Switch id  set to either 'A' or 'B' or 'A-B' to enable failover"
  end


  newproperty(:templ_type) do
    desc "option to enforce the vnic name .set to either yes/no"
    validate do |value|
	if !(value.to_s.strip == "updating-template" or value.to_s.strip == "initial-template")
		            raise  ArgumentError, "The template type should have a valid value. Allowed values are initial-template or updating-template"
          end
        end
 
 end

  newproperty(:vlan_name) do
    desc "boot mode for current managed object"
  end

  newproperty(:default_net) do
    desc "boot mode for current managed object"
  end

  newproperty(:cdn_source) do
    desc "boot mode for current managed object"
    validate do |value|
        if !(value.to_s.strip == "vnic-name" or value.to_s.strip == "user-defined")
                            raise  ArgumentError, "The cdn source should have a valid value. Allowed values are vnic-name or user-defined"
          end
        end

  end

  newproperty(:admin_cdn_name) do
    desc "boot mode for current managed object"
        validate do |value|
          if value.length > 16
            raise  ArgumentError, "The admin cdn name exceeds maximum character length of 16"
          end
        end
 end

  newproperty(:mtu) do
    desc "boot mode for current managed object"
        validate do |value|
          if !(value.to_i.between?(1500,9000))
            raise  ArgumentError, "The mtu size has to be between 1500-9000"
          end
        end
  end

  newproperty(:ident_pool_name) do
    desc "boot mode for current managed object"
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
    fail ("The 'switch_id' parameter must be set in the manifest.") if self[:switch_id].to_s.strip.empty?
    fail ("The 'templ_type' parameter must be set in the manifest.") if self[:templ_type].to_s.strip.empty?
    fail ("The 'cdn_source' parameter must be set in the manifest.") if self[:cdn_source].to_s.strip.empty?
    fail ("The 'mtu' parameter must be set in the manifest.") if self[:mtu].to_s.strip.empty?
    fail ("The 'username' parameter must be set in the manifest.") if self[:username].to_s.strip.empty?
    fail ("The 'password' parameter must be set in the manifest.") if self[:password].to_s.strip.empty?
   end

end

