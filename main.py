from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Configure CORS to allow communication from your frontend
origins = [
    "http://127.0.0.1:5500",  # VS Code Live Server default
    "http://localhost:5500",
    "http://127.0.0.1:8000",  # If frontend is served from FastAPI itself, or a different port
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScoreEntry(BaseModel):
    name: str
    score: int

# In-memory storage for scores. In a real application, this would be a database.
_scores: List[ScoreEntry] = []

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Snake Game Backend!"}

@app.post("/scores", response_model=ScoreEntry)
async def submit_score(score_entry: ScoreEntry):
    """
    Submits a new score to the high score list.
    """
    if not score_entry.name or not score_entry.score >= 0:
        raise HTTPException(status_code=400, detail="Invalid score data.")
    _scores.append(score_entry)
    _scores.sort(key=lambda x: x.score, reverse=True) # Sort scores highest first
    # Optionally limit the number of stored scores
    global _scores
    _scores = _scores[:10] # Keep top 10 scores
    return score_entry

@app.get("/scores", response_model=List[ScoreEntry])
async def get_high_scores():
    """
    Retrieves the sorted list of high scores.
    """
    return _scores

# To run this backend:
# 1. Make sure you have uvicorn installed: pip install uvicorn fastapi
# 2. Run from your terminal: uvicorn main:app --reload
# The server will typically run on http://127.0.0.1:8000