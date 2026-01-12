import { motion } from "framer-motion";

export default function LessonBox({ title, children }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-2xl shadow-lg p-6 mb-6 border border-gray-100 text-left"
    >
      <h3 className="text-2xl font-bold text-indigo-600 mb-3">{title}</h3>
      {children}
    </motion.div>
  );
}
