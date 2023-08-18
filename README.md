# Google Cloud Document AI Warehouse demo

## How it works

## Deployment

### Pre-Requisites

1. [Create a Google Cloud Organization](https://cloud.google.com/resource-manager/docs/creating-managing-organization).
1. [Create a project on your Organization](https://cloud.google.com/resource-manager/docs/creating-managing-projects).
1. Install the [gcloud CLI](https://cloud.google.com/sdk/docs/install).
1. Run [`gcloud auth login`](https://cloud.google.com/sdk/gcloud/reference/auth/login).
1. Run [`gcloud auth application-default login`](https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login).
1. Install [`terraform`](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli).

### Bootstrap

This process will:

- [Enable the required APIs](https://cloud.google.com/endpoints/docs/openapi/enable-api).
- [Create the Google Cloud Storage bucket](https://developer.hashicorp.com/terraform/language/settings/backends/gcs) that will contain the [terraform state](https://developer.hashicorp.com/terraform/language/state).
- Store the [`terraform.tfvars`](https://developer.hashicorp.com/terraform/language/values/variables#variable-definitions-tfvars-files) file content on [Secret Manager](https://cloud.google.com/secret-manager).
- Create the [service accounts](https://cloud.google.com/iam/docs/service-account-overview) that the system will use and give them their required [IAM permissions](https://cloud.google.com/iam/docs/overview#permissions).
- Create the [Cloud Build triggers](https://cloud.google.com/build/docs/automating-builds/create-manage-triggers) that will actually deploy the workloads.

You should perform this first. To do so:

1. [Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) this repository.
1. `cd` into the [./infra/deployment/terraform/bootstrap](./infra/deployment/terraform/bootstrap) folder.
1. Copy the `terraform.tfvars.template` file into a `terraform.tfvars` file.
1. Fill out the variables. You can leave these two empty for now:

   - `sourcerepo_name`
   - `sourcerepo_branch_name`

1. Comment out the entire contents of the `backend.tf` file.
1. Run `terraform init`.
1. Run `terraform apply -target=module.enable_apis` and type `yes`.
1. Create a [Cloud Source Repository](https://cloud.google.com/source-repositories/docs) by [mirroring your forked Github repository](https://cloud.google.com/source-repositories/docs/mirroring-a-github-repository).
1. Fill out the `sourcerepo_name` variable with the Cloud Source repository name.
1. Run `terraform apply` and type `yes`.
1. Uncomment the contents of the `backend.tf` file and set the `bucket` attribute to the value of the `tfstate_bucket` output.
1. Run `terraform init` and type `yes`.

### Apps

This process will deploy the actual applications and their supporting infra-structure. To run it:

1. Go to Cloud Build -> Triggers -> Click the "Run" button on the `apps` trigger row -> Click the "Run Trigger" button.
1. Go to Cloud Build -> History, and follow the build's progress.

### Train US Patent Parser Custom Document Extractor

The US Patent Parser is a Document AI [Custom Document Extractor](https://cloud.google.com/document-ai/docs/workbench/build-custom-processor). To train it, follow the steps below:

1. Go to Key Management -> take note of the location of the `doc-ai-key`.
1. Go to Cloud Storage -> click "Create" to [create a GCS bucket](https://cloud.google.com/storage/docs/creating-buckets) -> You can name it `<some random prefix>-us-patent-parser-v1-0-0-initial-data-import` -> For the location, select the same region as the `doc-ai-key` -> Click "Continue" until the "Choose how to protect object data" section -> open the "Data encryption" accordion, click "Customer-managed encryption key (CMEK)" and select the `doc-ai-key` as the encryption key -> click "Create". Now click "Upload Folder" and upload the [US patents labeled data folder](./data/documents/us/patents/labeled/).
1. Now go to Document AI -> My Processors -> Click the `us-patent-parser` processor -> Train.
1. Click "Show Advanced Options" -> Click "I'l specify my own location -> select the `<project_id>-us-patent-parser-dataset` bucket. Wait for the dataset configuration to finish.
1. Click the "Import Documents" button -> click "Browse" -> select the bucket you imported the US patents labeled data to and select the `labeled` folder -> In the "Data split" dropdown on the right, select `Auto-split` -> click "Import". Wait for the import to finish.
1. Click "Edit Schema", enable all the labels, set the labels according to the table below, and then click "Save":

   | Name                | Data type  | Occurrence    |
   | ------------------- | ---------- | ------------- |
   | applicant_line_1    | Plain Text | Required once |
   | application_number  | Number     | Required once |
   | class_international | Plain Text | Required once |
   | class_us            | Plain Text | Required once |
   | filing_date         | Datetime   | Required once |
   | inventor_line_1     | Plain text | Required once |
   | issuer              | Plain text | Required once |
   | patent_number       | Number     | Required once |
   | publication_date    | Datetime   | Required once |
   | title_line_1        | Plain text | Required once |

1. Go back to the "Train" tab, and click "Train New Version". You can name the version `v1-0-0`, and then click "Start Training". Wait for the training to finish: it can take more than 1 hour for it to finish.
1. Check the processor's [F1 score](https://cloud.google.com/document-ai/docs/workbench/evaluate#all-labels): it should show more than `0.9` for all labels.
1. Go to the Manage Versions tab -> click the three dots on the right of the model version -> click "Deploy version", and wait for it to finish. It can take more than 10 minutes for it to finish.
1. Click the three dots again and click "Set as default".
