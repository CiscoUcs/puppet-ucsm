require 'spec_helper'
describe 'ucsm' do
  context 'with default values for all parameters' do
    it { should contain_class('ucsm') }
  end
end
