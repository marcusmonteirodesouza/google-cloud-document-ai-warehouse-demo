locals {
  cloud_functions_sa = "service-${data.google_project.project.number}@gcf-admin-robot.iam.gserviceaccount.com"
}

resource "null_resource" "cloud_functions_sa" {
  provisioner "local-exec" {
    command = "gcloud beta services identity create --service \"cloudfunctions.googleapis.com\" --project ${data.google_project.project.project_id}"
  }
}

resource "google_kms_crypto_key_iam_member" "cloud_functions_sa_default_internal" {
  crypto_key_id = var.default_internal_crypto_key_id
  role          = "roles/cloudkms.cryptoKeyEncrypterDecrypter"
  member        = "serviceAccount:${local.cloud_functions_sa}"

  depends_on = [
    null_resource.cloud_functions_sa
  ]
}