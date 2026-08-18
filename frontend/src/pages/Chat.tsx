import { useState } from "react";
import Navbar from "../components/Navbar";

const BASE_URL = "http://127.0.0.1:8000";

type Message = {
  role: "user" | "assistant";
  content: string;
};

function Chat() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const threadId = "frontend-chat-v1";

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
      const response = await fetch(`${BASE_URL}/api/v2/chat/stream`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: trimmed,
          thread_id: threadId,
        }),
      });

      if (!response.ok) {
        throw new Error("Chat request failed");
      }

      if (!response.body) {
        throw new Error("Streaming response is unavailable");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let answer = "";

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "",
        },
      ]);

      while (true) {
        const { value, done } = await reader.read();

        if (done) {
          break;
        }

        const chunk = decoder.decode(value, {
          stream: true,
        });

        answer += chunk;

        setMessages((prev) => {
          const updated = [...prev];

          const lastIndex = updated.length - 1;

          if (
            lastIndex >= 0 &&
            updated[lastIndex].role === "assistant"
          ) {
            updated[lastIndex] = {
              role: "assistant",
              content: answer,
            };
          }

          return updated;
        });
      }
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, something went wrong while contacting AutoMind AI.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(
    event: React.KeyboardEvent<HTMLTextAreaElement>
  ) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <Navbar />

      <div className="mx-auto flex max-w-5xl flex-col px-6 py-10">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-cyan-400">
            AutoMind AI
          </h1>

          <p className="mt-2 text-slate-400">
            Ask questions about your uploaded documents.
          </p>
        </div>

        <div className="min-h-[500px] rounded-2xl border border-slate-800 bg-slate-900/70 p-6">
          <div className="space-y-5">
            {messages.length === 0 && (
              <div className="flex min-h-[400px] items-center justify-center text-center text-slate-500">
                <div>
                  <p className="text-xl">
                    Ask AutoMind AI something.
                  </p>

                  <p className="mt-2 text-sm">
                    Try: "What projects has Mukesh worked on?"
                  </p>
                </div>
              </div>
            )}

            {messages.map((message, index) => (
              <div
                key={index}
                className={
                  message.role === "user"
                    ? "ml-auto max-w-[80%] rounded-2xl bg-cyan-500/20 p-4"
                    : "mr-auto max-w-[80%] rounded-2xl bg-slate-800 p-4"
                }
              >
                <div className="mb-1 text-xs font-semibold uppercase text-slate-400">
                  {message.role === "user" ? "You" : "AutoMind AI"}
                </div>

                <div className="whitespace-pre-wrap leading-7">
                  {message.content}
                </div>
              </div>
            ))}

            {loading && (
              <div className="text-sm text-slate-500">
                AutoMind AI is thinking...
              </div>
            )}
          </div>
        </div>

        <div className="mt-5 flex gap-3">
          <textarea
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask something..."
            rows={2}
            className="flex-1 resize-none rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-white outline-none focus:border-cyan-400"
          />

          <button
            onClick={sendMessage}
            disabled={loading || !question.trim()}
            className="rounded-xl bg-cyan-500 px-6 font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-40"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default Chat;