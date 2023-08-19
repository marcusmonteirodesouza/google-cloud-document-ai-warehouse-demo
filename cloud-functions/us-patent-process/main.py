import functions_framework
import logging
from dataclasses import asdict
from google.cloud import documentai
from us_patent_extractor import USPatentExtractor
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

        us_patent_extractor = USPatentExtractor(
            document_processor_service_client=document_processor_service_client,
            project_id=config.project_id,
            us_patent_processor_id=config.us_patent_processor_id,
            us_patent_processor_location=config.us_patent_processor_location,
        )

        us_patent = us_patent_extractor.extract_from_bytes(
            content=file_content, mime_type=file.content_type
        )

        return asdict(us_patent)
    except Exception as e:
        logging.exception(e, exc_info=True)
        return ErrorHandler.handle_error(e)
