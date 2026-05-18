import logging
from typing import Dict

from utils import build_per_paper_md
from constants import PAPER3_TOPICS, ANALYSIS_HIGH_FREQ_THRESHOLD

from custom_types.agent import AgentOutput, GraphState

logger = logging.getLogger(__name__)


def analyse(state: GraphState) -> AgentOutput:
    questions_by_paper = state["questions"]
    logger.info("Analysing questions across %d papers", len(questions_by_paper))
    papers_by_name = {p["name"]: p for p in state["papers"]}

    topic_stats = {
        code: {"total_questions": 0, "total_marks": 0, "papers_appeared_in": 0}
        for code in PAPER3_TOPICS
    }
    marks_per_paper: Dict[str, int] = {}
    command_word_counts: Dict[str, int] = {}
    per_paper_md: Dict[str, str] = {}

    for paper_name, questions in questions_by_paper.items():
        marks_per_paper[paper_name] = sum(q.marks for q in questions)

        if paper_name in papers_by_name:
            per_paper_md[paper_name] = build_per_paper_md(
                papers_by_name[paper_name], questions
            )

        topics_in_paper: set[str] = set()
        for q in questions:
            code = q.topic_code
            command_word = q.command_word

            if code in topic_stats:
                topic_stats[code]["total_questions"] += 1
                topic_stats[code]["total_marks"] += q.marks
                topics_in_paper.add(code)

            command_word_counts[command_word] = (
                command_word_counts.get(command_word, 0) + 1
            )

        for code in topics_in_paper:
            topic_stats[code]["papers_appeared_in"] += 1

    total_papers = len(questions_by_paper)

    analysis = {
        "topic_stats": topic_stats,
        "marks_per_paper": marks_per_paper,
        "command_word_counts": command_word_counts,
        "never_appeared": [
            c for c, s in topic_stats.items() if s["papers_appeared_in"] == 0
        ],
        "high_frequency": [
            c
            for c, s in topic_stats.items()
            if s["papers_appeared_in"] >= ANALYSIS_HIGH_FREQ_THRESHOLD * total_papers
        ],
    }

    logger.info(
        "Analysis complete, found %d high frequency topics and %d topics that never appeared",
        len(analysis["high_frequency"]),
        len(analysis["never_appeared"]),
    )
    return {"analysis": analysis, "per_paper_md": per_paper_md}
