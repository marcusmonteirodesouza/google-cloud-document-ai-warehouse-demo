import functions_framework
from cloudevents.http import CloudEvent
from google.cloud import documentai, storage
from .us_patent_extractor import USPatentExtractor
from .config import config


@functions_framework.cloud_event
async def process_us_patent(cloud_event: CloudEvent):
    data = cloud_event.data

    bucket_name = data["bucket"]
    blob_name = data["name"]

    storage_client = storage.Client()

    document_processor_service_async_client = (
        documentai.DocumentProcessorServiceAsyncClient()
    )

    us_patent_extractor = USPatentExtractor(
        storage_client=storage_client,
        document_processor_service_async_client=document_processor_service_async_client,
        project_id=config._project_id,
        us_patent_processor_id=config._us_patent_processor_id,
        us_patent_processor_location=config._us_patent_processor_location,
    )

    us_patent = await us_patent_extractor.extract_from_gcs_document(
        bucket_name=bucket_name, blob_name=blob_name
    )

    print(us_patent)
