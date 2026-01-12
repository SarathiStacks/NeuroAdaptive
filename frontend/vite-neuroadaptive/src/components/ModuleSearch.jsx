export default function ModuleSearch({ onSearch }) {
  return (
    <input
      onChange={(e) => onSearch(e.target.value)}
      placeholder="Search modules..."
      className="w-full p-3 rounded-xl border border-gray-300 focus:border-indigo-500 outline-none mb-6 shadow-sm"
    />
  );
}
