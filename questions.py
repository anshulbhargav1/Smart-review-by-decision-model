"""
questions.py
Topics and the 4 choice questions sent to the decision model.
"""

# Topic name shown to users -> short id used as the question key
TOPICS = {
    "Camera": "camera",
    "Battery": "battery",
    "Display": "display",
    "Performance": "performance",
}

TOPIC_HINTS = {
    "camera": "the camera (photos or videos)",
    "battery": "battery life or charging",
    "display": "the screen",
    "performance": "speed, responsiveness, multitasking, or gaming",
}

# option key -> description shown to the model
CRITERIA = {
    "not_mentioned": "The reviewer does not mention this topic",
    "very_dissatisfied": "Very dissatisfied",
    "dissatisfied": "Dissatisfied",
    "neutral": "Neither satisfied nor dissatisfied, or balanced mixed feedback",
    "satisfied": "Satisfied",
    "very_satisfied": "Very satisfied",
}

# option key -> stars (not_mentioned is absent, so it gets skipped)
STARS = {
    "very_dissatisfied": 1.0,
    "dissatisfied": 2.0,
    "neutral": 3.0,
    "satisfied": 4.0,
    "very_satisfied": 5.0,
}

QUESTIONS = {
    topic_id: {
        "type": "choice",
        "instructions": f"How satisfied is the reviewer with {TOPIC_HINTS[topic_id]}?",
        "criteria": CRITERIA,
    }
    for topic_id in TOPICS.values()
}