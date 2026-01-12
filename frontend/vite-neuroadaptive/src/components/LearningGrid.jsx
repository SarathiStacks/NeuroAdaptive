import { BookOpen, PenTool, Brain, Trophy } from "lucide-react";
import LearningCard from "./LearningCard";

export default function LearningGrid({ filter = "" }) {
  const activities = [
    { title: "Reading Tutor", description: "Adaptive reading lessons", icon: BookOpen, path: "/reader" },
    { title: "Handwriting Helper", description: "Improve writing skills", icon: PenTool, path: "/handwriting" },
    { title: "Knowledge Quiz", description: "Adaptive quizzes", icon: Brain, path: "/quiz" },
    { title: "Achievements", description: "Badges and milestones", icon: Trophy, path: "/achievements" }
  ];

  const filtered = activities.filter(a =>
    a.title.toLowerCase().includes(filter.toLowerCase()) // ✔ correct key exists
  );

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-5 mt-4">
      {filtered.map((a, i) => (
        <LearningCard key={i} {...a} />
      ))}
    </div>
  );
}
