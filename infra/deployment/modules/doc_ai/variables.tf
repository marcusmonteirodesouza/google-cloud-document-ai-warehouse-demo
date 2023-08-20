variable "project_id" {
  type        = string
  description = "The project ID."
}

variable "doc_ai_region" {
  type        = string
  description = "The default Google Cloud region for the Document AI resources."
}

variable "doc_ai_public_crypto_key_id" {
  type        = string
  description = " The Document AI public KMS crypto keys ID."
}

variable "doc_ai_public_crypto_key_location" {
  type        = string
  description = " The Document AI public KMS crypto keys location."
}