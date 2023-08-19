import datetime
import string
from google.cloud import documentai
from us_patent import USPatent


class USPatentExtractor:
    def __init__(
        self,
        document_processor_service_client: documentai.DocumentProcessorServiceClient,
        project_id: str,
        us_patent_processor_id: str,
        us_patent_processor_location: str,
    ):
        self._document_processor_service_client = document_processor_service_client
        self._project_id = project_id
        self._us_patent_processor_id = us_patent_processor_id
        self._us_patent_processor_location = us_patent_processor_location

    def extract_from_bytes(self, content: bytes, mime_type: str) -> USPatent:
        raw_document = documentai.RawDocument()
        raw_document.content = content
        raw_document.mime_type = mime_type

        name = f"projects/{self._project_id}/locations/{self._us_patent_processor_location}/processors/{self._us_patent_processor_id}"

        process_document_request = documentai.ProcessRequest(
            raw_document=raw_document, name=name
        )

        process_document_response = (
            self._document_processor_service_client.process_document(
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

        application_number = (
            application_number_entity.normalized_value.text
            or application_number_entity.mention_text
        )
        if application_number:
            application_number = int(
                application_number.translate(str.maketrans("", "", string.punctuation))
            )

        class_international = class_international_entity.mention_text
        class_us = class_us_entity.mention_text
        filing_date = datetime.date(
            year=filing_date_entity.normalized_value.date_value.year,
            month=filing_date_entity.normalized_value.date_value.month,
            day=filing_date_entity.normalized_value.date_value.day,
        ).isoformat()
        inventor_line_1 = inventor_line_1_entity.mention_text
        issuer = issuer_entity.mention_text

        patent_number = (
            patent_number_entity.normalized_value.text
            or application_number_entity.mention_text
        )
        if patent_number:
            patent_number = int(
                patent_number.translate(str.maketrans("", "", string.punctuation))
            )

        publication_date = datetime.date(
            year=publication_date_entity.normalized_value.date_value.year,
            month=publication_date_entity.normalized_value.date_value.month,
            day=publication_date_entity.normalized_value.date_value.day,
        ).isoformat()
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
