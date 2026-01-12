from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.reading import router as reading_router
from routes.handwriting import router as handwriting_router
from routes.quiz import router as quiz_router  # Quiz + RL

app = FastAPI(title="NeuroAdaptive Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reading_router)
app.include_router(handwriting_router)
app.include_router(quiz_router)

@app.get("/health")
def health_check():
    return {"status": "Backend running"}
