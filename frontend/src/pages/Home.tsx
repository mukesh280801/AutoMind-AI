import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";

function Home() {
  return (
    <div className="min-h-screen text-slate-900">
      <Navbar />

      <main className="relative h-[calc(100vh-64px)] overflow-hidden">

        {/* Background Image */}
        <div
          className="absolute inset-0 bg-cover bg-center"
          style={{
            backgroundImage: "url('/images/home-car.jpg')",
          }}
        />

        <div className="relative h-full overflow-y-auto">

          <div className="max-w-7xl mx-auto px-5 py-8">

            <div className="grid lg:grid-cols-2 gap-8 items-center min-h-[calc(100vh-140px)]">

              {/* LEFT CONTENT */}
              <div className="max-w-xl">

                {/* Automotive Engineering AI Badge */}
                <div className="inline-flex items-center gap-3 bg-white rounded-full px-5 py-2.5 shadow-xl border border-cyan-200">

                  <span className="relative flex h-3 w-3">
                    <span className="absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-60 animate-ping" />
                    <span className="relative inline-flex h-3 w-3 rounded-full bg-cyan-600" />
                  </span>

                  <span className="text-sm md:text-base font-black tracking-[0.16em] text-slate-800">
                    AUTOMOTIVE{" "}
                    <span className="text-cyan-600">
                      ENGINEERING AI
                    </span>
                  </span>

                </div>

                {/* Main Hero Card */}
                <div className="mt-5 bg-white rounded-2xl p-7 shadow-2xl border border-white">

                  <h1 className="text-5xl md:text-6xl font-black leading-[1.02] tracking-tight">

                    Engineering

                    <span className="block text-cyan-600">
                      Knowledge,
                    </span>

                    <span className="block text-cyan-600">
                      Accelerated.
                    </span>

                  </h1>

                  <p className="mt-5 text-base text-slate-600 leading-7 max-w-lg">
                    AutoMind AI helps automotive engineers retrieve,
                    understand, and explore technical knowledge from
                    engineering documents using Retrieval-Augmented
                    Generation.
                  </p>

                  {/* Buttons */}
                  <div className="flex flex-wrap gap-3 mt-7">

                    <Link
                      to="/chat"
                      className="bg-cyan-600 hover:bg-cyan-700 text-white px-6 py-3 rounded-xl text-sm font-bold shadow-md transition"
                    >
                      Start AI Chat →
                    </Link>

                    <Link
                      to="/upload"
                      className="bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 px-6 py-3 rounded-xl text-sm font-bold transition"
                    >
                      Upload Document
                    </Link>

                  </div>

                  {/* Features */}
                  <div className="flex flex-wrap gap-5 mt-7 text-xs text-slate-500 font-semibold">

                    <span>
                      ✓ RAG Retrieval
                    </span>

                    <span>
                      ✓ Qdrant Search
                    </span>

                    <span>
                      ✓ Grounded AI
                    </span>

                  </div>

                </div>

              </div>

              {/* RIGHT CONTENT */}
              <div className="flex justify-end">

                <div className="w-full max-w-md space-y-3">

                  {/* Information Card */}
                  <div className="bg-white rounded-2xl p-6 shadow-2xl border border-white">

                    <p className="text-[10px] font-black tracking-[0.22em] text-cyan-600">
                      ENGINEERING KNOWLEDGE WORKSPACE
                    </p>

                    <h2 className="text-2xl font-black mt-2 leading-tight">
                      From technical documents
                      <span className="block text-cyan-600">
                        to engineering answers.
                      </span>
                    </h2>

                    <p className="text-sm text-slate-500 mt-3 leading-6">
                      Upload engineering documents, retrieve relevant
                      context, and generate grounded responses through
                      the AutoMind AI pipeline.
                    </p>

                  </div>

                  {/* System Cards */}
                  <div className="grid grid-cols-3 gap-2">

                    <div className="bg-white rounded-xl p-3.5 shadow-xl border border-white">

                      <p className="text-[9px] font-bold tracking-wider text-slate-400">
                        RAG SYSTEM
                      </p>

                      <div className="flex items-center gap-2 mt-2">

                        <span className="h-2 w-2 rounded-full bg-green-500" />

                        <p className="text-sm font-black">
                          Active
                        </p>

                      </div>

                    </div>

                    <div className="bg-white rounded-xl p-3.5 shadow-xl border border-white">

                      <p className="text-[9px] font-bold tracking-wider text-slate-400">
                        VECTOR DB
                      </p>

                      <div className="flex items-center gap-2 mt-2">

                        <span className="h-2 w-2 rounded-full bg-green-500" />

                        <p className="text-sm font-black">
                          Qdrant
                        </p>

                      </div>

                    </div>

                    <div className="bg-white rounded-xl p-3.5 shadow-xl border border-white">

                      <p className="text-[9px] font-bold tracking-wider text-slate-400">
                        AI ENGINE
                      </p>

                      <div className="flex items-center gap-2 mt-2">

                        <span className="h-2 w-2 rounded-full bg-green-500" />

                        <p className="text-sm font-black">
                          Ollama
                        </p>

                      </div>

                    </div>

                  </div>

                  {/* Bottom Feature Card */}
                  <div className="bg-slate-950 rounded-2xl p-5 shadow-2xl text-white">

                    <div className="flex items-center justify-between">

                      <div>

                        <p className="text-[9px] font-black tracking-[0.2em] text-cyan-400">
                          BUILT FOR ENGINEERS
                        </p>

                        <h3 className="text-lg font-black mt-1">
                          Search. Understand. Engineer.
                        </h3>

                      </div>

                      <div className="h-10 w-10 rounded-xl bg-cyan-500/10 border border-cyan-400/20 flex items-center justify-center text-cyan-400 text-lg">
                        ✦
                      </div>

                    </div>

                    <p className="text-xs text-slate-400 mt-3 leading-5">
                      A focused RAG workspace for retrieving reliable
                      knowledge from automotive engineering documents.
                    </p>

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

export default Home;