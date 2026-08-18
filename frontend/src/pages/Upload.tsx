import { useState } from "react";
import Navbar from "../components/Navbar";
import { uploadPDF } from "../services/api";

function Upload() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");
  const [characters, setCharacters] = useState(0);
  const [preview, setPreview] = useState("");

  async function handleUpload() {
    if (!selectedFile) {
      setMessage("Please select a PDF.");
      return;
    }

    try {
      const result = await uploadPDF(selectedFile);

      setMessage(result.message);
      setCharacters(result.characters);
      setPreview(result.preview);

    } catch (error) {
      console.error(error);
      setMessage("Upload Failed!");
      setCharacters(0);
      setPreview("");
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <Navbar />

      <div className="max-w-3xl mx-auto mt-20 bg-slate-900 p-10 rounded-xl shadow-lg">

        <h1 className="text-5xl font-bold text-cyan-400 text-center mb-8">
          Upload Engineering Document
        </h1>

        <input
          type="file"
          accept=".pdf"
          onChange={(e) => {
            if (e.target.files && e.target.files.length > 0) {
              setSelectedFile(e.target.files[0]);
            }
          }}
          className="w-full mb-6"
        />

        {selectedFile && (
          <p className="text-green-400 mb-6">
            <strong>Selected:</strong> {selectedFile.name}
          </p>
        )}

        <button
          onClick={handleUpload}
          className="w-full bg-cyan-500 hover:bg-cyan-600 py-3 rounded-lg font-semibold transition"
        >
          Upload PDF
        </button>

        {message && (
          <p className="mt-6 text-center text-xl text-cyan-300">
            {message}
          </p>
        )}

        {characters > 0 && (
          <div className="mt-10 bg-slate-800 rounded-lg p-6">

            <h2 className="text-2xl font-bold text-cyan-400 mb-4">
              PDF Information
            </h2>

            <p className="mb-4 text-lg">
              <strong>Characters:</strong> {characters}
            </p>

            <h3 className="text-xl font-semibold mb-2">
              Preview
            </h3>

            <div className="bg-slate-900 p-4 rounded-lg max-h-80 overflow-y-auto">
              <p className="text-slate-300 whitespace-pre-wrap">
                {preview}
              </p>
            </div>

          </div>
        )}

      </div>
    </div>
  );
}

export default Upload;