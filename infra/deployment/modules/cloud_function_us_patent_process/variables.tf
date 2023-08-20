variable "region" {
  type        = string
  description = "The default Google Cloud region for the created resources."
}

variable "service_account" {
  type        = string
  description = "The us-patent-process Cloud Function service account."
}

variable "default_internal_crypto_key_id" {
  type        = string
  description = "The default internal KMS crypto keys ID."
}

variable "us_patent_parser_processor_id" {
  type        = string
  description = "The US Patent Parser Document AI processor ID."
}

variable "us_patent_parser_processor_location" {
  type        = string
  description = "The US Patent Parser Document AI processor location."
}

variable "doc_ai_warehouse_region" {
  type        = string
  description = "The region in which the Document AI Warehouse was provisioned."
}

variable "doc_ai_warehouse_ui_sa" {
  type        = string
  description = "The Document AI Warehouse UI service account email address."
}

variable "us_patent_document_schema_id" {
  type        = string
  description = "The US Patent Document AI Warehouse schema ID."
}