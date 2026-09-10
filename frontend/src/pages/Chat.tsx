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

function Chat() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  // =====================================================
  // Persistent LangGraph thread ID
  // =====================================================

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

  // =====================================================
  // Send message
  // =====================================================

  async function sendMessage() {
    const trimmed = question.trim();

    if (!trimmed || loading) {
      return;
    }

    // ===================================================
    // Add user message
    // ===================================================

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: trimmed,
      },
    ]);

    setQuestion("");
    setLoading(true);

    // ===================================================
    // Add empty assistant message
    // ===================================================

    setMessages((prev) => [
      ...prev,
      {
        role: "assistant",
        content: "",
        sources: [],
      },
    ]);

    try {
      // =================================================
      // Call V2 streaming endpoint
      // =================================================

      const response = await fetch(
        `${BASE_URL}/api/v2/chat/stream`,
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

      if (!response.body) {
        throw new Error(
          "Streaming response body is unavailable."
        );
      }

      // =================================================
      // Read NDJSON stream
      // =================================================

      const reader =
        response.body.getReader();

      const decoder =
        new TextDecoder();

      let buffer = "";

      while (true) {
        const { value, done } =
          await reader.read();

        if (done) {
          break;
        }

        buffer += decoder.decode(
          value,
          {
            stream: true,
          }
        );

        const lines =
          buffer.split("\n");

        // Keep incomplete line
        buffer =
          lines.pop() || "";

        for (const line of lines) {
          if (!line.trim()) {
            continue;
          }

          processStreamEvent(line);
        }
      }

      // =================================================
      // Process remaining buffered data
      // =================================================

      buffer += decoder.decode();

      if (buffer.trim()) {
        processStreamEvent(buffer);
      }

    } catch (error) {
      console.error(
        "Streaming chat error:",
        error
      );

      setMessages((prev) => {
        const updated = [...prev];

        const lastIndex =
          updated.length - 1;

        if (
          updated[lastIndex] &&
          updated[lastIndex].role ===
            "assistant"
        ) {
          updated[lastIndex] = {
            ...updated[lastIndex],
            content:
              "Sorry, something went wrong while contacting AutoMind AI.",
          };
        }

        return updated;
      });

    } finally {
      setLoading(false);
    }
  }

  // =====================================================
  // Process one NDJSON event
  // =====================================================

  function processStreamEvent(
    line: string
  ) {
    try {
      const event =
        JSON.parse(line);

      // =================================================
      // Sources event
      // =================================================

      if (
        event.type === "sources"
      ) {
        const sources: Source[] =
          event.sources || [];

        setMessages((prev) => {
          const updated = [...prev];

          const lastIndex =
            updated.length - 1;

          if (
            updated[lastIndex] &&
            updated[lastIndex].role ===
              "assistant"
          ) {
            updated[lastIndex] = {
              ...updated[lastIndex],
              sources,
            };
          }

          return updated;
        });

        return;
      }

      // =================================================
      // Token event
      // =================================================

      if (
        event.type === "token"
      ) {
        const token =
          event.content || "";

        if (!token) {
          return;
        }

        setMessages((prev) => {
          const updated = [...prev];

          const lastIndex =
            updated.length - 1;

          if (
            updated[lastIndex] &&
            updated[lastIndex].role ===
              "assistant"
          ) {
            updated[lastIndex] = {
              ...updated[lastIndex],
              content:
                updated[lastIndex].content +
                token,
            };
          }

          return updated;
        });

        return;
      }

      // =================================================
      // Done event
      // =================================================

      if (
        event.type === "done"
      ) {
        return;
      }

      // =================================================
      // Error event
      // =================================================

      if (
        event.type === "error"
      ) {
        const errorMessage =
          event.content ||
          "AutoMind AI failed to generate the response.";

        setMessages((prev) => {
          const updated = [...prev];

          const lastIndex =
            updated.length - 1;

          if (
            updated[lastIndex] &&
            updated[lastIndex].role ===
              "assistant"
          ) {
            updated[lastIndex] = {
              ...updated[lastIndex],
              content: errorMessage,
            };
          }

          return updated;
        });

        return;
      }

    } catch (parseError) {
      console.error(
        "Stream JSON parse error:",
        parseError
      );
    }
  }

  // =====================================================
  // Enter key handling
  // =====================================================

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

  // =====================================================
  // UI
  // =====================================================

  return (
    <div className="min-h-screen bg-slate-950 text-white">

      <Navbar />

      <div className="mx-auto flex max-w-5xl flex-col px-6 py-10">

        {/* =================================================
            Header
        ================================================= */}

        <div className="mb-8">

          <h1 className="text-4xl font-bold text-cyan-400">
            AutoMind AI
          </h1>

          <p className="mt-2 text-slate-400">
            Ask questions about your uploaded documents.
          </p>

        </div>

        {/* =================================================
            Chat Area
        ================================================= */}

        <div className="min-h-[500px] rounded-2xl border border-slate-800 bg-slate-900/70 p-6">

          <div className="space-y-5">

            {/* =================================================
                Empty State
            ================================================= */}

            {messages.length === 0 && (
              <div className="flex min-h-[400px] items-center justify-center text-center text-slate-500">

                <div>

                  <p className="text-xl">
                    Ask AutoMind AI something.
                  </p>

                  <p className="mt-2 text-sm">
                    Try: "What is the maximum CAN bus length at 1 Mbit/s?"
                  </p>

                </div>

              </div>
            )}

            {/* =================================================
                Messages
            ================================================= */}

            {messages.map(
              (message, index) => (
                <div
                  key={index}
                  className={
                    message.role === "user"
                      ? "ml-auto max-w-[80%] rounded-2xl bg-cyan-500/20 p-4"
                      : "mr-auto max-w-[80%] rounded-2xl bg-slate-800 p-4"
                  }
                >

                  {/* Message role */}

                  <div className="mb-1 text-xs font-semibold uppercase text-slate-400">

                    {message.role === "user"
                      ? "You"
                      : "AutoMind AI"}

                  </div>

                  {/* Message content */}

                  <div className="whitespace-pre-wrap leading-7">

                    {message.content}

                    {message.role === "assistant" &&
                      loading &&
                      index ===
                        messages.length - 1 && (
                        <span className="ml-1 animate-pulse">
                          ▋
                        </span>
                      )}

                  </div>

                  {/* =================================================
                      Sources
                  ================================================= */}

                  {message.role === "assistant" &&
                    message.sources &&
                    message.sources.length > 0 && (

                    <div className="mt-4 border-t border-slate-700 pt-3">

                      <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-cyan-400">
                        Sources
                      </div>

                      <div className="space-y-2">

                        {message.sources.map(
                          (
                            source,
                            sourceIndex
                          ) => (

                            <div
                              key={`${source.filename}-${source.chunk_id}-${sourceIndex}`}
                              className="rounded-lg bg-slate-900/70 px-3 py-2 text-sm"
                            >

                              <div className="font-medium text-slate-200">

                                📄{" "}
                                {source.filename}

                              </div>

                              <div className="mt-1 text-xs text-slate-500">

                                Chunk{" "}
                                {source.chunk_id ??
                                  "N/A"}

                                {" · "}

                                Score{" "}

                                {Number(
                                  source.score
                                ).toFixed(3)}

                              </div>

                            </div>

                          )
                        )}

                      </div>

                    </div>

                  )}

                </div>
              )
            )}

          </div>

        </div>

        {/* =================================================
            Input
        ================================================= */}

        <div className="mt-5 flex gap-3">

          <textarea
            value={question}
            onChange={(event) =>
              setQuestion(
                event.target.value
              )
            }
            onKeyDown={handleKeyDown}
            placeholder="Ask something..."
            rows={2}
            disabled={loading}
            className="flex-1 resize-none rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-white outline-none focus:border-cyan-400 disabled:opacity-50"
          />

          <button
            onClick={sendMessage}
            disabled={
              loading ||
              !question.trim()
            }
            className="rounded-xl bg-cyan-500 px-6 font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-40"
          >

            {loading
              ? "Thinking..."
              : "Send"}

          </button>

        </div>

      </div>

    </div>
  );
}

export default Chat;