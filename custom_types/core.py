from pydantic import BaseModel
from typing import TypedDict, Literal, List

Session = Literal["mj", "on"]


class PDFMetadata(TypedDict):
    year: int
    session: Session
    paper_code: int
    region_code: int


class Paper(TypedDict):
    name: str
    metadata: PDFMetadata
    pages_text: List[str]
    empty_pages: int


# NOTE: See prompts/extractor.md for more information about the following attributes
class Question(BaseModel):
    number: str
    marks: int
    topic_code: str
    topic_name: str
    command_word: str
    raw_text: str
