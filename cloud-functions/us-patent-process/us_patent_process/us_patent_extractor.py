from google.cloud import documentai, storage
from .us_patent import USPatent


class USPatentExtractor:
    def __init__(
        self,
        storage_client: storage.Client,
        document_processor_service_async_client: documentai.DocumentProcessorServiceAsyncClient,
        project_id: str,
        us_patent_processor_id: str,
        us_patent_processor_location: str,
    ):
        self._storage_client = storage_client
        self._document_processor_service_async_client = (
            document_processor_service_async_client
        )
        self._project_id = project_id
        self._us_patent_processor_id = us_patent_processor_id
        self._us_patent_processor_location = us_patent_processor_location

    async def extract_from_gcs_document(
        self, bucket_name: str, blob_name: str
    ) -> USPatent:
        bucket = self._storage_client.get_bucket(bucket_or_name=bucket_name)
        blob = bucket.get_blob(blob_name=blob_name)

        gcs_document = documentai.GcsDocument()
        gcs_document.gcs_uri = f"gs://{bucket_name}/{blob_name}"
        gcs_document.mime_type = blob.content_type

        name = f"projects/{self._project_id}/locations/{self._us_patent_processor_location}/processors/{self._us_patent_processor_location}"

        process_document_request = documentai.ProcessRequest(
            gcs_document=gcs_document, name=name
        )

        process_document_response = (
            await self._document_processor_service_async_client.process_document(
                request=process_document_request
            )
        )

        entities = process_document_response.document.entities

        application_line_1_entity = next(
            entity for entity in entities if entity.type_ == "applicant_line_1"
        )
        application_number_entity = next(
            entity for entity in entities if entity.type_ == "application_number"
        )
        class_international_entity = next(
            entity for entity in entities if entity.type_ == "class_international"
        )
        class_us_entity = next(
            entity for entity in entities if entity.type_ == "class_us"
        )
        filing_date_entity = next(
            entity for entity in entities if entity.type_ == "filing_date"
        )
        inventor_line_1_entity = next(
            entity for entity in entities if entity.type_ == "inventor_line_1"
        )
        issuer_entity = next(entity for entity in entities if entity.type_ == "issuer")
        patent_number_entity = next(
            entity for entity in entities if entity.type_ == "patent_number"
        )
        publication_date_entity = next(
            entity for entity in entities if entity.type_ == "publication_date"
        )
        title_line_1_entity = next(
            entity for entity in entities if entity.type_ == "title_line_1"
        )

        application_line1 = application_line_1_entity.mention_text
        application_number = application_number_entity.normalized_value.text
        class_international = class_international_entity.mention_text
        class_us = class_us_entity.mention_text
        filing_date = filing_date_entity.normalized_value.date_value
        inventor_line_1 = inventor_line_1_entity.mention_text
        issuer = issuer_entity.mention_text
        patent_number = patent_number_entity.normalized_value.text
        publication_date = publication_date_entity.normalized_value.date_value
        title_line_1_entity = title_line_1_entity.mention_text

        return USPatent(
            application_line1,
            application_number,
            class_international,
            class_us,
            filing_date,
            inventor_line_1,
            issuer,
            patent_number,
            publication_date,
            title_line_1_entity,
        )
