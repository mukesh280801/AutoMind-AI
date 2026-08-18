import { useEffect, useState } from "react";
import { getBackendStatus } from "../services/api";

function Hero() {
  const [status, setStatus] = useState<any>(null);

  useEffect(() => {
    async function fetchStatus() {
      try {
        const data = await getBackendStatus();
        setStatus(data);
      } catch (error) {
        console.error("Error fetching backend status:", error);
      }
    }

    fetchStatus();
  }, []);

  return (
    <section className="flex flex-col items-center justify-center text-center px-6 pt-32 pb-24">

      <h2 className="text-5xl md:text-6xl font-bold leading-tight">
        AI Workspace for
        <br />
        <span className="text-cyan-400">
          Automotive Engineers
        </span>
      </h2>

      <p className="text-slate-400 text-lg mt-8 max-w-3xl">
        Analyze engineering documents, understand vehicle diagnostics,
        search technical knowledge, and automate engineering workflows
        using Generative AI, RAG, and AI Agents.
      </p>

      {/* Backend Status Card */}
      {status && (
        <div className="mt-8 w-full max-w-xl rounded-xl bg-slate-800 p-6 shadow-lg">
          <h3 className="text-2xl font-semibold text-cyan-400 mb-4">
            Backend Status
          </h3>

          <div className="space-y-2 text-left">
            <p>
              <span className="font-semibold">Project:</span> {status.project}
            </p>

            <p>
              <span className="font-semibold">Backend:</span> {status.backend}
            </p>

            <p>
              <span className="font-semibold">Version:</span> {status.version}
            </p>
          </div>
        </div>
      )}

      <div className="mt-10 flex gap-5">

        <button className="bg-cyan-500 hover:bg-cyan-600 px-7 py-3 rounded-lg font-semibold transition">
          Explore
        </button>

        <button className="border border-cyan-500 px-7 py-3 rounded-lg hover:bg-cyan-500 transition">
          Learn More
        </button>

      </div>

    </section>
  );
}

export default Hero;