resource "google_service_account" "cloud_function_us_patent_process" {
  account_id   = "cf-us-patent-process-sa"
  display_name = "us-patent-process Cloud Function Service Account"
}

resource "google_project_iam_custom_role" "cloud_function_us_patent_process" {
  role_id     = "cloudFunctionUSPatentProcessCF"
  title       = "us-patent-process Cloud Function custom role"
  description = "Contains the permissions necessary to run the us-patent-process Cloud Function"
  permissions = [
    "appengine.applications.get",
    "compute.backendServices.get",
    "contentwarehouse.documentSchemas.get",
    "contentwarehouse.documentSchemas.list",
    "contentwarehouse.documents.create",
    "documentai.humanReviewConfigs.review",
    "documentai.operations.getLegacy",
    "documentai.processorVersions.processBatch",
    "documentai.processorVersions.processOnline",
    "documentai.processors.processBatch",
    "documentai.processors.processOnline",
    "eventarc.events.receiveEvent",
    "resourcemanager.projects.get",
  ]
}

resource "google_project_iam_member" "cloud_function_us_patent_process_sa" {
  project = data.google_project.project.project_id
  role    = google_project_iam_custom_role.cloud_function_us_patent_process.name
  member  = "serviceAccount:${google_service_account.cloud_function_us_patent_process.email}"
}
