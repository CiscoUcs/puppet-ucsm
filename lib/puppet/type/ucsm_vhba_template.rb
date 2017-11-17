Puppet::Type.newtype(:ucsm_vhba_template) do
  desc "Puppet type that manages vhba templates"
  ensurable
  newparam(:typename ,:namevar => true) do
	desc "namevar for puppet object"
  end

  newproperty(:ip) do
	desc "The IP address of UCSM"
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
        desc "The username of the UCSM user"
  end


  newproperty(:password) do
        desc "The password of the UCSM user"
  end

  newproperty(:policy_name) do
    desc "The name of the vhba template"
        validate do |value|
          if value.length > 32
            raise  ArgumentError, "The policy name exceeds maximum character length of 32"
          end
        end

  end

  newproperty(:descr) do
    desc "The description of the vHBA template"
  end

  newproperty(:fabric) do
    desc "Fabric ID.  Either 'A' (default) or 'B'"
  end

  newproperty(:redundancy_type) do
    desc "Redundancy Type.  'none' (default), 'primary', or 'secondary'"
  end

  newproperty(:vsan) do
    desc "VSAN name"
  end

  newproperty(:template_type) do
    desc "Template Type.  'initial-template' (default) or 'updating-template'"
  end

  newproperty(:max_data) do
    desc "Max Data Field Size as a string.  Default is '2048'"
  end

  newproperty(:wwpn_pool) do
    desc "WWPN Pool name.  Default is 'default'"
  end

  newproperty(:qos_policy) do
    desc "QoS Policy name"
  end

  newproperty(:pin_group) do
    desc "Pin Group"
  end

  newproperty(:stats_policy) do
    desc "Stats Threshold Policy name.  Default is 'default'"
  end

  newproperty(:org_dn) do
    desc "Org dn (distinguished name).  Default is 'org-root'"
  end

  newproperty(:state) do
    desc "ensure whether the managed object is present or absent"
    newvalue(:present)
    newvalue(:absent)
  end

  validate do
    fail ("The 'IP address' parameter must be set in the manifest.") if self[:ip].to_s.strip.empty?
    fail ("The 'username' parameter must be set in the manifest.") if self[:username].to_s.strip.empty?
    fail ("The 'password' parameter must be set in the manifest.") if self[:password].to_s.strip.empty?
    fail ("The 'state' parameter must be set in the manifest.") if self[:state].to_s.strip.empty?
    fail ("The 'policy_name' parameter must be set in the manifest.") if self[:policy_name].to_s.strip.empty?
  end
end

