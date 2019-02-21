locals {
  env = {
    defaults = {
      queue_name   = "${var.queue_name}"
    }

    kitchen-terraform-base-aws = {
      queue_name   = "${var.queue_name}"
    }
  }

  workspace   = "${merge(local.env["defaults"], local.env[terraform.workspace])}"
  queue_name  = "${local.workspace["queue_name"]}"
  role_name   = "${local.workspace["role_name"]}"


}
