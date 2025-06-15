# agent.py
"""Simple knowledge base loader and OpenRouter query interface."""

import os
import glob
import requests
from collections import defaultdict


def load_books(directory: str = "books") -> dict:
    """Load all .txt files from a directory into a dictionary."""
    knowledge = {}
    if not os.path.isdir(directory):
        return knowledge
    for path in glob.glob(os.path.join(directory, "*.txt")):
        with open(path, "r", encoding="utf-8") as f:
            knowledge[os.path.basename(path)] = f.read()
    return knowledge


def select_relevant_context(question: str, knowledge: dict) -> str:
    """Return the text from the book that best matches the question."""
    if not knowledge:
        return ""
    scores = defaultdict(int)
    words = set(question.lower().split())
    for name, text in knowledge.items():
        text_words = text.lower().split()
        overlap = words.intersection(text_words)
        scores[name] = len(overlap)
    best_doc = max(scores, key=scores.get)
    return knowledge[best_doc]


def query_openrouter(question: str, context: str) -> str:
    """Send a question and context to the OpenRouter API."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENROUTER_API_KEY is not set")

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You answer questions about provided context."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"},
        ],
    }
    response = requests.post(url, headers=headers, json=data, timeout=30)
    response.raise_for_status()
    result = response.json()
    try:
        return result["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        return str(result)


if __name__ == "__main__":
    kb = load_books()
    example_question = "Summarize the content of the first book."
    context = select_relevant_context(example_question, kb)
    try:
        answer = query_openrouter(example_question, context)
        print(answer)
    except Exception as e:
        print(f"Failed to query OpenRouter: {e}")

