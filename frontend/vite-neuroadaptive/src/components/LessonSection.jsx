export default function LessonSection({ heading, children }) {
  return (
    <div className="bg-white rounded-2xl shadow p-6 mb-6 border border-gray-100 text-left">
      <h3 className="text-xl font-bold text-indigo-600 mb-3">{heading}</h3>
      {children}
    </div>
  );
}
