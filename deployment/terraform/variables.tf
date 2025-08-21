variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
  default     = "hr-assistant-cluster"
}

variable "node_group_name" {
  description = "EKS node group name"
  type        = string
  default     = "hr-assistant-nodes"
}

variable "instance_type" {
  description = "EC2 instance type for nodes"
  type        = string
  default     = "t3.medium"
}