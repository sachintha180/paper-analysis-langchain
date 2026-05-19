import json
from typing import cast, List

from constants import EXTRACTION_PROMPT_FP, TOPICS, EXPORTER_PROMPT_FP

from custom_types.agent import GraphState
from custom_types.core import Question, Session, PDFMetadata, Paper


def get_paper_metadata(pdf_fname: str) -> PDFMetadata:
    try:
        year_str, session_str, prefixed_code_str, _ = pdf_fname.split("-")
    except:
        raise ValueError(f"Invalid pdf_fname, not enough values to unpack: {pdf_fname}")

    try:
        code_str = prefixed_code_str.split("paper")[-1]
        paper_code, region_code = int(code_str[0]), int(code_str[1])
    except:
        raise ValueError(
            f"Invalid prefixed_code_str, cannot extract paper_code and region_code: {prefixed_code_str}"
        )

    return {
        "year": int(year_str),
        "session": cast(Session, session_str),
        "paper_code": paper_code,
        "region_code": region_code,
    }


def load_extraction_prompt() -> str:
    return EXTRACTION_PROMPT_FP.read_text(encoding="utf-8")


def build_per_paper_md(paper: Paper, questions: List[Question]) -> str:
    meta = paper["metadata"]
    session_label = "May/June" if meta["session"] == "mj" else "Oct/Nov"
    header = f"# {meta['year']} {session_label} - Paper {meta['paper_code']}{meta['region_code']}\n\n"

    rows = ""
    for q in questions:
        text = q.raw_text.replace("|", "\\|")
        rows += f"| {q.number} | {q.marks} | {q.topic_code} | {q.topic_name} | {q.command_word} | {text} |\n"

    table = (
        "| Question | Marks | Topic Code | Topic Name | Command Word | Text |\n"
        "|---|---|---|---|---|---|\n" + rows
    )

    total = sum(q.marks for q in questions)
    return header + table + f"\n**Total marks extracted: {total} / 75**\n"


def build_user_prompt(state: GraphState) -> str:
    per_paper_section = "\n\n---\n\n".join(state["per_paper_md"].values())
    return (
        f"## Statistical Analysis\n\n"
        f"```json\n{json.dumps(state['analysis'], indent=2)}\n```\n\n"
        f"## Topic Reference\n\n"
        f"{json.dumps(TOPICS, indent=2)}\n\n"
        f"## Per-Paper Question Extracts\n\n"
        f"{per_paper_section}"
    )


def load_exporter_prompt() -> str:
    return EXPORTER_PROMPT_FP.read_text(encoding="utf-8")
