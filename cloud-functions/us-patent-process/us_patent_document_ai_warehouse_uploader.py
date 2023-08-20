from google.cloud import contentwarehouse
from us_patent import USPatent


class USPatentDocumentAIWarehouseUploader:
    def __init__(
        self,
        document_service_client: contentwarehouse.DocumentServiceClient,
        project_number: str,
        document_ai_warehouse_region: str,
        document_ai_warehouse_user_id: str,
        us_patent_document_schema_id: str,
    ):
        self._document_service_client = document_service_client
        self._project_number = project_number
        self._document_ai_warehouse_region = document_ai_warehouse_region
        self._document_ai_warehouse_user_id = document_ai_warehouse_user_id
        self._us_patent_document_schema_id = us_patent_document_schema_id

    def upload(self, content: bytes, mime_type: str, us_patent: USPatent):
        applicant_line1 = contentwarehouse.Property(
            name="applicant_line1",
            text_values=contentwarehouse.TextArray(values=[us_patent.applicant_line1]),
        )

        application_number = contentwarehouse.Property(
            name="application_number",
            text_values=contentwarehouse.TextArray(
                values=[str(us_patent.application_number)]
            ),
        )

        class_international = contentwarehouse.Property(
            name="class_international",
            text_values=contentwarehouse.TextArray(
                values=[us_patent.class_international]
            ),
        )

        class_us = contentwarehouse.Property(
            name="class_us",
            text_values=contentwarehouse.TextArray(values=[us_patent.class_us]),
        )

        filing_date = contentwarehouse.Property(
            name="filing_date",
            text_values=contentwarehouse.TextArray(values=[us_patent.filing_date]),
        )

        inventor_Line_1 = contentwarehouse.Property(
            name="inventor_Line_1",
            text_values=contentwarehouse.TextArray(values=[us_patent.inventor_Line_1]),
        )

        issuer = contentwarehouse.Property(
            name="issuer",
            text_values=contentwarehouse.TextArray(values=[us_patent.issuer]),
        )

        patent_number = contentwarehouse.Property(
            name="patent_number",
            text_values=contentwarehouse.TextArray(
                values=[str(us_patent.patent_number)]
            ),
        )

        publication_date = contentwarehouse.Property(
            name="publication_date",
            text_values=contentwarehouse.TextArray(values=[us_patent.publication_date]),
        )

        title_line_1 = contentwarehouse.Property(
            name="title_line_1",
            text_values=contentwarehouse.TextArray(values=[us_patent.title_line_1]),
        )

        document = contentwarehouse.Document(
            reference_id=str(us_patent.patent_number),
            display_name=f"{us_patent.patent_number}{self._get_file_extension(mime_type=mime_type)}",
            title=f"{us_patent.title_line_1} - {us_patent.applicant_line1} - {us_patent.inventor_Line_1}",
            document_schema_name=f"projects/{self._project_number}/locations/{self._document_ai_warehouse_region}/documentSchemas/{ self._us_patent_document_schema_id}",
            inline_raw_document=content,
            raw_document_file_type=self._get_raw_document_file_type(
                mime_type=mime_type
            ),
            properties=[
                applicant_line1,
                application_number,
                class_international,
                class_us,
                filing_date,
                inventor_Line_1,
                issuer,
                patent_number,
                publication_date,
                title_line_1,
            ],
        )

        parent = self._document_service_client.common_location_path(
            project=self._project_number, location=self._document_ai_warehouse_region
        )

        create_document_request = contentwarehouse.CreateDocumentRequest(
            parent=parent,
            document=document,
            request_metadata=contentwarehouse.RequestMetadata(
                user_info=contentwarehouse.UserInfo(
                    id=f"user:{self._document_ai_warehouse_user_id}"
                )
            ),
        )

        self._document_service_client.create_document(request=create_document_request)

    def _get_raw_document_file_type(self, mime_type: str):
        match mime_type:
            case "application/pdf":
                return contentwarehouse.RawDocumentFileType.RAW_DOCUMENT_FILE_TYPE_PDF
            case _:
                raise ValueError(
                    f'Unexpected mime_type {mime_type}. Valid mime_types: "application/pdf"'
                )

    def _get_file_extension(self, mime_type: str):
        match mime_type:
            case "application/pdf":
                return ".pdf"
            case _:
                raise ValueError(
                    f'Unexpected mime_type {mime_type}. Valid mime_types: "application/pdf"'
                )
