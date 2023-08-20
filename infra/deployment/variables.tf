variable "project_id" {
  type        = string
  description = "The project ID."
}

variable "region" {
  type        = string
  description = "The default Google Cloud region for the created resources."
}

variable "doc_ai_region" {
  type        = string
  description = "The default Google Cloud region for the Document AI resources."

  validation {
    condition     = var.doc_ai_region == "us" || var.doc_ai_region == "eu"
    error_message = "The doc_ai_region value must be \"us\" or \"eu\"."
  }
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