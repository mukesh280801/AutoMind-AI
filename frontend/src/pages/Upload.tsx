import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import { uploadPDF } from "../services/api";

const BASE_URL = "http://127.0.0.1:8000";

type Document = {
  filename: string;
  chunks: number;
};

function Upload() {
  const [selectedFile, setSelectedFile] =
    useState<File | null>(null);

  const [message, setMessage] =
    useState("");

  const [characters, setCharacters] =
    useState(0);

  const [preview, setPreview] =
    useState("");

  const [documents, setDocuments] =
    useState<Document[]>([]);

  const [loadingDocuments, setLoadingDocuments] =
    useState(true);

  const [uploading, setUploading] =
    useState(false);


  // =========================================================
  // LOAD UPLOADED DOCUMENTS
  // =========================================================

  async function loadDocuments() {
    try {
      setLoadingDocuments(true);

      const response = await fetch(
        `${BASE_URL}/api/documents`
      );

      if (!response.ok) {
        throw new Error(
          `Document request failed: ${response.status}`
        );
      }

      const data = await response.json();

      setDocuments(
        data.documents || []
      );

    } catch (error) {
      console.error(
        "Failed to load documents:",
        error
      );

      setDocuments([]);

    } finally {
      setLoadingDocuments(false);
    }
  }


  // =========================================================
  // LOAD DOCUMENTS WHEN PAGE OPENS
  // =========================================================

  useEffect(() => {
    loadDocuments();
  }, []);


  // =========================================================
  // UPLOAD PDF
  // =========================================================

  async function handleUpload() {
    if (!selectedFile || uploading) {
      return;
    }

    try {
      setUploading(true);
      setMessage("");

      const result =
        await uploadPDF(selectedFile);

      setMessage(result.message);
      setCharacters(result.characters);
      setPreview(result.preview);

      // Refresh persistent document list
      await loadDocuments();

    } catch (error) {
      console.error(error);

      setMessage("Upload Failed!");
      setCharacters(0);
      setPreview("");

    } finally {
      setUploading(false);
    }
  }


  return (
    <div className="min-h-screen text-slate-900 overflow-hidden">

      <Navbar />

      <main className="relative h-[calc(100vh-64px)] overflow-hidden">

        {/* ================================================= */}
        {/* BACKGROUND */}
        {/* ================================================= */}

        <div
          className="absolute inset-0 bg-cover bg-center"
          style={{
            backgroundImage:
              "url('/images/upload-document.jpg')",
          }}
        />

        <div className="relative h-full">

          <div className="max-w-7xl mx-auto h-full px-5 py-3">

            {/* ================================================= */}
            {/* HEADER */}
            {/* ================================================= */}

            <div className="mb-3">

              <div className="inline-flex items-center gap-2 bg-white rounded-xl px-4 py-2 shadow-lg border border-slate-100">

                <span className="h-2.5 w-2.5 rounded-full bg-cyan-500" />

                <div>

                  <h1 className="text-xl font-black tracking-tight">
                    Upload Engineering Document
                  </h1>

                  <p className="text-[9px] text-slate-500">
                    Add technical PDFs to the AutoMind AI knowledge base.
                  </p>

                </div>

              </div>

            </div>


            {/* ================================================= */}
            {/* MAIN GRID */}
            {/* ================================================= */}

            <div className="grid grid-cols-[minmax(0,1fr)_300px] gap-4 h-[calc(100%-58px)]">

              {/* ================================================= */}
              {/* LEFT SIDE */}
              {/* ================================================= */}

              <div className="space-y-3 min-h-0">

                {/* ================================================= */}
                {/* UPLOAD CARD */}
                {/* ================================================= */}

                <div className="bg-white rounded-2xl p-5 shadow-2xl border border-white">

                  {/* CARD HEADER */}

                  <div className="flex items-center gap-3 mb-3">

                    <div className="h-9 w-9 rounded-xl bg-cyan-50 flex items-center justify-center text-sm">
                      📄
                    </div>

                    <div>

                      <h2 className="text-sm font-black">
                        Document Ingestion
                      </h2>

                      <p className="text-[9px] text-slate-400">
                        PDF → Text → Chunks → Embeddings → Vector Database
                      </p>

                    </div>

                  </div>


                  {/* DROP AREA */}

                  <label className="h-[135px] border-2 border-dashed border-cyan-400 rounded-2xl bg-cyan-50/70 flex flex-col items-center justify-center cursor-pointer hover:bg-cyan-50 transition">

                    <div className="h-11 w-11 bg-white rounded-xl shadow-sm border border-cyan-100 flex items-center justify-center text-xl">
                      ↑
                    </div>

                    <h3 className="text-sm font-black mt-2">
                      Select an engineering PDF
                    </h3>

                    <p className="text-[10px] text-slate-400 mt-1">
                      Click here to browse your files
                    </p>

                    <span className="mt-2 px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-[9px] font-bold text-cyan-700">
                      Choose PDF
                    </span>

                    <input
                      type="file"
                      accept=".pdf"
                      className="hidden"
                      onChange={(e) => {

                        if (
                          e.target.files &&
                          e.target.files.length > 0
                        ) {

                          setSelectedFile(
                            e.target.files[0]
                          );

                          setMessage("");
                        }

                      }}
                    />

                  </label>


                  {/* SELECTED FILE */}

                  {selectedFile && (

                    <div className="mt-2.5 bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 flex items-center justify-between">

                      <div className="flex items-center gap-2 min-w-0">

                        <div className="h-8 w-8 shrink-0 rounded-lg bg-red-50 text-red-500 flex items-center justify-center text-[9px] font-black">
                          PDF
                        </div>

                        <div className="min-w-0">

                          <p className="text-[10px] font-bold truncate">
                            {selectedFile.name}
                          </p>

                          <p className="text-[8px] text-slate-400">
                            {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                          </p>

                        </div>

                      </div>

                      <span className="text-[8px] font-black text-green-600">
                        READY
                      </span>

                    </div>

                  )}


                  {/* UPLOAD BUTTON */}

                  <button
                    onClick={handleUpload}
                    disabled={
                      !selectedFile ||
                      uploading
                    }
                    className={`w-full mt-2.5 py-2.5 rounded-xl text-[11px] font-black transition shadow-sm ${
                      selectedFile &&
                      !uploading
                        ? "bg-cyan-600 hover:bg-cyan-700 text-white"
                        : "bg-slate-300 text-white cursor-not-allowed"
                    }`}
                  >
                    {uploading
                      ? "Processing Document..."
                      : "Upload & Process Document"}
                  </button>


                  {/* STATUS */}

                  {message && (

                    <div
                      className={`mt-2.5 rounded-xl px-3 py-2 text-center text-[10px] font-bold ${
                        message === "Upload Failed!"
                          ? "bg-red-50 border border-red-100 text-red-600"
                          : "bg-green-50 border border-green-100 text-green-600"
                      }`}
                    >
                      {message}
                    </div>

                  )}


                  {/* DOCUMENT INFO */}

                  {characters > 0 && (

                    <div className="mt-2.5">

                      <div className="grid grid-cols-2 gap-2">

                        <div className="bg-slate-50 rounded-xl p-2.5 border border-slate-100">

                          <p className="text-[8px] font-bold text-slate-400 uppercase tracking-wider">
                            Characters
                          </p>

                          <p className="text-base font-black mt-1">
                            {characters.toLocaleString()}
                          </p>

                        </div>


                        <div className="bg-slate-50 rounded-xl p-2.5 border border-slate-100">

                          <p className="text-[8px] font-bold text-slate-400 uppercase tracking-wider">
                            Status
                          </p>

                          <p className="text-base font-black text-green-600 mt-1">
                            INGESTED
                          </p>

                        </div>

                      </div>


                      {/* PREVIEW */}

                      {preview && (

                        <div className="mt-2.5">

                          <p className="text-[10px] font-black mb-1">
                            Document Preview
                          </p>

                          <div className="h-[55px] overflow-hidden bg-slate-50 border border-slate-200 rounded-xl px-3 py-2">

                            <p className="text-[8px] text-slate-500 leading-3.5">
                              {preview}
                            </p>

                          </div>

                        </div>

                      )}

                    </div>

                  )}

                </div>


                {/* ================================================= */}
                {/* UPLOADED DOCUMENTS */}
                {/* ================================================= */}

                <div className="bg-white rounded-2xl p-4 shadow-2xl border border-white">

                  <div className="flex items-center justify-between mb-2">

                    <div>

                      <h2 className="text-sm font-black">
                        Uploaded Documents
                      </h2>

                      <p className="text-[9px] text-slate-400">
                        Documents currently available in the RAG knowledge base.
                      </p>

                    </div>

                    <div className="bg-cyan-50 text-cyan-700 rounded-lg px-2.5 py-1 text-[9px] font-black">
                      {documents.length} DOCUMENTS
                    </div>

                  </div>


                  {/* LOADING */}

                  {loadingDocuments ? (

                    <div className="py-4 text-center">

                      <p className="text-[10px] text-slate-400">
                        Loading knowledge base...
                      </p>

                    </div>

                  ) : documents.length === 0 ? (

                    <div className="py-4 text-center bg-slate-50 rounded-xl border border-slate-100">

                      <p className="text-[10px] font-semibold text-slate-500">
                        No documents uploaded yet.
                      </p>

                    </div>

                  ) : (

                    <div className="grid grid-cols-3 gap-2">

                      {documents.map(
                        (document) => (

                          <div
                            key={document.filename}
                            className="bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5"
                          >

                            <div className="flex items-center gap-2">

                              <div className="h-7 w-7 shrink-0 rounded-lg bg-red-50 text-red-500 flex items-center justify-center text-[8px] font-black">
                                PDF
                              </div>

                              <div className="min-w-0">

                                <p
                                  className="text-[9px] font-bold text-slate-700 truncate"
                                  title={document.filename}
                                >
                                  {document.filename}
                                </p>

                                <p className="text-[8px] text-slate-400 mt-0.5">
                                  {document.chunks} chunks
                                </p>

                              </div>

                            </div>

                          </div>

                        )
                      )}

                    </div>

                  )}

                </div>

              </div>


              {/* ================================================= */}
              {/* RIGHT SIDEBAR */}
              {/* ================================================= */}

              <div className="space-y-3">

                {/* PIPELINE */}

                <div className="bg-white rounded-2xl p-4 shadow-2xl border border-white">

                  <h2 className="text-sm font-black">
                    Document Pipeline
                  </h2>

                  <div className="space-y-2 mt-3">

                    {[
                      ["01", "PDF Upload"],
                      ["02", "Text Extraction"],
                      ["03", "Chunking"],
                      ["04", "Embeddings"],
                      ["05", "Qdrant Storage"],
                    ].map(
                      ([number, title]) => (

                        <div
                          key={number}
                          className="flex items-center gap-2"
                        >

                          <div className="h-8 w-8 rounded-lg bg-cyan-50 text-cyan-600 flex items-center justify-center text-[9px] font-black">
                            {number}
                          </div>

                          <span className="text-[10px] font-semibold text-slate-600">
                            {title}
                          </span>

                        </div>

                      )
                    )}

                  </div>

                </div>


                {/* AUTOMOTIVE AI */}

                <div className="bg-slate-950 rounded-2xl p-4 shadow-2xl text-white">

                  <p className="text-[8px] font-black tracking-[0.2em] text-cyan-400">
                    AUTOMOTIVE AI
                  </p>

                  <h2 className="text-base font-black mt-2">
                    Build Your Knowledge Base
                  </h2>

                  <p className="text-[9px] text-slate-400 leading-4 mt-2">
                    Upload automotive technical documents and make them
                    searchable through the RAG-powered AI assistant.
                  </p>

                  <div className="border-t border-slate-700 mt-3 pt-3 flex items-center justify-between">

                    <span className="text-[8px] text-slate-500">
                      VECTOR DATABASE
                    </span>

                    <span className="text-[8px] font-black text-green-400">
                      READY
                    </span>

                  </div>

                </div>

              </div>

            </div>

          </div>

        </div>

      </main>

    </div>
  );
}

export default Upload;