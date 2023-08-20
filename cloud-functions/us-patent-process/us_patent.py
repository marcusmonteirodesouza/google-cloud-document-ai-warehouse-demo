from dataclasses import dataclass


@dataclass
class USPatent:
    applicant_line1: str | None
    application_number: int | None
    class_international: str | None
    class_us: str | None
    filing_date: str | None
    inventor_Line_1: str | None
    issuer: str | None
    patent_number: int | None
    publication_date: str | None
    title_line_1: str | None
