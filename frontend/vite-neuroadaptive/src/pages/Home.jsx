import Layout from "../components/Layout";
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <Layout>
      <div className="flex flex-col items-center justify-center mt-20 text-center">
        <h1 className="text-5xl font-extrabold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-4">
          Welcome to NeuroAdaptive
        </h1>
        <p className="text-gray-600 text-lg max-w-lg mb-8">
          AI‑adaptive learning for every student
        </p>

        <Link to="/learn">
          <button className="bg-indigo-600 text-white px-8 py-3 text-lg rounded-xl font-semibold hover:bg-indigo-700 transition shadow-lg">
            Start Learning
          </button>
        </Link>
      </div>
    </Layout>
  );
}
