output "default_public_crypto_key_id" {
  value = google_kms_crypto_key.default_public.id
}

output "default_internal_crypto_key_id" {
  value = google_kms_crypto_key.defaut_internal.id
}

output "default_restricted_crypto_key_id" {
  value = google_kms_crypto_key.default_restricted.id
}

output "doc_ai_public_crypto_key_id" {
  value = google_kms_crypto_key.doc_ai_public.id
}

output "doc_ai_public_crypto_key_id_location" {
  value = google_kms_key_ring.doc_ai_public.location
}

