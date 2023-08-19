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