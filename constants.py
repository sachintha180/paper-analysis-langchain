from pathlib import Path
from typing import Dict

PAPER_PREFIX = input("Enter your paper prefix (paper3/paper4): ")
INPUT_DIR = Path("papers") / PAPER_PREFIX

START_FROM = 1  # skip the cover page
MIN_PAGE_CHAR_COUNT = 50  # skip pages that have less than 50 chars

EXTRACTION_PROMPT_FP = Path(f"prompts/{PAPER_PREFIX}_extractor.md")
EXTRACTION_MODEL = "openai:gpt-5.4-mini-2026-03-17"

ANALYSIS_HIGH_FREQ_THRESHOLD = 0.8

# NOTE: The TOPICS keys must match the PAPER_PREFIX that is entered, other KeyError
TOPICS: Dict[str, Dict[str, str]] = {
    "paper3": {
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
    },
    "paper4": {
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
    },
}

EXPORTER_PROMPT_FP = Path(f"prompts/{PAPER_PREFIX}_exporter.md")
SYNTHESIS_MODEL = "openai:gpt-5.5-2026-04-23"
OUTPUT_DIR = Path("output") / PAPER_PREFIX
