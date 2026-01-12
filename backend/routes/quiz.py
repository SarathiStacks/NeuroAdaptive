from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from services.azure_openai_quiz import generate_quiz, generate_explanations
from services.dqn_quiz_agent import DQNQuizAgent
from services.adhd_service import get_attention_feedback
from services.knowledge_service import predict_mastery

router = APIRouter(prefix="/quiz", tags=["Quiz"])

agent = DQNQuizAgent()

LAST_QUESTIONS = []
CURRENT_DIFFICULTY = None
ATTENTION_TIMELINE = []
MASTERY_HISTORY = []

class QuizGenerateRequest(BaseModel):
    topic: str


class QuizSubmitRequest(BaseModel):
    answers: List[int]
    time_taken: List[float]

@router.post("/generate")
def generate(req: QuizGenerateRequest):
    global LAST_QUESTIONS, CURRENT_DIFFICULTY

    difficulty = agent.choose_difficulty()
    CURRENT_DIFFICULTY = difficulty

    LAST_QUESTIONS = generate_quiz(req.topic, difficulty)

    return {
        "difficulty": difficulty,
        "level": agent.get_level(),
        "questions": LAST_QUESTIONS
    }

@router.post("/submit")
def submit(req: QuizSubmitRequest):
    global LAST_QUESTIONS, CURRENT_DIFFICULTY
    global ATTENTION_TIMELINE, MASTERY_HISTORY

    if not LAST_QUESTIONS:
        return {
            "error": "No active quiz found. Please generate a quiz first."
        }

    if len(req.answers) != len(LAST_QUESTIONS):
        return {
            "error": "Answer count does not match quiz questions."
        }

    if len(req.time_taken) != len(LAST_QUESTIONS):
        return {
            "error": "Time data missing or incomplete."
        }

    correct = 0
    wrong = []
    correctness_seq = []

    for i, q in enumerate(LAST_QUESTIONS):
        if req.answers[i] == q["answer"]:
            correct += 1
            correctness_seq.append(1)
        else:
            correctness_seq.append(0)
            wrong.append({
                "question": q["question"],
                "options": q["options"],
                "correct_answer": q["options"][q["answer"]],
                "user_answer": q["options"][req.answers[i]]
            })

    total = len(LAST_QUESTIONS)
    score = correct / total if total > 0 else 0.0

    if score >= 0.8:
        reward = 1.0
    elif score >= 0.5:
        reward = 0.5
    else:
        reward = -0.3

    agent.update(reward, CURRENT_DIFFICULTY)

    attention_score, attention_msg = get_attention_feedback(
        req.time_taken,
        correctness_seq
    )
    ATTENTION_TIMELINE.append(attention_score)

    mastery = predict_mastery(correctness_seq)
    MASTERY_HISTORY.append(mastery)

    explanations = generate_explanations(wrong) if wrong else []

    LAST_QUESTIONS.clear()
    CURRENT_DIFFICULTY = None

    return {
        "score": round(score * 100, 2),
        "correct": correct,
        "total": total,
        "level": agent.get_level(),
        "quiz_feedback": agent.get_reward_feedback(),
        "attention_feedback": attention_msg,
        "attention_score": round(attention_score, 3),
        "attention_timeline": ATTENTION_TIMELINE,
        "mastery_score": round(mastery, 3),
        "mastery_history": MASTERY_HISTORY,
        "wrong_answers": wrong,
        "explanations": explanations
    }
