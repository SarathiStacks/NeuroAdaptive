from fastapi import APIRouter
from fastapi.responses import Response
from pydantic import BaseModel
from services.azure_speech import text_to_speech
from services.azure_language import check_understanding

router = APIRouter(prefix="/reading", tags=["Reading Tutor"])

class TextRequest(BaseModel):
    text: str

@router.get("/content")
def get_reading_content():
    return {
        "title": "The Curious Octopus",
        "passage": (
            "Octopuses are intelligent sea animals. "
            "They have eight arms and can solve simple problems. "
            "They use their arms to explore their surroundings and protect themselves."
        ),
        "tips": [
            "Read slowly",
            "Listen to the audio if needed",
            "Focus on the main idea"
        ]
    }

@router.post("/audio")
def play_audio(data: TextRequest):
    audio = text_to_speech(data.text)
    return Response(content=audio, media_type="audio/wav")

@router.post("/understanding")
def understanding(data: TextRequest):
    feedback = check_understanding(data.text)
    return {"feedback": feedback}
