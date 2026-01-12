import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import ProgressBar from "../components/ProgressBar";
import CircularScore from "../components/CircularScore";
import { Brain, PenTool } from "lucide-react";

export default function Progress() {
  const [state, setState] = useState({
    reading: 0,
    handwriting: 0,
    quiz: 0,
    attention: 0,
    mastery: 0,
    clarity: 0,
    reward: ""
  });

  useEffect(() => {
    const update = () => {
      setState({
        reading: localStorage.getItem("reader_readingDone") === "1" ? 100 : 0,
        handwriting: localStorage.getItem("reader_handwritingDone") === "1" ? 100 : 0,
        quiz: localStorage.getItem("reader_quizDone") === "1" ? 100 : 0,
        attention: Number(localStorage.getItem("attentionScore") || 0) * 100,
        mastery: Number(localStorage.getItem("knowledgeMastery") || 0) * 100,
        clarity: Number(localStorage.getItem("handwritingClarity") || 0) * 100,
        reward: JSON.parse(localStorage.getItem("quizReward") || "{}").reward || ""
      });
    };

    update();
    const interval = setInterval(update, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <Layout>
      <div className="max-w-4xl mx-auto px-4">

        <h2 className="text-3xl font-bold mb-6 flex items-center gap-2">
          <Brain size={28} /> Learning Progress
        </h2>

        <div className="space-y-4 mb-8">
          <ProgressBar label="Reading" value={state.reading} />
          <ProgressBar label="Handwriting" value={state.handwriting} />
          <ProgressBar label="Quiz Completion" value={state.quiz} />
        </div>

        <div className="flex justify-around bg-white rounded-2xl p-6 shadow border mb-8">
          <CircularScore label="Focus" value={state.attention} />
          <CircularScore label="Mastery" value={state.mastery} />
          <CircularScore label="Clarity" value={state.clarity} />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-white p-4 border rounded-xl shadow">
            <PenTool size={22} className="mb-2 text-green-600" />
            <p className="font-semibold">Handwriting Clarity</p>
            <p className="text-sm text-gray-600">
              {state.clarity > 70 ? "Very clear ✨" :
               state.clarity > 40 ? "Readable ✍️" :
               "Needs improvement 💡"}
            </p>
          </div>

          <div className="bg-white p-4 border rounded-xl shadow">
            <Brain size={22} className="mb-2 text-purple-600" />
            <p className="font-semibold">Focus Level</p>
            <p className="text-sm text-gray-600">
              {state.attention > 70 ? "High 🎯" :
               state.attention > 40 ? "Medium 🙂" :
               "Low — take a break 💛"}
            </p>
          </div>
        </div>

        {state.reward && (
          <div className="mt-6 text-center text-xl font-bold text-indigo-600">
            {state.reward}
          </div>
        )}

      </div>
    </Layout>
  );
}
