"""
analyzer.py
Send ONE review to the local Ollama decision model (4 questions, 1 request)
and turn the answers into star ratings per topic.
"""

import requests
from questions import TOPICS, QUESTIONS, STARS

URL = "http://localhost:11434/v1/systemone"
MODEL = "tev1:0.8b"


def analyze_review(review_text):
    """Return a dict like {"Camera": 4.0, "Battery": 2.0}.
    Topics the review doesn't talk about are left out."""

    try:
        resp = requests.post(
            URL,
            json={"model": MODEL, "state": review_text, "questions": QUESTIONS},
            timeout=120,
        )
        resp.raise_for_status()
        answers = resp.json()["answers"]
    except (requests.RequestException, KeyError, ValueError) as e:
        detail = getattr(getattr(e, "response", None), "text", "")
        print(f"  ! analysis failed: {e} {detail}")
        return {}

    ratings = {}
    for topic_name, topic_id in TOPICS.items():
        choice = answers.get(topic_id, {}).get("choice")
        if choice in STARS:
            ratings[topic_name] = STARS[choice]
    return ratings