locals {
  doc_ai_warehouse_ui_sa_roles = [
    "roles/contentwarehouse.documentCreator",
  ]
}

resource "google_project_iam_member" "doc_ai_warehouse_ui_sa" {
  for_each = toset(local.doc_ai_warehouse_ui_sa_roles)
  project  = data.google_project.project.project_id
  role     = each.value
  member   = "serviceAccount:${var.doc_ai_warehouse_ui_sa}"
}