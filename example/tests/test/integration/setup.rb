# frozen_string_literal: true


main_tf = Rhcl.parse(File.open("/tmp/sqs_queue/tests/test/fixtures/kms.tf"))
puts 'main_tf'
puts main_tf
module_sqs = main_tf["module"]["sqs_queue"]



# rubocop:disable LineLength
state_file = 'terraform.tfstate.d/kitchen-terraform-base-aws/terraform.tfstate'
tf_state = JSON.parse(File.open(state_file).read)

tf_state.each_with_index {|val, index|

    puts val

    if val.instance_of? Array
        puts 'is an array'
    end

    puts tf_state[index]

    item = val.to_s

    puts 'item'
    puts item[0]

    if val[0] == 'modules'
        puts 'found modules'

        val[1].each_with_index{|nval, nindex|
            puts 'nval'
            puts nval
            if nval.instance_of? Hash
                puts 'is a hash'

                if nval.has_key?('resources')

                    nval['resources'].each_with_index {|val2, index2|
                        puts val2
                        puts index2
                    }

                    if nval['resources'].has_key?('aws_sqs_queue.queue')
                        SQS_ID = nval['resources']['aws_sqs_queue.queue']['primary']['id']
                        puts "SQS_ID #{SQS_ID}"
                        SQS_NAME = nval['resources']['aws_sqs_queue.queue']['primary']['attributes']['name']
                        puts "SQS_NAME #{SQS_NAME}"
                    end

                end
            end

        }
    end
}

ENV['AWS_REGION'] = 'us-east-1'


