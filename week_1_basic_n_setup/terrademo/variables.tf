variable "project" {
  description = "Project"
  default     = "terraform-demo-454505"
}

variable "credentials" {
  description = "My Credentials"
  default     = "./keys/my-creds.json"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}

variable "bq_dataset_name" {
  description = "My Big Query Dataset name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "terraform-demo-454505-terra-bucket"
}

variable "gcs_storage_class" {
  description = "My Storage Bucket Name"
  default     = "STANDARD"
}