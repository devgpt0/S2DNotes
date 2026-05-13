# Project 09: Quiz Runner with Scoreboard

## Estimated Time
4 to 6 hours

## Goal
Create a terminal quiz app with multiple quizzes, scoring, and leaderboard.

## Functional Requirements
- Load quiz questions from JSON.
- Ask each question with options.
- Track user answers and score.
- Show result summary:
  - total score
  - correct/incorrect
  - wrong question review
- Maintain scoreboard file:
  - player name
  - score
  - timestamp
- Show top N scores.

## Non-Functional Requirements
- Invalid option input must be handled.
- Questions should be shuffled (optional simple random).

## Concepts Practiced
- `list` of questions
- `dict` for question/score records
- sorting lists of dicts
- file I/O with JSON

## HLD
- `quiz_loader.py`: load question bank
- `engine.py`: run quiz loop
- `scoring.py`: evaluate result
- `scoreboard.py`: save and rank scores
- `main.py`: menu and flow

## LLD
- `load_questions(path) -> list[dict]`
- `run_quiz(questions, player_name) -> dict`
- `evaluate(questions, answers) -> dict`
- `save_score(path, score_item) -> None`
- `load_scores(path) -> list[dict]`
- `top_scores(scores, n=10) -> list[dict]`

Question structure:
```python
{
  "id": 1,
  "question": "...",
  "options": ["A", "B", "C", "D"],
  "answer": 2
}
```

## Passing Criteria
- Quiz runs end-to-end without crash.
- Score math is correct.
- Scoreboard persists across runs.
- Top 5 ranking sorted descending.

## Implementation Roadmap
1. Create question format and loader.
2. Build input/answer loop.
3. Build scoring logic.
4. Build scoreboard persistence.
5. Add review screen for wrong answers.

## Optional Extensions
- Timed quiz mode.
- Category-wise quizzes.
