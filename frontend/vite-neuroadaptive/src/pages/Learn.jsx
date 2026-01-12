import Layout from "../components/Layout";
import LearningGrid from "../components/LearningGrid";

export default function Learn() {
  return (
    <Layout>
      <div className="text-center pt-24 px-4">
        <h2 className="text-3xl font-bold text-indigo-600 mb-6">Choose a Module</h2>
        <LearningGrid />  {/* Cards will show now */}
      </div>
    </Layout>
  );
}
