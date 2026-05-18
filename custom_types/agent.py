import operator
from pathlib import Path
from pydantic import BaseModel
from typing import Annotated, TypedDict, Dict, List, Optional, Any

from custom_types.core import Paper, Question


class GraphState(TypedDict):
    pdf_paths: List[Path]
    papers: Annotated[List[Paper], operator.add]
    questions: Annotated[Dict[str, List[Question]], operator.or_]
    analysis: Optional[Dict[str, Any]]
    per_paper_md: Dict[str, str]


AgentOutput = Dict[str, Any]


class ExtractionResult(BaseModel):
    questions: List[Question]
