require 'ipaddr'
Puppet::Type.newtype(:ucsm_boot_policy) do
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

  newproperty(:type) do
    desc "The type of Local LUN Image path.Values acccepted are primary,secondary and any"
    validate do |value|
          if !(value.to_s.strip == "LAN" or value.to_s.strip == "LocalLun" or value.to_s.strip == "")
            raise  ArgumentError, "The type allowed is LAN/LocalLun "
          end
        end

  end

  newproperty(:device_name) do
    desc "The name of the Local LUN Image Path"
        validate do |value|
	if value != ""
          if value.length > 10
            raise  ArgumentError, "The device name exceeds maximum character length of 10"
          end
	end
        end

  end
  newproperty(:order) do
    desc "The name of the Local LUN Image Path"
    validate do |value|
	if !(value =~ /^-?[0-9]+$/ or value.to_s.strip == "")
		raise  ArgumentError, "The order should be an integer value %s" % value
	end
    end
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

