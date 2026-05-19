import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

from dotenv import load_dotenv

# Load environment variables before the remaining imports
load_dotenv(".env.local")

from typing import List
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Send

from agents.injest import injest
from agents.extract import extract
from agents.analyze import analyse
from agents.export import export

from custom_types.agent import GraphState

from constants import INPUT_DIR, OUTPUT_DIR


def route_to_extract(state: GraphState) -> List[Send]:
    return [Send("extract", paper) for paper in state["papers"]]


def build_graph() -> CompiledStateGraph:
    builder = StateGraph(GraphState)

    builder.add_node("injest", injest)
    builder.add_node("extract", extract)
    builder.add_node("analyse", analyse)
    builder.add_node("export", export)

    builder.add_edge(START, "injest")
    builder.add_conditional_edges("injest", route_to_extract, ["extract"])
    builder.add_edge("extract", "analyse")
    builder.add_edge("analyse", "export")
    builder.add_edge("export", END)

    return builder.compile()


pdf_paths = sorted(INPUT_DIR.glob("*.pdf"))
if not pdf_paths:
    logging.info("No paper PDFs found in %s", INPUT_DIR)
else:
    logging.info("Found %d papers to process", len(pdf_paths))
    graph = build_graph()

    with open(OUTPUT_DIR / "graph.png", "wb") as f:
        f.write(graph.get_graph(xray=True).draw_mermaid_png())

    graph.invoke({"pdf_paths": pdf_paths})
