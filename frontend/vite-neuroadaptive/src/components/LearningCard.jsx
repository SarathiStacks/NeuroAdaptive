import { Link } from "react-router-dom";
import { motion } from "framer-motion"; // ✔ ADD THIS

export default function LearningCard({ title, description, icon: Icon, path }) {
  return (
    <Link to={path}>
      <motion.div
        whileHover={{ scale: 1.05 }}
        className="bg-white shadow-md hover:shadow-xl hover:border-indigo-300 border border-transparent rounded-2xl p-5 flex flex-col items-center gap-3 text-center transition-all duration-300"
      >
        <div className="bg-indigo-50 p-3 rounded-full">
          <Icon size={28} className="text-indigo-600" />
        </div>

        <h3 className="text-lg font-bold text-gray-800">{title}</h3>
        <p className="text-sm text-gray-600">{description}</p>

        <span className="mt-2 bg-indigo-600 text-white text-xs font-semibold px-3 py-1.5 rounded-lg">
          Open
        </span>
      </motion.div>
    </Link>
  );
}
