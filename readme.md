Aurvia Threshold Checker — Screening Assignment
A unified full-stack application built with FastAPI (backend) and React (frontend).  
The entire app runs from a single command — no separate frontend dev server needed.
---
Project Structure
```
aurvia-screening-app/
├── app.py              # FastAPI backend + static file mount
├── templates/
│   └── index.html      # React frontend (rendered in-browser via Babel CDN)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```
---
Setup & Run Instructions
1. Prerequisites
Make sure you have Python 3.10+ installed.  
Check with:
```bash
python --version
```
2. Clone / Download the Project
```bash
git clone https://github.com/YOUR_USERNAME/aurvia-screening-app.git
cd aurvia-screening-app
```
3. Create a Virtual Environment (Recommended)
```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```
4. Install Dependencies
```bash
pip install -r requirements.txt
```
5. Run the Application
```bash
uvicorn app:app --reload
```
6. Open in Browser
Visit: http://localhost:8000
That's it — the full app (UI + API) runs on a single port. ✅
---
How It Works
Backend (`app.py`)
Built with FastAPI
POST /api/threshold — Accepts JSON:
```json
  { "stream_values": [10, 15, 22, 19, 8], "max_variance": 5 }
  ```
Calculates the mean of `stream_values`
If any value deviates from the mean by more than `max_variance` → returns `"CRITICAL"`
Otherwise → returns `"STABLE"`
Returns 400 Bad Request if values are empty or contain non-numbers
Static Mount — The `/templates` folder is mounted at `/`, so `index.html` is served at the root URL.
Frontend (`templates/index.html`)
Built with React 18 (loaded via CDN — no build step required)
User enters comma-separated stream values and a max variance number
Clicks "Check Metrics" → fires a `fetch()` POST to `/api/threshold`
Shows a green STABLE badge or a red CRITICAL badge based on the response
Button is disabled while a request is in-flight (prevents double-clicks)
Errors (empty input, non-numbers, server issues) are shown gracefully
---
API Reference
`POST /api/threshold`
Request Body:
```json
{
  "stream_values": [10, 15, 22, 19, 8],
  "max_variance": 5.0
}
```
Success Response (200):
```json
{
  "mean": 14.8,
  "status": "STABLE",
  "max_variance": 5.0,
  "count": 5
}
```
Error Response (400):
```json
{
  "error": "Bad Request",
  "detail": "stream_values must be a non-empty list of numbers, and max_variance must be a number."
}
```
---
Example Test Cases
Input Values	Max Variance	Mean	Result
10, 15, 22, 19, 8	5	14.8	CRITICAL (22 is 7.2 away)
10, 12, 11, 10, 11	5	10.8	STABLE
(empty)	5	—	400 Error
---
Tech Stack
Layer	Technology
Backend	Python, FastAPI, Uvicorn, Pydantic
Frontend	React 18 (CDN), Babel (CDN)
Served	Single port via FastAPI StaticFiles
