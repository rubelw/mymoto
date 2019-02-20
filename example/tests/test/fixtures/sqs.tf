terraform {
  required_version = ">= 0.11.7"
}

resource "aws_sqs_queue" "queue" {
  name                              = "${var.queue_name}"
  delay_seconds                     = "${var.delay_seconds}"
  max_message_size                  = "${var.max_message_size}"
  message_retention_seconds         = "${var.message_retention_seconds}"
  receive_wait_time_seconds         = "${var.receive_wait_time_seconds}"
  fifo_queue                        = "${var.fifo_queue}"
  visibility_timeout_seconds        = "${var.visibility_timeout_seconds}"
  redrive_policy                    = "${var.redrive_policy}"
  tags                              = "${merge(map("Name", "${var.queue_name}"), var.tags)}"
}
