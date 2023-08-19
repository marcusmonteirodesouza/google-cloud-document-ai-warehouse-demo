output "cloud_function_us_patent_process_input_bucket" {
  value = module.cloud_function_us_patent_process.input_bucket
}

output "terraform_tfvars_secret_id" {
  value = google_secret_manager_secret.terraform_tfvars.id
}

output "tfstate_bucket" {
  value = google_storage_bucket.tfstate.name
}