locals {
  roles = [
    "roles/pubsub.publisher"
  ]
}

data "google_storage_project_service_account" "gcs_sa" {
}

resource "google_project_iam_member" "gcs_sa" {
  for_each = toset(local.roles)
  project  = data.google_project.project.project_id
  role     = each.value
  member   = "serviceAccount:${data.google_storage_project_service_account.gcs_sa.email_address}"
}

resource "google_kms_crypto_key_iam_member" "gcs_sa_default_internal" {
  crypto_key_id = var.default_internal_crypto_key_id
  role          = "roles/cloudkms.cryptoKeyEncrypterDecrypter"
  member        = "serviceAccount:${data.google_storage_project_service_account.gcs_sa.email_address}"
}

resource "google_kms_crypto_key_iam_member" "gcs_sa_default_restricted" {
  crypto_key_id = var.default_restricted_crypto_key_id
  role          = "roles/cloudkms.cryptoKeyEncrypterDecrypter"
  member        = "serviceAccount:${data.google_storage_project_service_account.gcs_sa.email_address}"
}

resource "google_kms_crypto_key_iam_member" "gcs_sa_doc_ai_public" {
  crypto_key_id = var.doc_ai_public_crypto_key_id
  role          = "roles/cloudkms.cryptoKeyEncrypterDecrypter"
  member        = "serviceAccount:${data.google_storage_project_service_account.gcs_sa.email_address}"
}