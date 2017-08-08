Puppet::Type.newtype(:ucsm_serviceprofile) do
  desc "Puppet type that manages service profile object"
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

  newproperty(:src_templ_name) do
    desc "Source Service Profile Template name"
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

