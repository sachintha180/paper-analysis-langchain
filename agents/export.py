import json
import logging

from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

from constants import SYNTHESIS_MODEL, OUTPUT_DIR

from custom_types.agent import GraphState, AgentOutput
from utils import load_exporter_prompt, build_user_prompt

model = init_chat_model(SYNTHESIS_MODEL, temperature=0)
logger = logging.getLogger(__name__)


def export(state: GraphState) -> AgentOutput:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "per_paper").mkdir(exist_ok=True)

    logger.info("Exporting results for %d papers", len(state["per_paper_md"]))
    for paper_name, md in state["per_paper_md"].items():
        logger.debug("Writing per paper file for %s", paper_name)
        (OUTPUT_DIR / "per_paper" / f"{paper_name}.md").write_text(md, encoding="utf-8")

    logger.info("Writing analysis JSON to %s", OUTPUT_DIR)
    (OUTPUT_DIR / "analysis.json").write_text(
        json.dumps(state["analysis"], indent=2), encoding="utf-8"
    )

    logger.info("Generating final analysis markdown")
    final_md = model.invoke(
        [
            SystemMessage(content=load_exporter_prompt()),
            HumanMessage(content=build_user_prompt(state)),
        ]
    ).content
    logger.info("Writing final analysis to %s", OUTPUT_DIR)
    (OUTPUT_DIR / "final_analysis.md").write_text(str(final_md), encoding="utf-8")

    return {}
