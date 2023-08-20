import functions_framework
import logging
from google.cloud import documentai, contentwarehouse
from us_patent_extractor import USPatentExtractor
from us_patent_document_ai_warehouse_uploader import USPatentDocumentAIWarehouseUploader
from errors import MethodNotAllowedError
from error_handler import ErrorHandler
from config import config


@functions_framework.http
def process_us_patent(request):
    try:
        if request.method != "POST":
            raise MethodNotAllowedError("HTTP request method must be 'POST'")

        if "file" not in request.files:
            raise ValueError("No file part")

        file = request.files["file"]

        if file.filename == "":
            raise ValueError("No selected file")

        file_content = file.read()

        document_processor_service_client = documentai.DocumentProcessorServiceClient()

        document_service_client = contentwarehouse.DocumentServiceClient()

        us_patent_extractor = USPatentExtractor(
            document_processor_service_client=document_processor_service_client,
            project_id=config.project_id,
            us_patent_processor_id=config.us_patent_processor_id,
            us_patent_processor_location=config.us_patent_processor_location,
        )

        us_patent_document_ai_warehouse_uploader = USPatentDocumentAIWarehouseUploader(
            document_service_client=document_service_client,
            project_number=config.project_number,
            document_ai_warehouse_region=config.doc_ai_warehouse_region,
            document_ai_warehouse_user_id=config.doc_ai_warehouse_user_id,
            us_patent_document_schema_id=config.us_patent_document_schema_id,
        )

        us_patent = us_patent_extractor.extract_from_bytes(
            content=file_content, mime_type=file.content_type
        )

        us_patent_document_ai_warehouse_uploader.upload(
            content=file_content, mime_type=file.content_type, us_patent=us_patent
        )

        return {}, 201
    except Exception as e:
        logging.exception(e, exc_info=True)
        return ErrorHandler.handle_error(e)
