import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import { Trophy, BookOpen, PenTool, Brain } from "lucide-react";

export default function Achievements() {
  const [badges, setBadges] = useState([]);

  useEffect(() => {
    const updateBadges = () => {
      const newBadges = [];

      if (localStorage.getItem("reader_readingDone") === "1") {
        newBadges.push({ icon: <BookOpen />, text: "Reading Completed" });
      }

      if (localStorage.getItem("reader_handwritingDone") === "1") {
        newBadges.push({ icon: <PenTool />, text: "Handwriting Uploaded" });
      }

      if (localStorage.getItem("reader_quizDone") === "1") {
        newBadges.push({ icon: <Brain />, text: "Quiz Finished" });
      }

      if (localStorage.getItem("quizReward")) {
        newBadges.push({ icon: <Trophy />, text: "Adaptive Learning Reward" });
      }

      setBadges(newBadges);
    };

    updateBadges();
    const interval = setInterval(updateBadges, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <Layout>
      <div className="max-w-3xl mx-auto p-6">
        <h1 className="text-3xl font-bold text-center mb-6">
          Achievements
        </h1>

        {badges.length === 0 && (
          <p className="text-center text-gray-500">
            Complete activities to unlock achievements 🌱
          </p>
        )}

        <div className="grid grid-cols-2 gap-4">
          {badges.map((badge, i) => (
            <div
              key={i}
              className="flex flex-col items-center p-4 bg-white border rounded-xl shadow"
            >
              <div className="mb-2 text-indigo-600">{badge.icon}</div>
              <p className="font-semibold text-center">{badge.text}</p>
            </div>
          ))}
        </div>

        <div className="mt-6 text-center text-lg font-semibold text-green-600">
          Keep going — learning is a journey 🌟
        </div>
      </div>
    </Layout>
  );
}
