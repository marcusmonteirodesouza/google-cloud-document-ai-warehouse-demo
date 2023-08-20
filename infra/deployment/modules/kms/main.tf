locals {
  kms_crypto_key_rotation_period = "7776000s" # 90 days

  doc_ai_keyring_location = var.doc_ai_region == "us" ? "us-central1" : "europe-west4" # See https://cloud.google.com/document-ai/docs/cmek#using_cmek
}

resource "google_kms_key_ring" "default_public" {
  name     = "public-keyring"
  location = var.region
}

resource "google_kms_crypto_key" "default_public" {
  name            = "public-key"
  key_ring        = google_kms_key_ring.default_public.id
  rotation_period = local.kms_crypto_key_rotation_period

  lifecycle {
    prevent_destroy = true
  }
}

resource "google_kms_key_ring" "defaut_internal" {
  name     = "internal-keyring"
  location = var.region
}

resource "google_kms_crypto_key" "defaut_internal" {
  name            = "internal-key"
  key_ring        = google_kms_key_ring.defaut_internal.id
  rotation_period = local.kms_crypto_key_rotation_period

  lifecycle {
    prevent_destroy = true
  }
}

resource "google_kms_key_ring" "default_restricted" {
  name     = "restricted-keyring"
  location = var.region
}

resource "google_kms_crypto_key" "default_restricted" {
  name            = "restricted-key"
  key_ring        = google_kms_key_ring.default_restricted.id
  rotation_period = local.kms_crypto_key_rotation_period

  lifecycle {
    prevent_destroy = true
  }
}

resource "google_kms_key_ring" "doc_ai_public" {
  name     = "public-doc-ai-keyring"
  location = local.doc_ai_keyring_location
}

resource "google_kms_crypto_key" "doc_ai_public" {
  name            = "public-key"
  key_ring        = google_kms_key_ring.doc_ai_public.id
  rotation_period = local.kms_crypto_key_rotation_period

  lifecycle {
    prevent_destroy = true
  }
}

