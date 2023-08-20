provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}

module "enable_apis" {
  source = "./modules/enable_apis"
}

module "kms" {
  source = "./modules/kms"

  region        = var.region
  doc_ai_region = var.doc_ai_region

  depends_on = [
    module.enable_apis
  ]
}

module "iam" {
  source = "./modules/iam"

  default_public_crypto_key_id     = module.kms.default_public_crypto_key_id
  default_internal_crypto_key_id   = module.kms.default_internal_crypto_key_id
  default_restricted_crypto_key_id = module.kms.default_restricted_crypto_key_id
  doc_ai_public_crypto_key_id      = module.kms.doc_ai_public_crypto_key_id
  doc_ai_warehouse_ui_sa           = var.doc_ai_warehouse_ui_sa
}

module "doc_ai" {
  source = "./modules/doc_ai"

  project_id                        = var.project_id
  doc_ai_region                     = var.doc_ai_region
  doc_ai_public_crypto_key_id       = module.kms.doc_ai_public_crypto_key_id
  doc_ai_public_crypto_key_location = module.kms.doc_ai_public_crypto_key_id_location

  depends_on = [module.iam]
}

module "cloud_function_us_patent_process" {
  source = "./modules/cloud_function_us_patent_process"

  region                              = var.region
  service_account                     = module.iam.cloud_function_us_patent_process_sa
  default_internal_crypto_key_id      = module.kms.default_internal_crypto_key_id
  us_patent_parser_processor_id       = module.doc_ai.us_patent_parser_processor_id
  us_patent_parser_processor_location = module.doc_ai.us_patent_parser_processor_location
  doc_ai_warehouse_region             = var.doc_ai_warehouse_region
  doc_ai_warehouse_ui_sa              = var.doc_ai_warehouse_ui_sa
  us_patent_document_schema_id        = var.us_patent_document_schema_id
}