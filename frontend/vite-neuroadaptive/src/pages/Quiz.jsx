import { useEffect, useState } from "react";
import Layout from "../components/Layout";

export default function Quiz() {
  const [topic, setTopic] = useState("Neural Networks");
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState([]);
  const [timeTaken, setTimeTaken] = useState([]);
  const [startTimes, setStartTimes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [difficulty, setDifficulty] = useState(null);
  const [stats, setStats] = useState(null);
  const [error, setError] = useState("");

  // ---------- Generate Quiz ----------
  const generateQuiz = async () => {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/quiz/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic }),
      });

      const data = await res.json();

      setQuestions(data.questions);
      setDifficulty(data.difficulty);
      setStats(data.stats);
      setAnswers(new Array(data.questions.length).fill(null));
      setTimeTaken(new Array(data.questions.length).fill(0));
      setStartTimes(data.questions.map(() => Date.now()));
    } catch {
      setError("Failed to generate quiz. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // ---------- Select Answer ----------
  const selectAnswer = (qIndex, optionIndex) => {
    const now = Date.now();
    const timeSpent = Math.round((now - startTimes[qIndex]) / 1000);

    const newAnswers = [...answers];
    const newTimes = [...timeTaken];

    newAnswers[qIndex] = optionIndex;
    newTimes[qIndex] = timeSpent;

    setAnswers(newAnswers);
    setTimeTaken(newTimes);
  };

  // ---------- Submit Quiz ----------
  const submitQuiz = async () => {
    setSubmitting(true);
    setError("");

    try {
      const res = await fetch("http://127.0.0.1:8000/quiz/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          answers,
          time_taken: timeTaken,
        }),
      });

      const data = await res.json();
      setResult(data);
      setStats(data.stats);
    } catch {
      setError("Quiz submission failed. Please retry.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Layout>
      <div className="max-w-5xl mx-auto p-6 space-y-6">

        {/* ---------- Header ---------- */}
        <div className="rounded-2xl p-6 bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-xl">
          <h1 className="text-3xl font-bold">NeuroAdaptive Quiz</h1>
          <p className="opacity-90 mt-1">
            AI-driven • ADHD-friendly • Gamified Learning
          </p>
        </div>

        {/* ---------- Topic Input ---------- */}
        <div className="flex gap-4">
          <input
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            className="flex-1 px-4 py-3 rounded-xl border shadow-sm"
            placeholder="Enter learning topic"
          />
          <button
            onClick={generateQuiz}
            className="px-6 py-3 rounded-xl bg-indigo-600 text-white font-semibold hover:bg-indigo-700"
          >
            Generate Quiz
          </button>
        </div>

        {/* ---------- Loading ---------- */}
        {loading && (
          <div className="text-center text-indigo-600 font-semibold animate-pulse">
            Generating personalized quiz…
          </div>
        )}

        {/* ---------- Error ---------- */}
        {error && (
          <div className="p-4 bg-red-100 text-red-700 rounded-xl">
            {error}
          </div>
        )}

        {/* ---------- Stats ---------- */}
        {stats && (
          <div className="grid grid-cols-3 gap-4">
            <Stat label="Level" value={stats.level} />
            <Stat label="XP" value={stats.xp} />
            <Stat label="Streak" value={stats.streak} />
          </div>
        )}

        {/* ---------- Difficulty ---------- */}
        {difficulty && (
          <div className="text-center text-sm text-gray-600">
            Current Difficulty:{" "}
            <span className="font-semibold capitalize">{difficulty}</span>
          </div>
        )}

        {/* ---------- Questions ---------- */}
        {questions.map((q, qi) => (
          <div
            key={qi}
            className="p-6 bg-white rounded-2xl shadow-md space-y-4"
          >
            <h3 className="font-semibold text-lg">
              {qi + 1}. {q.question}
            </h3>

            <div className="grid grid-cols-2 gap-3">
              {q.options.map((opt, oi) => (
                <button
                  key={oi}
                  onClick={() => selectAnswer(qi, oi)}
                  className={`px-4 py-3 rounded-xl border text-left transition
                    ${
                      answers[qi] === oi
                        ? "bg-indigo-600 text-white"
                        : "hover:bg-gray-100"
                    }`}
                >
                  {opt}
                </button>
              ))}
            </div>
          </div>
        ))}

        {/* ---------- Submit ---------- */}
        {questions.length > 0 && (
          <button
            onClick={submitQuiz}
            disabled={submitting}
            className="w-full py-4 rounded-2xl bg-green-600 text-white font-bold text-lg hover:bg-green-700"
          >
            {submitting ? "Submitting…" : "Submit Quiz"}
          </button>
        )}

        {/* ---------- Results ---------- */}
        {result && (
          <div className="space-y-6 mt-6">

            <div className="p-6 bg-gradient-to-r from-green-500 to-emerald-500 text-white rounded-2xl shadow-xl">
              <h2 className="text-2xl font-bold">
                Score: {result.score}%
              </h2>
              <p className="mt-2">{result.quiz_feedback}</p>
            </div>

            <InfoCard title="Attention Feedback">
              {result.attention_feedback}
            </InfoCard>

            <InfoCard title="Knowledge Mastery">
              Mastery Score: {(result.mastery_score * 100).toFixed(1)}%
            </InfoCard>

            {result.explanations?.length > 0 && (
              <div className="space-y-4">
                <h3 className="font-bold text-xl">Review Mistakes</h3>

                {result.explanations.map((e, i) => (
                  <div
                    key={i}
                    className="p-4 border-l-4 border-red-500 bg-red-50 rounded-xl"
                  >
                    <p className="font-semibold">{e.question}</p>
                    <p className="text-sm text-red-700">
                      Your Answer: {e.user_answer}
                    </p>
                    <p className="text-sm text-green-700">
                      Correct Answer: {e.correct_answer}
                    </p>
                    <p className="mt-2 text-gray-700">{e.reason}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </Layout>
  );
}

// ---------- UI Components ----------
function Stat({ label, value }) {
  return (
    <div className="p-4 bg-white rounded-xl shadow text-center">
      <p className="text-gray-500 text-sm">{label}</p>
      <p className="text-xl font-bold">{value}</p>
    </div>
  );
}

function InfoCard({ title, children }) {
  return (
    <div className="p-5 bg-white rounded-xl shadow">
      <h3 className="font-semibold mb-2">{title}</h3>
      <p className="text-gray-700">{children}</p>
    </div>
  );
}
