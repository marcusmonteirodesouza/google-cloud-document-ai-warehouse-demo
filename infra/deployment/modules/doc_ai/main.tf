resource "google_document_ai_processor" "us_patent_parser" {
  location     = var.doc_ai_region
  display_name = "us-patent-parser"
  type         = "CUSTOM_EXTRACTION_PROCESSOR"
  kms_key_name = var.doc_ai_public_crypto_key_id
}

resource "google_storage_bucket" "us_passport_parser_dataset" {
  name     = "${var.project_id}-us-patent-parser-dataset"
  location = var.doc_ai_public_crypto_key_location

  uniform_bucket_level_access = true

  encryption {
    default_kms_key_name = var.doc_ai_public_crypto_key_id
  }

  versioning {
    enabled = true
  }
}