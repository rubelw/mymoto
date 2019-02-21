terraform {
  required_version = ">= 0.11.7"
}

resource "aws_sqs_queue" "queue" {
  name  = "test_queue"
}
