import os
from dataclasses import dataclass


@dataclass
class _Config:
    project_id = os.environ["PROJECT_ID"]
    project_number = os.environ["PROJECT_NUMBER"]
    us_patent_processor_id = os.environ["US_PATENT_PROCESSOR_ID"]
    us_patent_processor_location = os.environ["US_PATENT_PROCESSOR_LOCATION"]
    doc_ai_warehouse_region = os.environ["DOC_AI_WAREHOUSE_REGION"]
    doc_ai_warehouse_user_id = os.environ["DOC_AI_WAREHOUSE_USER_ID"]
    us_patent_document_schema_id = os.environ["US_PATENT_DOCUMENT_SCHEMA_ID"]


config = _Config()
