# frozen_string_literal: true

require "awspec"
require "rhcl"
require_relative "setup"

 describe sqs(SQS_ID) do
     puts "This object #{it}."
     #its(:name) { should eq 'testkitchen' }
     if SQS_NAME == 'testkitchen'
        return true
     end
end


