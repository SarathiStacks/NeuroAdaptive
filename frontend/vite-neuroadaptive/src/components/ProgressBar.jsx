export default function ProgressBar({ label, value }) {
  return (
    <div className="mb-5">
      <p className="text-gray-700 font-medium mb-1">{label}</p>
      <div className="w-full bg-gray-200 rounded-full h-3">
        <div
          className="bg-indigo-600 h-3 rounded-full transition-all"
          style={{ width: `${value}%` }}
        ></div>
      </div>
      <p className="text-xs text-gray-500 mt-1">{value}%</p>
    </div>
  );
}
