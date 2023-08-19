import os
from dataclasses import dataclass


@dataclass
class _Config:
    project_id = os.environ["PROJECT_ID"]
    us_patent_processor_id = os.environ["US_PATENT_PROCESSOR_ID"]
    us_patent_processor_location = os.environ["US_PATENT_PROCESSOR_LOCATION"]


config = _Config()
