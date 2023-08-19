locals {
  cloud_function_zip_path = "${path.module}/cloud-function-us-patent-process.zip"
}

data "google_project" "project" {
}

resource "google_storage_bucket" "cloud_function_code" {
  name                        = "${data.google_project.project.project_id}-cloud-function-us-patent-process-code"
  location                    = var.region
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  encryption {
    default_kms_key_name = var.default_internal_crypto_key_id
  }
}

data "archive_file" "cloud_function_code" {
  type        = "zip"
  source_dir  = "${path.module}/../../../../cloud-functions/us-patent-process"
  output_path = local.cloud_function_zip_path
}

resource "google_storage_bucket_object" "cloud_function_code" {
  name   = "cloud-function-us-patent-process.${filemd5(data.archive_file.cloud_function_code.output_path)}.zip"
  bucket = google_storage_bucket.cloud_function_code.name
  source = local.cloud_function_zip_path
}

resource "google_cloudfunctions2_function" "us_patent_process" {
  name        = "us-patent-process"
  location    = var.region
  description = "Process US Patent file uploads"

  build_config {
    runtime     = "python311"
    entry_point = "process_us_patent"

    source {
      storage_source {
        bucket = google_storage_bucket.cloud_function_code.name
        object = google_storage_bucket_object.cloud_function_code.name
      }
    }
  }

  service_config {
    service_account_email = var.service_account

    environment_variables = {
      PROJECT_ID                   = data.google_project.project.project_id
      US_PATENT_PROCESSOR_ID       = var.us_patent_parser_processor_id
      US_PATENT_PROCESSOR_LOCATION = var.us_patent_parser_processor_location
    }
  }
}