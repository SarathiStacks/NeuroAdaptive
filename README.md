
# 🧠 NeuroAdaptive
### AI-Powered Adaptive Learning Platform for Neurodiverse Students

**NeuroAdaptive** is an AI-driven personalized learning platform designed to support students with **Neurodevelopmental Disorders (NDDs)** such as **ADHD, Dyslexia, and Autism**.

The platform adapts learning content in real-time using **Machine Learning**, **Reinforcement Learning**, and **Azure Cognitive Services** to create an inclusive and engaging educational environment.

---

## 🚀 Features

### 📘 Reading Tutor
* **AI-Powered Lessons:** Personalized reading material adapted to user proficiency.
* **Text-to-Speech:** Utilizes **Azure Speech** to assist with auditory learning.
* **Comprehension Feedback:** Real-time analysis and feedback using **Azure OpenAI**.
* **Progress Tracking:** Monitors reading speed and accuracy over time.

### ✍️ Handwriting Helper
* **Digital OCR:** Upload images of handwritten text for analysis using **Azure Vision**.
* **Dyslexia Support:** Custom ML model specifically trained to estimate handwriting clarity.
* **Personalized Feedback:** actionable tips to improve letter formation and legibility.

### 🧠 ADHD Gamified Quiz
* **Adaptive Difficulty:** Questions adjust in real-time based on performance.
* **Reinforcement Learning:** Uses a **DQN-based agent** to optimize engagement and challenge levels.
* **Attention Estimation:** ML models analyze interaction patterns to gauge focus.
* **Gamification:** Earn points and badges to maintain motivation.

### 📊 Progress & Achievements
* **Unified Dashboard:** View stats across reading, writing, and quizzes.
* **State Management:** LocalStorage-based persistence for MVP.
* **Gamification:** Unlockable achievements and badges for milestones.

---

## 🏗️ Tech Stack

### Frontend
* **Framework:** React (Vite)
* **Styling:** Tailwind CSS
* **Icons:** Lucide React

### Backend
* **Framework:** FastAPI (Python)
* **ML Libraries:** TensorFlow / Keras, Scikit-learn
* **Services:**
    * Azure Speech (Text-to-Speech)
    * Azure Vision (OCR)
    * Azure OpenAI (Generative Feedback)
    * Azure Language (Sentiment/Analytics)

---

## 📁 Project Structure

```bash
NeuroAdaptive/
├── backend/
│   ├── app.py                      # Main FastAPI entry point
│   ├── routes/
│   │   ├── reading.py              # Reading tutor endpoints
│   │   ├── handwriting.py          # Handwriting analysis endpoints
│   │   ├── quiz.py                 # Quiz logic endpoints
│   ├── services/
│   │   ├── azure_speech.py         # Azure TTS integration
│   │   ├── azure_language.py       # Azure Language integration
│   │   ├── azure_openai_quiz.py    # OpenAI integration for quizzes
│   │   ├── handwriting_service.py  # Custom handwriting model logic
│   │   ├── adhd_service.py         # Attention estimation logic
│   │   ├── dqn_quiz_agent.py       # RL Agent for adaptive difficulty
│   ├── models/
│   │   ├── dyslexia_handwriting_cnn.h5
│   │   ├── attention_rf_model.pkl
│   │   ├── knowledge_tracing_lstm.h5
│   └── .env ❗ (Create this file manually)
│
├── frontend/
│   └── src/
│       ├── pages/
│       │   ├── Reader.jsx
│       │   ├── Handwriting.jsx
│       │   ├── Quiz.jsx
│       │   ├── Progress.jsx
│       │   ├── Achievements.jsx
│       ├── components/
│       ├── App.jsx
│
└── README.md

```

---

## 🔐 Environment Variables (REQUIRED)

### ⚠️ IMPORTANT

You **must create your own `.env` file** inside the `backend/` folder. This file is not included in the repository for security reasons.

**1. Create the file:**
`backend/.env`

**2. Add the following keys:**

```env
# Azure Speech Service
AZURE_SPEECH_KEY=your_speech_key_here
AZURE_SPEECH_REGION=your_region_here

# Azure Vision (OCR)
AZURE_VISION_KEY=your_vision_key_here
AZURE_VISION_ENDPOINT=[https://your-resource-name.cognitiveservices.azure.com/](https://your-resource-name.cognitiveservices.azure.com/)

# Azure Language Service
AZURE_LANGUAGE_KEY=your_language_key_here
AZURE_LANGUAGE_ENDPOINT=[https://your-resource-name.cognitiveservices.azure.com/](https://your-resource-name.cognitiveservices.azure.com/)

# Azure OpenAI
AZURE_OPENAI_KEY=your_openai_key_here
AZURE_OPENAI_ENDPOINT=[https://your-resource-name.openai.azure.com/](https://your-resource-name.openai.azure.com/)
AZURE_OPENAI_MODEL=gpt-4o-mini

```

---

## ▶️ Getting Started

### Prerequisites

* Python 3.9+
* Node.js & npm

### 1️⃣ Backend Setup

Navigate to the backend directory, set up the virtual environment, and install dependencies.

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app:app --reload

```

*The Backend will run at: `http://127.0.0.1:8000*`

### 2️⃣ Frontend Setup

Open a new terminal, navigate to the frontend directory, and install dependencies.

```bash
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev

```

*The Frontend will run at: `http://localhost:5173*`

---

## 🧪 MVP Notes & Limitations

* **Data Persistence:** Progress tracking currently uses `LocalStorage` for MVP simplicity. Clearing browser cache will reset progress.
* **Model Loading:** ML models are pre-trained and loaded into memory at backend startup.
* **OCR Accuracy:** Azure OCR accuracy may vary for severely dyslexic handwriting (this is expected behavior in the MVP phase).
* **RL Logic:** The Reinforcement Learning logic for the quiz is simplified for demonstration purposes.

---

## 🎯 Vision

NeuroAdaptive aims to become the standard adaptive learning platform for inclusive education by combining **AI**, **cognitive personalization**, and **human-centered design** to empower every student to learn in their own way.

---

## 📬 Contact
Srisha: kanna.srisha@gmail.com

Sarathi: sarathi16072006@gmail.com
