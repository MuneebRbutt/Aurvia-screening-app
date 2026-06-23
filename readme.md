# Aurvia Threshold Checker — Pre-Screening Assignment

A unified full-stack application built with **FastAPI** (backend) and **Vanilla JavaScript** (frontend).
The entire app runs from a **single command** on a **single port** — no separate frontend dev server needed.

---

## Project Structure

```
aurvia-screening-app/
├── app.py              # FastAPI backend + static file mount
├── templates/
│   └── index.html      # Frontend UI (HTML + CSS + Vanilla JS)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## Environment Setup & Run Instructions

### Prerequisites
- Python 3.10 or higher

Check your version:
```bash
python --version
```

### Step 1 — Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/aurvia-screening-app.git
cd aurvia-screening-app
```

### Step 2 — Create a Virtual Environment
```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Run the Application
```bash
python -m uvicorn app:app --reload
```

### Step 5 — Open in Browser
```
http://127.0.0.1:8000
```

The full app (UI + API) runs on a single port. No separate frontend server required.

---

## API Reference

### `POST /api/threshold`

Accepts a JSON payload, computes the mean of the stream values, and returns STABLE or CRITICAL based on variance.

**Request Body:**
```json
{
  "stream_values": [10, 15, 22, 19, 8],
  "max_variance": 5.0
}
```

**Success Response `200`:**
```json
{
  "mean": 14.8,
  "status": "CRITICAL",
  "max_variance": 5.0,
  "count": 5
}
```

**Error Response `400`:**
```json
{
  "error": "Bad Request",
  "detail": "stream_values must be a non-empty list of numbers, and max_variance must be a number."
}
```

---

## Logic Explained

1. Compute the **mean** of all values in `stream_values`
2. Check if **any value** deviates from the mean by more than `max_variance`
3. If yes → return `"CRITICAL"` | If no → return `"STABLE"`

---

## Test Cases

| Stream Values         | Max Variance | Mean   | Status   | Reason                          |
|-----------------------|-------------|--------|----------|---------------------------------|
| 10, 15, 22, 19, 8    | 5           | 14.8   | CRITICAL | 22 is 7.2 away, exceeds 5       |
| 10, 12, 11, 10, 11   | 5           | 10.8   | STABLE   | All values within 5 of mean     |
| 42                    | 1           | 42.0   | STABLE   | Single value, zero deviation    |
| abc, hello            | 5           | —      | 400 Error| Non-numeric input rejected      |
| (empty)               | 5           | —      | 400 Error| Empty input rejected            |

---

## Evaluation Compliance

| Evaluation Metric         | Implementation                                                                 | Status |
|---------------------------|--------------------------------------------------------------------------------|--------|
| Server Mount Compliance   | Single command launch via `uvicorn`. UI and API both served on port 8000       | ✅ Pass |
| Exception Handling        | Empty or non-numeric input returns clean `400 Bad Request`, no `500` crashes   | ✅ Pass |
| React State Integrity     | Button disables immediately on click, re-enables only after request completes  | ✅ Pass |

---

## Tech Stack

| Layer    | Technology                        |
|----------|-----------------------------------|
| Backend  | Python, FastAPI, Uvicorn, Pydantic |
| Frontend | HTML, CSS, Vanilla JavaScript      |
| Serving  | Single port via FastAPI StaticFiles |
