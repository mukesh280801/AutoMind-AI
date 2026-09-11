import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";

function Dashboard() {
  const systems = [
    ["◈", "RAG System", "Ready", "Document retrieval pipeline active"],
    ["⌁", "Vector Database", "Qdrant", "Semantic search available"],
    ["✦", "AI Engine", "Ollama", "Grounded response generation"],
  ];

  const pipeline = [
    ["01", "Document Upload", "Engineering PDF"],
    ["02", "Semantic Retrieval", "Qdrant Vector Search"],
    ["03", "Context Processing", "Relevant document chunks"],
    ["04", "AI Response", "Grounded Ollama answer"],
  ];

  return (
    <div className="min-h-screen text-slate-900">
      <Navbar />

      <main className="relative h-[calc(100vh-64px)] overflow-hidden">

        {/* BACKGROUND IMAGE */}
        <div
          className="absolute inset-0 bg-cover bg-center"
          style={{
            backgroundImage: "url('/images/dashboard-auto.jpg')",
          }}
        />

        {/* MAIN CONTENT */}
        <div className="relative h-full">

          <div className="max-w-7xl mx-auto h-full px-5 py-3 flex flex-col">

            {/* HEADER */}
            <div className="flex items-center justify-between mb-2 shrink-0">

              <div className="bg-white rounded-xl px-4 py-2 shadow-lg border border-slate-100">

                <div className="flex items-center gap-3">

                  <div className="h-8 w-8 rounded-lg bg-cyan-50 text-cyan-600 flex items-center justify-center text-sm">
                    ✦
                  </div>

                  <div>
                    <h1 className="text-xl font-black tracking-tight">
                      Engineering Knowledge Dashboard
                    </h1>

                    <p className="text-[9px] text-slate-500">
                      Your workspace for document retrieval and grounded AI.
                    </p>
                  </div>

                </div>

              </div>

              <div className="bg-white rounded-xl px-4 py-2 shadow-lg border border-slate-100">

                <div className="flex items-center gap-2">

                  <span className="h-2 w-2 rounded-full bg-green-500" />

                  <span className="text-[10px] font-bold text-slate-700">
                    All Systems Ready
                  </span>

                </div>

              </div>

            </div>

            {/* HERO */}
            <section className="shrink-0 rounded-2xl bg-gradient-to-r from-cyan-700 to-blue-700 px-7 py-4 text-white shadow-2xl">

              <p className="text-[8px] font-black tracking-[0.22em] text-cyan-100">
                ENGINEERING KNOWLEDGE PLATFORM
              </p>

              <h2 className="mt-1 text-3xl font-black leading-tight">
                Drive Knowledge.
                <br />
                Build Smarter.
              </h2>

              <p className="mt-1.5 text-[11px] text-cyan-50 max-w-2xl leading-5">
                Retrieve and understand automotive engineering knowledge
                from your technical documents using RAG and Generative AI.
              </p>

              <div className="flex gap-3 mt-3">

                <Link
                  to="/chat"
                  className="bg-white text-blue-700 px-5 py-2 rounded-lg text-[11px] font-bold hover:bg-slate-100 transition"
                >
                  Start AI Chat →
                </Link>

                <Link
                  to="/upload"
                  className="border border-white/80 px-5 py-2 rounded-lg text-[11px] font-bold hover:bg-white/10 transition"
                >
                  Upload Document
                </Link>

              </div>

            </section>

            {/* SYSTEM STATUS */}
            <section className="grid grid-cols-3 gap-3 mt-2 shrink-0">

              {systems.map(
                ([icon, title, value, description]) => (
                  <div
                    key={title}
                    className="bg-white rounded-xl px-4 py-2.5 shadow-lg border border-slate-100"
                  >

                    <div className="flex items-center justify-between">

                      <div className="flex items-center gap-2">

                        <div className="h-7 w-7 rounded-lg bg-cyan-50 text-cyan-600 flex items-center justify-center text-xs">
                          {icon}
                        </div>

                        <span className="text-[11px] font-bold text-slate-600">
                          {title}
                        </span>

                      </div>

                      <span className="h-2.5 w-2.5 rounded-full bg-green-500" />

                    </div>

                    <p className="text-base font-black mt-1">
                      {value}
                    </p>

                    <p className="text-[9px] text-slate-500">
                      {description}
                    </p>

                  </div>
                )
              )}

            </section>

            {/* LOWER CONTENT */}
            <section className="grid grid-cols-2 gap-3 mt-2 flex-1 min-h-0">

              {/* QUICK ACTIONS */}
              <div className="bg-white rounded-xl p-4 shadow-lg border border-slate-100">

                <div className="flex items-center justify-between mb-2">

                  <div>
                    <h2 className="text-sm font-black">
                      Quick Actions
                    </h2>

                    <p className="text-[9px] text-slate-500">
                      Start working with engineering knowledge.
                    </p>
                  </div>

                  <span className="text-[8px] font-black tracking-wider text-cyan-600">
                    WORKSPACE
                  </span>

                </div>

                <div className="grid grid-cols-2 gap-3">

                  <Link
                    to="/chat"
                    className="border border-slate-200 rounded-xl p-3 hover:border-cyan-300 hover:bg-cyan-50 transition"
                  >

                    <div className="h-7 w-7 rounded-lg bg-cyan-50 flex items-center justify-center text-xs">
                      💬
                    </div>

                    <h3 className="text-[11px] font-black mt-2">
                      AI Engineering Chat
                    </h3>

                    <p className="text-[9px] text-slate-500 mt-1">
                      Ask questions from documents.
                    </p>

                  </Link>

                  <Link
                    to="/upload"
                    className="border border-slate-200 rounded-xl p-3 hover:border-cyan-300 hover:bg-cyan-50 transition"
                  >

                    <div className="h-7 w-7 rounded-lg bg-cyan-50 flex items-center justify-center text-xs">
                      📄
                    </div>

                    <h3 className="text-[11px] font-black mt-2">
                      Upload Document
                    </h3>

                    <p className="text-[9px] text-slate-500 mt-1">
                      Add engineering PDFs.
                    </p>

                  </Link>

                </div>

              </div>

              {/* KNOWLEDGE PIPELINE */}
              <div className="bg-white rounded-xl p-4 shadow-lg border border-slate-100">

                <div className="mb-2">

                  <h2 className="text-sm font-black">
                    Knowledge Pipeline
                  </h2>

                  <p className="text-[9px] text-slate-500">
                    From engineering document to grounded answer.
                  </p>

                </div>

                <div className="space-y-1.5">

                  {pipeline.map(
                    ([number, title, description]) => (
                      <div
                        key={number}
                        className="flex items-center gap-2"
                      >

                        <div className="h-7 w-7 shrink-0 rounded-lg bg-cyan-50 text-cyan-700 flex items-center justify-center text-[8px] font-black">
                          {number}
                        </div>

                        <div className="flex-1 bg-slate-50 rounded-lg px-3 py-1.5 border border-slate-100 flex items-center justify-between">

                          <div>
                            <p className="text-[9px] font-black">
                              {title}
                            </p>

                            <p className="text-[8px] text-slate-400">
                              {description}
                            </p>
                          </div>

                          <span className="text-[7px] text-green-600 font-black">
                            READY
                          </span>

                        </div>

                      </div>
                    )
                  )}

                </div>

              </div>

            </section>

          </div>
        </div>
      </main>
    </div>
  );
}

export default Dashboard;