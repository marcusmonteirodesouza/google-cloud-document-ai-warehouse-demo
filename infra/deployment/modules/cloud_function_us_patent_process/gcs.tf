resource "google_storage_bucket" "input" {
  name                        = "${data.google_project.project.project_id}-us-patent-process-input"
  location                    = var.region
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  encryption {
    default_kms_key_name = var.default_internal_crypto_key_id
  }
}

resource "google_storage_bucket_iam_member" "input_pdf_hc_cloud_function_service_account" {
  bucket = google_storage_bucket.input.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${var.service_account}"
}