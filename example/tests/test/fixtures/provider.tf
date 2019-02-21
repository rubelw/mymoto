
provider "aws" {
    region = "us-east-1"
    skip_credentials_validation = true
    skip_metadata_api_check     = true
    s3_force_path_style         = true
    skip_requesting_account_id = true
    skip_get_ec2_platforms = true
    access_key                  = "mock_access_key"
    secret_key                  = "mock_secret_key"
    endpoints {
        cloudformation = "http://localhost:5001"
        cloudwatch = "http://localhost:5002"
        ec2 = "http://localhost:5003"
        cloudwatchevents = "http://localhost:5004"
        iam = "http://localhost:5005"
        kms = "http://localhost:5006"
        lambda = "http://localhost:5007"
        s3 = "http://localhost:5008"
        #ses = "http://localhost:5009"
        sns = "http://localhost:5010"
        sqs = "http://localhost:5011"
        #sts = "http://localhost:5012"
        cloudwatchlogs = "http://localhost:5013"
    }
}