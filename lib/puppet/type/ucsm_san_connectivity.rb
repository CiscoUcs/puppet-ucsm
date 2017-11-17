Puppet::Type.newtype(:ucsm_san_connectivity) do
  desc "Puppet type that manages san connectivity policies"
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
    desc "The name of the SAN connectivity policy"
        validate do |value|
          if value.length > 32
            raise  ArgumentError, "The policy name exceeds maximum character length of 32"
          end
        end

  end

  newproperty(:descr) do
    desc "The description of the vHBA template"
  end

  newproperty(:wwnn_pool) do
    desc "WWNN Pool name"
  end

  newproperty(:vhba_list, :array_matching => :all) do
    desc "List of vHBAs contained in the SAN Connectivity Policy. Each list element has the following suboptions: name (Name of the vHBA (required)), vhba_template (vHBA template (required)), adapter_policy ('' (default), Linux, Solaris, VMware, Windows, WindowsBoot, or default), order (string specifying vHBA assignment order ('1', '2', etc.) (required))"
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

