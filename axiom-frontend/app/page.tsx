"use client";
import { useState } from "react";
import { Send, Bot, User, Loader2, FileText } from "lucide-react";

type Message = {
  role: "user" | "ai";
  text: string;
  sources?: { content: string; metadata?: any }[];
};

export default function ChatPage() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    setMessages((prev) => [...prev, { role: "user", text: query }]);

    try {
      const res = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      
      const data = await res.json();
      
      setMessages((prev) => [
        ...prev, 
        { role: "ai", text: data.answer, sources: data.sources }
      ]);
    } catch (err) {
      setMessages((prev) => [...prev, { role: "ai", text: "Error connecting to the Axiom Engine backend." }]);
    } finally {
      setQuery("");
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-slate-50">
      {/* Header */}
      <header className="p-5 bg-white border-b shadow-sm flex items-center justify-between">
        <h1 className="text-2xl font-bold text-slate-800 tracking-tight">Axiom Engine</h1>
      </header>

      {/* Chat History Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-slate-400 space-y-4">
            <Bot size={48} className="text-slate-300" />
            <p className="text-lg">What would you like to know from your documents?</p>
          </div>
        ) : (
          messages.map((m, i) => (
            <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
              <div className={`max-w-[80%] p-4 rounded-xl flex flex-col gap-2 shadow-sm ${
                m.role === "user" ? "bg-blue-600 text-white" : "bg-white border border-slate-200 text-slate-700"
              }`}>
                <div className="flex gap-4">
                  <div className="mt-1">
                    {m.role === "ai" ? <Bot size={20} className="text-blue-500" /> : <User size={20} className="text-blue-200" />}
                  </div>
                  <p className="leading-relaxed whitespace-pre-wrap">{m.text}</p>
                </div>

                {/* The Sources UI Section */}
                {m.sources && m.sources.length > 0 && (
                  <div className="ml-9 mt-3 pt-3 border-t border-slate-100">
                    <p className="text-xs font-semibold text-slate-400 mb-2 flex items-center gap-1 uppercase tracking-wider">
                      <FileText size={12} /> Sources Used
                    </p>
                    <div className="flex flex-col gap-2">
                      {m.sources.map((source, idx) => (
                        <details key={idx} className="group">
                          <summary className="text-xs text-blue-500 cursor-pointer hover:text-blue-700 list-none font-medium transition-colors">
                            ▶ View Source Document {idx + 1}
                          </summary>
                          <div className="mt-2 text-xs text-slate-600 bg-slate-50 p-3 rounded border border-slate-200 max-h-40 overflow-y-auto leading-relaxed">
                            {source.content}
                          </div>
                        </details>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))
        )}
      </div>

      {/* Input Bar */}
      <div className="p-4 bg-white border-t">
        <div className="max-w-4xl mx-auto flex gap-3">
          <input
            className="flex-1 p-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-slate-800 bg-slate-50 placeholder-slate-400 shadow-sm"
            placeholder="Ask your Axiom Engine anything..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            disabled={loading}
          />
          <button 
            onClick={handleSearch}
            disabled={loading || !query.trim()}
            className="bg-blue-600 text-white px-5 rounded-lg hover:bg-blue-700 disabled:bg-slate-300 disabled:cursor-not-allowed transition-colors shadow-sm flex items-center justify-center"
          >
            {loading ? <Loader2 className="animate-spin" size={20} /> : <Send size={20} />}
          </button>
        </div>
      </div>
    </div>
  );
}