locals {
  doc_ai_sa = "service-${data.google_project.project.number}@gcp-sa-prod-dai-core.iam.gserviceaccount.com"
}

resource "null_resource" "doc_ai_sa" {
  provisioner "local-exec" {
    command = "gcloud beta services identity create --service \"documentai.googleapis.com\" --project ${data.google_project.project.project_id}"
  }
}

resource "google_kms_crypto_key_iam_member" "doc_ai_sa_doc_ai_public" {
  crypto_key_id = var.doc_ai_public_crypto_key_id
  role          = "roles/cloudkms.cryptoKeyEncrypterDecrypter"
  member        = "serviceAccount:${local.doc_ai_sa}"

  depends_on = [
    null_resource.doc_ai_sa
  ]
}