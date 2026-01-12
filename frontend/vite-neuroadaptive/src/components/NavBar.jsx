import { Link } from "react-router-dom";
import { Brain } from "lucide-react";

export default function Navbar() {
  return (
    <nav className="bg-white/80 backdrop-blur fixed w-full top-0 shadow-sm px-6 py-4 flex justify-between items-center">
      {/* Logo */}
      <div className="flex items-center gap-2 font-bold text-xl text-indigo-600">
        <Brain size={22} />
        <span>NeuroAdaptive</span>
      </div>

      {/* Navigation Links */}
      <div className="flex items-center gap-5 text-gray-700 font-medium">
        <Link to="/learn" className="hover:text-indigo-600 transition">Learn</Link>
        <Link to="/progress" className="hover:text-indigo-600 transition">Progress</Link>
        <Link to="/" className="hover:text-indigo-600 transition">Home</Link>
      </div>
    </nav>
  );
}
