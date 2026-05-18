import logging
import pymupdf
from pathlib import Path
from typing import List

from custom_types.core import Paper
from custom_types.agent import GraphState, AgentOutput

from utils import get_paper_metadata
from constants import START_FROM, MIN_PAGE_CHAR_COUNT

logger = logging.getLogger(__name__)


def read_paper(pdf_path: Path) -> Paper:
    logger.info("Reading paper %s", pdf_path.name)
    try:
        paper = pymupdf.open(pdf_path)
    except:
        raise Exception(f"Cannot open paper at filepath: {pdf_path}")

    paper_metadata = get_paper_metadata(pdf_path.name)
    pages_text = []
    empty_pages = 0

    for page in paper.pages(START_FROM):
        # NOTE: page.number is 0-indexed
        raw_text = page.get_text().strip()
        if len(raw_text) < MIN_PAGE_CHAR_COUNT:
            logger.debug(
                "Skipping page %d in %s, only %d of %d characters",
                page.number + 1, pdf_path.name, len(raw_text), MIN_PAGE_CHAR_COUNT,
            )
            empty_pages += 1
            continue

        text = f"[PAGE {page.number + 1}]\n{raw_text}"
        pages_text.append(text)

    paper.close()

    return {
        "name": pdf_path.stem,
        "metadata": paper_metadata,
        "pages_text": pages_text,
        "empty_pages": empty_pages,
    }


def injest(state: GraphState) -> AgentOutput:
    papers: List[Paper] = []
    for pdf_path in state["pdf_paths"]:
        try:
            papers.append(read_paper(pdf_path))
        except:
            logger.error("Failed to read paper %s", pdf_path)

    logger.info("Injest complete, loaded %d papers", len(papers))
    return {"papers": papers}
