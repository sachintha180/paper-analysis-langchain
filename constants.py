from pathlib import Path
from typing import Dict

INPUT_DIR = Path("papers")

START_FROM = 1  # skip the cover page
MIN_PAGE_CHAR_COUNT = 50  # skip pages that have less than 50 chars

EXTRACTION_PROMPT_FP = Path("prompts/extractor.md")
EXTRACTION_MODEL = "openai:gpt-5.4-mini-2026-03-17"

ANALYSIS_HIGH_FREQ_THRESHOLD = 0.8
PAPER3_TOPICS: Dict[str, str] = {
    "13.1": "User-defined data types",
    "13.2": "File organisation and access",
    "13.3": "Floating-point numbers, representation and manipulation",
    "14.1": "Protocols",
    "14.2": "Circuit switching and packet switching",
    "15.1": "Processors, Parallel Processing and Virtual Machines",
    "15.2": "Boolean Algebra and Logic Circuits",
    "16.1": "Purposes of an Operating System",
    "16.2": "Translation Software",
    "17.1": "Encryption, Encryption Protocols and Digital Certificates",
    "18.1": "Artificial Intelligence",
    "19.1": "Algorithms",
    "19.2": "Recursion",
    "20.1": "Programming Paradigms",
    "20.2": "File Processing and Exception Handling",
}

EXPORTER_PROMPT_FP = Path("prompts/exporter.md")
SYNTHESIS_MODEL = "openai:gpt-5.5-2026-04-23"
OUTPUT_DIR = Path("output")
