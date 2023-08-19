variable "default_public_crypto_key_id" {
  type        = string
  description = " The default public KMS crypto keys ID."
}

variable "default_internal_crypto_key_id" {
  type        = string
  description = "The default internal KMS crypto keys ID."
}

variable "default_restricted_crypto_key_id" {
  type        = string
  description = "The default restricted KMS crypto keys ID."
}

variable "doc_ai_public_crypto_key_id" {
  type        = string
  description = " The Document AI public KMS crypto keys ID."
}