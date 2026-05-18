import logging
from typing import cast

from langchain.chat_models import init_chat_model
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)
from utils import load_extraction_prompt
from constants import EXTRACTION_MODEL

from custom_types.core import Paper
from custom_types.agent import ExtractionResult, AgentOutput

model = init_chat_model(EXTRACTION_MODEL, temperature=0)
structured_model = model.with_structured_output(ExtractionResult)
logger = logging.getLogger(__name__)


def extract(state: Paper) -> AgentOutput:
    paper_name = state["name"]

    logger.info("Extracting questions from %s", paper_name)
    result = cast(
        ExtractionResult,
        structured_model.invoke(
            [
                SystemMessage(content=load_extraction_prompt()),
                HumanMessage(content="\n\n".join(state["pages_text"])),
            ]
        ),
    )
    logger.info("Extracted %d questions from %s", len(result.questions), paper_name)
    return {"questions": {paper_name: result.questions}}
