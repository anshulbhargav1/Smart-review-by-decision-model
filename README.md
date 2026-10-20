# Smartphone Review Analyzer

Turns free-text smartphone reviews into Flipkart-style per-topic star ratings using a **local decision model** (`tev1:0.8b`) served by **Ollama**. No API key and no cloud calls.

For every review, the model is asked 4 multiple-choice questions, one per topic:

- Each question is a `choice` question: *"How satisfied is the reviewer with <topic>?"*
- The model picks one option: **not mentioned**, **very dissatisfied**, **dissatisfied**, **neutral**, **satisfied**, or **very satisfied**
- Options map to whole stars (1-5). "Not mentioned" is skipped, so the topic doesn't count for that review
- Ratings are then averaged across all reviews

**Topics:** Camera, Battery, Display, Performance

## How it works

`tev1:0.8b` is a decision model: its only capability is `decision`, so `ollama.chat` and `ollama.generate` do not work with it. It is reached through Ollama's `/v1/systemone` endpoint (Ollama 0.35 or later), which takes a `state` (the review text) and a set of named questions, and returns an answer per question.

All 4 questions for a review are sent in a single request.

## Project structure

| File | Purpose |
|---|---|
| `main.py` | Reads the CSV, analyzes each review, prints the summary |
| `analyzer.py` | Sends one review to Ollama's `/v1/systemone` and converts answers into star ratings |
| `questions.py` | Topic list, answer options, option-to-star mapping, and the 4 questions |
| `aggregation.py` | Averages per-review ratings into one score per topic |
| `synthetic_phone_reviews.csv` | 50 synthetic sample reviews |

## Setup

**1. Install Ollama** (version 0.35 or later; `tev1:0.8b` itself requires 0.40.0) from [ollama.com](https://ollama.com).

**2. Download the model:**

```bash
ollama pull tev1:0.8b
```

**3. Install the Python dependency:**

```bash
pip install requests
```

A virtual environment is recommended:

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install requests
```

## Usage

Make sure Ollama is running (the desktop app, or `ollama serve` in another terminal). Quick check:

```bash
curl http://localhost:11434
```

It should print `Ollama is running`. Then, from the project folder:

```bash
python main.py
```

Example output:

```
R001 {'Camera': 5.0, 'Battery': 4.0, 'Performance': 4.0}
R002 {'Battery': 2.0}
...

3.2 ★  based on 50 ratings
----------------------------------------
Camera           3.8 ★  (21 reviews)
Battery          2.9 ★  (24 reviews)
Display          3.5 ★  (18 reviews)
Performance      3.6 ★  (22 reviews)
```

The headline rating (`3.2 ★`) is the average of the reviewers' own `overall_rating` column, not the model's output. The per-topic lines come from the model.

## Input format

The CSV must have these columns:

| Column | Description |
|---|---|
| `review_id` | Unique review ID |
| `phone_model` | Phone name |
| `overall_rating` | Integer 1-5 star rating given by the reviewer |
| `review_text` | The review body |
| `is_synthetic` | Whether the review was generated |

## Configuration

| What | Where |
|---|---|
| Model name | `MODEL` in `analyzer.py` (must match `ollama list`) |
| Ollama address | `URL` in `analyzer.py` (default `http://localhost:11434/v1/systemone`) |
| Topics and question wording | `TOPICS`, `TOPIC_HINTS` in `questions.py` |
| Answer options and star mapping | `CRITERIA`, `STARS` in `questions.py` |

To add a topic, add it to both `TOPICS` and `TOPIC_HINTS`. The question and the aggregation pick it up automatically.

## Troubleshooting

| Problem | Fix |
|---|---|
| `does not support chat` / `does not support generate` | Don't use `ollama.chat` or `ollama.generate` with this model. Use `/v1/systemone` as `analyzer.py` does |
| `Connection refused` | Ollama isn't running. Start the app or run `ollama serve` |
| `model "tev1:0.8b" not found` | Run `ollama pull tev1:0.8b`, and check `MODEL` matches `ollama list` |
| `404` on `/v1/systemone` | Ollama is older than 0.35. Update it |
| `FileNotFoundError` for the CSV | Run `python main.py` from the project folder |
| `! analysis failed: ...` on some reviews | That review is skipped and the run continues. The server's error message is printed next to it |

## Notes

- Ratings are whole stars (1-5), so per-topic averages are the only fractional values.
- `tev1:0.8b` is a small experimental model, so expect some wrong ratings on reviews with mixed opinions.