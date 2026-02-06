import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Send,
  ShieldCheck,
  Zap,
  Search,
  Cloud,
  Sun,
  CloudRain,
  CloudLightning,
  Github,
  CheckCircle2,
  Clock,
  AlertCircle,
  Menu,
  ChevronRight,
  Database,
  Thermometer,
  Wind,
  Droplets,
  Plus
} from 'lucide-react';

const API_BASE = 'http://localhost:8000';

const WeatherCard = ({ data }) => {
  if (!data || data.status === 'failed') return null;

  const getIcon = (description) => {
    const desc = (description || "").toLowerCase();
    if (desc.includes('rain')) return <CloudRain className="text-[#ff006e]" size={32} />;
    if (desc.includes('clear') || desc.includes('sun')) return <Sun className="text-[#06d6a0]" size={32} />;
    if (desc.includes('storm') || desc.includes('bolt')) return <CloudLightning className="text-[#ff006e]" size={32} />;
    return <Cloud className="text-white" size={32} />;
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="glass p-6 flex flex-col gap-4 relative overflow-hidden group mt-4 mb-2 max-w-sm self-end border-[#9d4edd]/20"
      style={{ background: 'rgba(255, 255, 255, 0.03)' }}
    >
      <div className="flex justify-between items-start">
        <div>
          <h3 className="text-xl font-bold text-white">{data.city}</h3>
          <p className="text-[#adb5bd] text-xs uppercase tracking-widest font-semibold">{data.description || 'Current Condition'}</p>
        </div>
        {getIcon(data.description)}
      </div>

      <div className="flex items-center gap-6 mt-2">
        <div className="flex items-center gap-2">
          <Thermometer size={18} className="text-[#9d4edd]" />
          <span className="text-2xl font-bold text-white">{Math.round(data.temperature)}°C</span>
        </div>
        <div className="h-8 w-px bg-white/10" />
        <div className="flex flex-col">
          <div className="flex items-center gap-2 text-[#adb5bd]">
            <Droplets size={12} />
            <span className="text-[10px]">{data.humidity}% Humidity</span>
          </div>
          <div className="flex items-center gap-2 text-[#adb5bd]">
            <Wind size={12} />
            <span className="text-[10px]">{data.wind_speed} km/h Wind</span>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [activeStep, setActiveStep] = useState(0);
  const [integrityLogOpen, setIntegrityLogOpen] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const scrollRef = useRef(null);

  const handleNewChat = () => {
    setChatHistory([]);
    setResponse(null);
    setQuery('');
    setActiveStep(0);
  };

  const steps = [
    { id: 1, title: 'Planner', icon: Zap, color: '#9d4edd', desc: 'Designing logical flow' },
    { id: 2, title: 'Executor', icon: Search, color: '#ff006e', desc: 'Fetching verified data' },
    { id: 3, title: 'Verifier', icon: ShieldCheck, color: '#06d6a0', desc: 'Validating integrity' }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim() || loading) return;

    setLoading(true);
    setResponse(null);
    setActiveStep(1);

    try {
      setTimeout(() => setActiveStep(2), 1500);
      setTimeout(() => setActiveStep(3), 3500);

      const res = await fetch(`${API_BASE}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query,
          history: chatHistory.map(m => ({ role: m.role, content: m.content }))
        })
      });

      if (!res.ok) throw new Error('Failed to fetch response');

      const data = await res.json();
      setResponse(data);

      // Update history with both the user query and assistant response
      setChatHistory(prev => [
        ...prev,
        { role: 'user', content: query },
        { role: 'assistant', content: data.verified_output, weather: data.results?.find(r => r.step.tool === 'get_weather')?.output }
      ]);

      setActiveStep(0);
      setQuery('');
    } catch (err) {
      console.error(err);
      setActiveStep(0);
    } finally {
      setLoading(false);
    }
  };

  const weatherData = response?.results?.find(r => r.step.tool === 'get_weather')?.output;

  return (
    <div className="flex flex-col min-h-screen">
      {/* Header */}
      <header className="p-6 flex justify-between items-center glass m-4 mb-2">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#9d4edd] to-[#ff006e] flex items-center justify-center">
            <ShieldCheck className="text-white" size={24} />
          </div>
          <h1 className="text-xl font-bold tracking-tight">AssistOps <span className="gradient-text">AI Operations</span> Assistant</h1>
        </div>
        <div className="flex items-center gap-4">
          <button
            onClick={handleNewChat}
            className="flex items-center gap-2 text-sm font-medium hover:text-[#06d6a0] transition-colors"
          >
            <Plus size={18} />
            <span className="hidden sm:inline">New Chat</span>
          </button>
          <button
            onClick={() => setIntegrityLogOpen(!integrityLogOpen)}
            className="flex items-center gap-2 text-sm font-medium hover:text-[#ff006e] transition-colors"
          >
            <Database size={18} />
            <span className="hidden sm:inline">Integrity Log</span>
          </button>
        </div>
      </header>

      <main className="flex-1 flex flex-col md:flex-row p-4 gap-4 overflow-hidden">
        {/* Main Interaction Area */}
        <div className="flex-1 flex flex-col gap-4 overflow-hidden relative">

          {/* Progress Tracker */}
          <div className="flex justify-between px-4 py-2">
            {steps.map((step) => {
              const isActive = activeStep === step.id;
              const Icon = step.icon;

              return (
                <div key={step.id} className="flex flex-col items-center gap-2 flex-1">
                  <div
                    className={`w-12 h-12 rounded-2xl flex items-center justify-center transition-all duration-500 ${isActive ? 'scale-110 shadow-lg' : 'opacity-40 grayscale'
                      }`}
                    style={{
                      backgroundColor: isActive ? step.color + '22' : 'transparent',
                      border: `1px solid ${isActive ? step.color : 'rgba(255,255,255,0.1)'}`,
                      boxShadow: isActive ? `0 0 20px ${step.color}44` : 'none'
                    }}
                  >
                    <Icon size={20} color={isActive ? step.color : '#fff'} />
                  </div>
                  <span className={`text-xs font-semibold ${isActive ? 'opacity-100' : 'opacity-30'}`}>{step.title}</span>
                  {isActive && (
                    <motion.span
                      initial={{ opacity: 0, y: 5 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="text-[10px] text-zinc-500 text-center"
                    >
                      {step.desc}
                    </motion.span>
                  )}
                </div>
              );
            })}
          </div>

          <div className="flex-1 glass overflow-y-auto p-6 flex flex-col gap-6 scroll-smooth" ref={scrollRef}>
            <AnimatePresence>
              {chatHistory.length === 0 && !loading && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="flex-1 flex flex-col items-center justify-center text-center p-8"
                >
                  <div className="w-20 h-20 rounded-3xl bg-zinc-900 border border-zinc-800 flex items-center justify-center mb-6">
                    <Zap className="text-zinc-600" size={32} />
                  </div>
                  <h2 className="text-2xl font-semibold mb-2">How can I assist you today?</h2>
                  <p className="text-zinc-500 max-w-md">I can give weather-based event advice, research tech repos, and provide verified, empathy-driven operations assistance.</p>
                </motion.div>
              )}

              {chatHistory.map((msg, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`flex flex-col gap-4 ${msg.role === 'user' ? '' : 'items-end'}`}
                >
                  {msg.role === 'user' ? (
                    <div className="flex items-start gap-4">
                      <div className="w-8 h-8 rounded-lg bg-zinc-800 flex items-center justify-center flex-shrink-0">
                        <Zap size={16} className="text-[#9d4edd]" />
                      </div>
                      <div className="bg-zinc-900/50 p-4 rounded-2xl border border-zinc-800 max-w-[85%]">
                        <p className="text-sm italic text-zinc-400">"{msg.content}"</p>
                      </div>
                    </div>
                  ) : (
                    <div className="flex flex-col gap-2 items-end w-full">
                      <div className="flex items-start gap-4 flex-row-reverse w-full">
                        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#9d4edd] to-[#ff006e] flex items-center justify-center flex-shrink-0">
                          <ShieldCheck size={16} className="text-white" />
                        </div>
                        <div className="bg-gradient-to-br from-zinc-900 to-zinc-950 p-6 rounded-2xl border border-zinc-800 shadow-xl max-w-[85%]">
                          <div className="flex items-center gap-2 mb-3">
                            <CheckCircle2 size={14} className="text-[#06d6a0]" />
                            <span className="text-[10px] font-bold uppercase tracking-wider text-[#06d6a0]">Verified by Integrity Guard</span>
                          </div>
                          <div className="text-sm leading-relaxed whitespace-pre-wrap">
                            {msg.content}
                          </div>
                        </div>
                      </div>
                      {msg.weather && <WeatherCard data={msg.weather} />}
                    </div>
                  )}
                </motion.div>
              ))}

              {loading && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="flex items-center gap-3 p-4 rounded-2xl bg-zinc-900/50 self-start"
                >
                  <div className="flex gap-1">
                    <motion.div animate={{ scale: [1, 1.5, 1] }} transition={{ repeat: Infinity, duration: 1 }} className="w-1 h-1 rounded-full bg-[#9d4edd]" />
                    <motion.div animate={{ scale: [1, 1.5, 1] }} transition={{ repeat: Infinity, duration: 1, delay: 0.2 }} className="w-1 h-1 rounded-full bg-[#ff006e]" />
                    <motion.div animate={{ scale: [1, 1.5, 1] }} transition={{ repeat: Infinity, duration: 1, delay: 0.4 }} className="w-1 h-1 rounded-full bg-[#06d6a0]" />
                  </div>
                  <span className="text-xs text-zinc-400">Assistant is refining information...</span>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Input Area */}
          <form onSubmit={handleSubmit} className="p-2 glass flex items-center gap-2">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask anything... (e.g., 'Weather advice for a night in Mumbai')"
              className="flex-1 bg-transparent border-none outline-none p-4 text-sm"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !query.trim()}
              className="w-12 h-12 rounded-xl bg-gradient-to-br from-[#9d4edd] to-[#ff006e] flex items-center justify-center disabled:opacity-50 disabled:grayscale transition-all hover:scale-105 active:scale-95"
            >
              <Send size={20} className="text-white" />
            </button>
          </form>
        </div>

        {/* Integrity Log Sidebar */}
        <AnimatePresence>
          {integrityLogOpen && (
            <motion.div
              initial={{ width: 0, opacity: 0 }}
              animate={{ width: 320, opacity: 1 }}
              exit={{ width: 0, opacity: 0 }}
              className="glass overflow-hidden flex flex-col"
            >
              <div className="p-4 border-b border-zinc-800 flex justify-between items-center">
                <div className="flex items-center gap-2">
                  <Database size={16} className="text-[#06d6a0]" />
                  <span className="text-sm font-bold tracking-tight uppercase">Integrity Log</span>
                </div>
              </div>

              <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-4">
                {!response && (
                  <div className="flex-1 flex flex-col items-center justify-center text-center p-6 opacity-30">
                    <AlertCircle size={32} className="mb-4" />
                    <p className="text-xs">No active logs. Execute a task to see verification data.</p>
                  </div>
                )}

                {response && response.results.map((res, i) => (
                  <div key={i} className="bg-zinc-900/80 rounded-xl p-3 border border-zinc-800">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-[10px] font-bold text-[#ff006e]">{res.step.tool}</span>
                      <span className={`text-[8px] px-1.5 py-0.5 rounded-full ${res.status === 'success' ? 'bg-[#06d6a022] text-[#06d6a0]' : 'bg-red-900/20 text-red-500'}`}>
                        {res.status.toUpperCase()}
                      </span>
                    </div>
                    <p className="text-[10px] text-zinc-400 mb-2">{res.step.reason}</p>
                    <pre className="text-[9px] bg-black/40 p-2 rounded-lg overflow-x-auto text-zinc-300 font-mono">
                      {JSON.stringify(res.output, null, 2)}
                    </pre>
                  </div>
                ))}
              </div>

              <div className="p-4 border-t border-zinc-800 bg-zinc-900/50">
                <div className="flex items-center gap-2 mb-1">
                  <ShieldCheck size={12} className="text-[#06d6a0]" />
                  <span className="text-[9px] font-bold text-zinc-300">High-Trust Proof</span>
                </div>
                <p className="text-[8px] text-zinc-500">Every response is cross-referenced with these raw API logs to ensure zero hallucinations.</p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {/* Footer */}
      <footer className="p-6 text-center text-[10px] text-zinc-600 font-medium">
        &copy; 2026 ASSISTOPS AI OPERATIONS ASSISTANT &bull; POWERED BY GEMINI 2.0 FLASH &bull; HIGH-TRUST EDITION
      </footer>
    </div>
  );
}

export default App;
