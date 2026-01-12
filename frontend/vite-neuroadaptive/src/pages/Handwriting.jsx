import { useState } from "react";
import Layout from "../components/Layout";

export default function Handwriting() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/handwriting/upload", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      console.log("Backend returned:", data);

      if (!res.ok) throw new Error(data.error || "Upload failed");

      setResult(data);
      localStorage.setItem("handwritingUploaded", "true");

    } catch (err) {
      console.error("Upload error:", err);
      setResult({ error: err.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="max-w-2xl mx-auto mt-10 bg-white p-6 rounded-xl shadow-md border">
        <h2 className="text-2xl font-bold mb-4">Handwriting Helper</h2>

        <input
          type="file"
          accept="image/*"
          onChange={handleUpload}
          className="w-full p-3 border-2 rounded cursor-pointer"
        />

        {loading && <p className="mt-3 text-blue-500">Processing...</p>}

        {result && !result.error && (
          <>
            <div className="mt-4 p-3 bg-gray-50 border rounded">
              <h4 className="font-semibold">Extracted Text:</h4>
              <p className="whitespace-pre-line">{result.extractedText}</p>
            </div>

            <p className="mt-3 text-green-700 font-medium">
              Clarity Score: {result.clarityScore?.toFixed(2)}
            </p>

            {result.improvement && (
              <div className="mt-4 p-3 bg-yellow-50 border-l-4 border-yellow-400 rounded">
                <strong className="text-yellow-700">Try improving:</strong>
                <ul className="list-disc ml-5 text-sm mt-2">
                  {result.improvement.map((tip,i)=><li key={i}>{tip}</li>)}
                </ul>
              </div>
            )}

            <div className="mt-3 p-3 bg-green-50 border-l-4 border-green-400 rounded">
              <p className="text-sm">{result.message}</p>
            </div>
          </>
        )}

        {result?.error && (
          <p className="mt-3 text-red-500">Error: {result.error}</p>
        )}
      </div>
    </Layout>
  );
}
