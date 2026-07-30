"""
Run this once from your project root to scaffold the Career Bot project.
Usage: python setup_structure.py
"""

import os

STARTER_CONTENT = {
    ".gitignore": (
        "venv/\n"
        "__pycache__/\n"
        "*.pyc\n"
        ".env\n"
        "*.log\n"
    ),
    ".env": "# API keys go here — never commit this file\nGROQ_API_KEY=\nADZUNA_APP_ID=\nADZUNA_APP_KEY=\n",
    "config.yaml": (
        "llm:\n"
        "  model_name: \"llama-3.3-70b-versatile\"\n"
        "  temperature: 0.2\n\n"
        "adzuna:\n"
        "  country: \"in\"\n"
        "  results_per_page: 20\n"
    ),
    "README.md": "# Career Bot\n\nTakes a natural-language job request, extracts search criteria, "
                 "queries Adzuna, and recommends genuinely matching listings with links.\n",
    "requirements.txt": (
        "groq\n"
        "langchain-groq\n"
        "requests\n"
        "python-dotenv\n"
        "pyyaml\n"
        "pydantic\n"
    ),
}

FILES = [
    "main.py",          # entry point — takes user input, runs the full flow
    "extractor.py",      # LLM step: parses free-text request into structured keywords/role/location
    "adzuna_client.py",  # the actual API call to Adzuna
    "matcher.py",        # LLM step: judges relevance of each fetched job against the request
    "config.yaml",
    ".env",
    ".gitignore",
    "requirements.txt",
    "README.md",
]


def create_file(path: str):
    if os.path.exists(path):
        print(f"  skip (exists): {path}")
        return
    content = STARTER_CONTENT.get(path, "")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  created: {path}")


def main():
    print("Scaffolding Career Bot project...\n")
    for fname in FILES:
        create_file(fname)
    print("\nDone.")


if __name__ == "__main__":
    main()