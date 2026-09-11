import { useState } from "react";
import Navbar from "../components/Navbar";

const BASE_URL = "http://127.0.0.1:8000";

type Source = {
  filename: string;
  chunk_id: number | null;
  score: number;
};

type Message = {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
};

type ChatResponse = {
  version: string;
  thread_id: string;
  question: string;
  intent: string;
  answer: string;
  sources: Source[];
};

function Chat() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const [threadId] = useState(() => {
    const existingThreadId =
      localStorage.getItem("automind-thread-id");

    if (existingThreadId) {
      return existingThreadId;
    }

    const newThreadId =
      `frontend-chat-${crypto.randomUUID()}`;

    localStorage.setItem(
      "automind-thread-id",
      newThreadId
    );

    return newThreadId;
  });

  async function sendMessage() {
    const trimmed = question.trim();

    if (!trimmed || loading) {
      return;
    }

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: trimmed,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch(
        `${BASE_URL}/api/v2/chat`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: trimmed,
            thread_id: threadId,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(
          `Chat request failed: ${response.status}`
        );
      }

      const data: ChatResponse =
        await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            data.answer ||
            "I couldn't find that information in the uploaded documents.",
          sources: data.sources || [],
        },
      ]);

    } catch (error) {
      console.error(
        "Chat request error:",
        error
      );

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Sorry, something went wrong while contacting AutoMind AI.",
          sources: [],
        },
      ]);

    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(
    event: React.KeyboardEvent<HTMLTextAreaElement>
  ) {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();
      sendMessage();
    }
  }

  return (
    <div className="min-h-screen text-slate-900">

      <Navbar />

      <main className="relative h-[calc(100vh-64px)] overflow-hidden">

        {/* Background */}
        <div
          className="absolute inset-0 bg-cover bg-center"
          style={{
            backgroundImage:
              "url('/images/chat-engineering.jpg')",
          }}
        />

        <div className="relative h-full overflow-hidden">

          <div className="max-w-7xl mx-auto h-full px-4 py-3">

            {/* ================================================= */}
            {/* HEADER */}
            {/* ================================================= */}

            <div className="flex items-center justify-between mb-3">

              <div className="bg-white rounded-xl px-4 py-2 shadow-lg">

                <div className="flex items-center gap-2">

                  <span className="h-2 w-2 rounded-full bg-green-500" />

                  <div>
                    <h1 className="text-xl md:text-2xl font-bold">
                      AutoMind AI
                    </h1>

                    <p className="text-[10px] text-slate-500">
                      Automotive engineering knowledge assistant
                    </p>
                  </div>

                </div>

              </div>

              <div className="bg-white rounded-xl px-3 py-2 shadow-lg">

                <div className="flex items-center gap-2">

                  <span className="h-2 w-2 rounded-full bg-green-500" />

                  <span className="text-[10px] font-semibold text-slate-600">
                    KNOWLEDGE BASE READY
                  </span>

                </div>

              </div>

            </div>

            {/* ================================================= */}
            {/* WORKSPACE */}
            {/* ================================================= */}

            <div className="grid lg:grid-cols-[1fr_235px] gap-3 h-[calc(100%-68px)]">

              {/* ================================================= */}
              {/* CHAT PANEL */}
              {/* ================================================= */}

              <section className="bg-white rounded-2xl shadow-xl overflow-hidden flex flex-col min-h-0">

                {/* Chat Header */}
                <div className="px-4 py-3 border-b border-slate-100 flex items-center justify-between">

                  <div className="flex items-center gap-2">

                    <div className="h-8 w-8 rounded-lg bg-cyan-50 text-cyan-600 flex items-center justify-center">
                      ✦
                    </div>

                    <div>

                      <h2 className="text-sm font-bold">
                        Engineering Assistant
                      </h2>

                      <p className="text-[10px] text-slate-400">
                        Grounded responses from uploaded documents
                      </p>

                    </div>

                  </div>

                  <div className="text-[9px] font-bold text-green-600">
                    ● RAG ACTIVE
                  </div>

                </div>

                {/* ================================================= */}
                {/* MESSAGES */}
                {/* ================================================= */}

                <div className="flex-1 min-h-0 overflow-y-auto p-4">

                  {messages.length === 0 ? (

                    <div className="h-full flex items-center justify-center">

                      <div className="max-w-xl w-full text-center">

                        <div className="mx-auto h-12 w-12 rounded-xl bg-cyan-50 border border-cyan-100 flex items-center justify-center text-xl">
                          ⚙
                        </div>

                        <h2 className="mt-3 text-lg font-bold">
                          Ask your engineering question
                        </h2>

                        <p className="text-xs text-slate-500 mt-1 leading-5">
                          AutoMind AI retrieves relevant technical
                          context before generating an answer.
                        </p>

                        <div className="grid grid-cols-3 gap-2 mt-4">

                          {[
                            "What is CAN bus?",
                            "Explain automotive Bluetooth",
                            "Summarize the document",
                          ].map((text) => (

                            <button
                              key={text}
                              onClick={() =>
                                setQuestion(text)
                              }
                              className="text-left px-3 py-2.5 rounded-xl border border-slate-200 bg-slate-50 hover:bg-cyan-50 hover:border-cyan-300 transition"
                            >

                              <span className="text-[8px] font-bold text-cyan-600">
                                SUGGESTED
                              </span>

                              <p className="mt-1 text-[10px] font-medium text-slate-700">
                                {text}
                              </p>

                            </button>

                          ))}

                        </div>

                      </div>

                    </div>

                  ) : (

                    <div className="space-y-3">

                      {messages.map(
                        (message, index) => (

                          <div
                            key={index}
                            className={
                              message.role === "user"
                                ? "flex justify-end"
                                : "flex justify-start"
                            }
                          >

                            <div
                              className={
                                message.role === "user"
                                  ? "max-w-[78%] rounded-2xl rounded-br-md bg-cyan-600 text-white px-4 py-3"
                                  : "max-w-[82%] rounded-2xl rounded-bl-md bg-slate-50 border border-slate-200 px-4 py-3"
                              }
                            >

                              {/* Message Label */}
                              <div
                                className={
                                  message.role === "user"
                                    ? "mb-1 text-[8px] font-bold uppercase text-cyan-100"
                                    : "mb-1 text-[8px] font-bold uppercase text-cyan-700"
                                }
                              >
                                {message.role === "user"
                                  ? "YOU"
                                  : "AUTOMIND AI"}
                              </div>

                              {/* Message Content */}
                              <div className="whitespace-pre-wrap text-sm leading-6">

                                {message.content}

                                {loading &&
                                  index === messages.length - 1 &&
                                  message.role === "user" && (

                                    <span className="ml-1 animate-pulse">
                                      ▋
                                    </span>

                                  )}

                              </div>

                              {/* ================================================= */}
                              {/* SOURCES */}
                              {/* ================================================= */}

                              {message.role === "assistant" &&
                                message.sources &&
                                message.sources.length > 0 && (

                                  <div className="mt-3 pt-2 border-t border-slate-200">

                                    <p className="text-[9px] font-bold text-slate-600 mb-1.5">
                                      Retrieved Sources
                                    </p>

                                    <div className="space-y-1">

                                      {Array.from(
                                        new Map(
                                          message.sources.map(
                                            (source) => [
                                              source.filename,
                                              source,
                                            ]
                                          )
                                        ).values()
                                      )
                                        .slice(0, 2)
                                        .map(
                                          (source, sourceIndex) => (

                                            <div
                                              key={`${source.filename}-${sourceIndex}`}
                                              className="bg-white border border-slate-200 rounded-lg px-2.5 py-1.5"
                                            >

                                              <p className="text-[9px] font-semibold text-slate-700 truncate">
                                                📄 {source.filename}
                                              </p>

                                              <p className="text-[8px] text-slate-400">
                                                Chunk{" "}
                                                {source.chunk_id ??
                                                  "N/A"}
                                                {" · "}
                                                Relevance{" "}
                                                {Number(
                                                  source.score
                                                ).toFixed(3)}
                                              </p>

                                            </div>

                                          )
                                        )}

                                    </div>

                                  </div>

                                )}

                            </div>

                          </div>

                        )
                      )}

                    </div>

                  )}

                </div>

                {/* ================================================= */}
                {/* INPUT */}
                {/* ================================================= */}

                <div className="border-t border-slate-100 bg-slate-50 p-3">

                  <div className="flex gap-2 items-end">

                    <textarea
                      value={question}
                      onChange={(event) =>
                        setQuestion(event.target.value)
                      }
                      onKeyDown={handleKeyDown}
                      placeholder="Ask an automotive engineering question..."
                      rows={2}
                      disabled={loading}
                      className="flex-1 resize-none rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm outline-none focus:border-cyan-400 focus:ring-2 focus:ring-cyan-100 disabled:opacity-50"
                    />

                    <button
                      onClick={sendMessage}
                      disabled={
                        loading ||
                        !question.trim()
                      }
                      className="h-[46px] px-5 rounded-xl bg-cyan-600 hover:bg-cyan-700 text-white text-sm font-semibold transition disabled:bg-slate-300 disabled:cursor-not-allowed"
                    >
                      {loading
                        ? "..."
                        : "Send →"}
                    </button>

                  </div>

                  <p className="mt-1 text-[8px] text-slate-400">
                    Enter to send · Shift + Enter for new line
                  </p>

                </div>

              </section>

              {/* ================================================= */}
              {/* SIDEBAR */}
              {/* ================================================= */}

              <aside className="space-y-3">

                {/* Knowledge Pipeline */}
                <div className="bg-white rounded-xl p-4 shadow-lg">

                  <h3 className="text-sm font-bold">
                    Knowledge Pipeline
                  </h3>

                  <p className="text-[9px] text-slate-400 mt-1">
                    How AutoMind processes your question.
                  </p>

                  <div className="mt-3 space-y-2.5">

                    {[
                      ["01", "Question", "User query"],
                      ["02", "Retrieve", "Qdrant search"],
                      ["03", "Context", "Relevant chunks"],
                      ["04", "Generate", "Grounded AI"],
                    ].map(
                      ([
                        number,
                        title,
                        description,
                      ]) => (

                        <div
                          key={number}
                          className="flex items-center gap-2"
                        >

                          <div className="h-7 w-7 rounded-lg bg-cyan-50 text-cyan-700 flex items-center justify-center text-[9px] font-bold">
                            {number}
                          </div>

                          <div>

                            <p className="text-[10px] font-semibold">
                              {title}
                            </p>

                            <p className="text-[8px] text-slate-400">
                              {description}
                            </p>

                          </div>

                        </div>

                      )
                    )}

                  </div>

                </div>

                {/* Automotive AI Card */}
                <div className="bg-slate-900 rounded-xl p-4 text-white shadow-lg">

                  <p className="text-[8px] tracking-widest text-cyan-400 font-bold">
                    AUTOMOTIVE AI
                  </p>

                  <h3 className="text-sm font-bold mt-2 leading-5">

                    Engineering knowledge,

                    <span className="block text-cyan-300">
                      one question away.
                    </span>

                  </h3>

                  <p className="text-[9px] text-slate-400 leading-4 mt-2">
                    Retrieve technical information from uploaded
                    documents instead of relying on unsupported answers.
                  </p>

                  <div className="mt-3 pt-2 border-t border-slate-700 flex justify-between">

                    <span className="text-[8px] text-slate-500">
                      VECTOR DATABASE
                    </span>

                    <span className="text-[8px] text-green-400 font-bold">
                      READY
                    </span>

                  </div>

                </div>

              </aside>

            </div>

          </div>

        </div>

      </main>

    </div>
  );
}

export default Chat;