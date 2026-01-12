import { motion } from "framer-motion";

export default function CircleScore({ label, value }) {
  return (
    <div className="flex flex-col items-center">
      <motion.div
        initial={{ rotate: -90 }}
        animate={{ rotate: 0 }}
        className="w-20 h-20 rounded-full bg-gradient-to-br from-indigo-400 to-purple-500 flex items-center justify-center text-white font-bold text-xl shadow-md"
      >
        {value}%
      </motion.div>
      <p className="mt-2 text-gray-700 font-medium">{label}</p>
    </div>
  );
}
