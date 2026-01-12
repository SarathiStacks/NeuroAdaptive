import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import LessonBox from "../components/LessonBox";
import { Volume2, Brain, CheckCircle } from "lucide-react";

export default function Reader() {
  const [content, setContent] = useState(null);
  const [feedback, setFeedback] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/reading/content")
      .then((res) => res.json())
      .then((data) => {
        setContent(data);
        setLoading(false);
      });
  }, []);

  const playAudio = async () => {
    const res = await fetch("http://127.0.0.1:8000/reading/audio", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: content.passage }),
    });

    const blob = await res.blob();
    new Audio(URL.createObjectURL(blob)).play();
  };

  const checkUnderstanding = async () => {
    const res = await fetch("http://127.0.0.1:8000/reading/understanding", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: content.passage }),
    });

    const data = await res.json();
    setFeedback(data.feedback);
  };

  const markCompleted = () => {
    localStorage.setItem("reader_readingDone", "1");
    alert("Reading completed! 🎉 Great job!");
  };

  if (loading) {
    return (
      <Layout>
        <div className="p-6 text-center text-gray-500">
          Loading your reading lesson…
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-3xl mx-auto px-4">
        <LessonBox title={content.title}>

          {/* Reading Passage */}
          <div className="bg-white rounded-xl p-5 shadow-sm border mb-5">
            <p className="text-lg leading-relaxed text-gray-800">
              {content.passage}
            </p>
          </div>

          {/* Tips */}
          <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 mb-6">
            <h4 className="font-semibold mb-2 text-blue-700">
              Helpful Tips
            </h4>
            <ul className="list-disc ml-5 text-gray-700">
              {content.tips.map((tip, i) => (
                <li key={i}>{tip}</li>
              ))}
            </ul>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-3 mb-6">
            <button
              onClick={playAudio}
              className="flex items-center justify-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 transition"
            >
              <Volume2 size={18} />
              Play Audio
            </button>

            <button
              onClick={checkUnderstanding}
              className="flex items-center justify-center gap-2 px-4 py-2 bg-green-600 text-white rounded-xl hover:bg-green-700 transition"
            >
              <Brain size={18} />
              Check Understanding
            </button>
          </div>

          {/* Feedback */}
          {feedback && (
            <div className="bg-green-50 border border-green-300 rounded-xl p-4 mb-6">
              <h4 className="font-semibold text-green-700 mb-1">
                Tutor Feedback
              </h4>
              <p className="text-gray-800">{feedback}</p>
            </div>
          )}

          {/* Completion */}
          <div className="text-center">
            <button
              onClick={markCompleted}
              className="inline-flex items-center gap-2 px-6 py-3 bg-purple-600 text-white rounded-full text-lg font-semibold hover:bg-purple-700 transition"
            >
              <CheckCircle size={20} />
              Done Reading
            </button>
          </div>

        </LessonBox>
      </div>
    </Layout>
  );
}
