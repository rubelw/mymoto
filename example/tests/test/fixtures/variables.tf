# Required

variable "queue_name" {
  description = "The human readable name of the queue"
}



# Optional

variable "visibility_timeout_seconds" {
  description = "The visibility timeout for the queue in seconds. Default is 30"
  default     = 30
}

variable "message_retention_seconds" {
  description = "The message retention for the queue in secons. Default is 60"
  default     = 60
}

variable "max_message_size" {
  description = "The maximum size of message for the queue.  default is 262144 bytes"
  default     = 262144
}

variable "delay_seconds" {
  description = "the delay for all messages in the queue in seconds default is 0"
  default     = 0
}

variable "receive_wait_time_seconds" {
  description = "the wait time for a receive message call in seconds. default is 0"
  default     = 0
}

variable "fifo_queue" {
  description = "FIFO queue? default is false"
  default     = "false"
}

variable "kms_data_key_reuse_period_seconds" {
  description = "length of time in seconds sqs can reuse a data key to encrypt of decrypt message default is 300"
  default     = 300
}

variable "tags" {
  type    = "map"
  default = {}
}

variable "redrive_policy" {
  description = "Redrive policy for queue"
  default     = ""
}
