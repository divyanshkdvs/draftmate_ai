/**
 * Hiromi Higuruma Interactive Character Companion Component
 * Executive Editorial Theme: Deep Navy (#1C2541), Cream (#F4F1EA), Warm Copper (#9A5B32)
 */

import React, { useState } from 'react';
import { X } from 'lucide-react';

interface HigurumaCompanionProps {
  isOpen: boolean;
  onClose: () => void;
  activeDraftText?: string;
  onApplyRecommendation: (recommendationText: string) => void;
}

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  recommendation?: string;
}

export const HigurumaCompanion: React.FC<HigurumaCompanionProps> = ({
  isOpen,
  onClose,
  activeDraftText,
  onApplyRecommendation
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: 'assistant',
      content: "*(Adjusts cuff, placing gavel on the docket)*\n\nI am listening. Whether you need to cross-examine a counterparty's clause, identify hidden liabilities in an indemnity provision, or formulate an ironclad courtroom defense—tell me what evidence or draft we are dealing with."
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  if (!isOpen) return null;

  const handleSend = async (messageToSend?: string) => {
    const text = messageToSend || inputMessage;
    if (!text.trim() || isLoading) return;

    const newHistory = [...messages, { role: 'user' as const, content: text }];
    setMessages(newHistory);
    setInputMessage('');
    setIsLoading(true);

    try {
      const res = await fetch('/api/higuruma/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          active_draft: activeDraftText,
          chat_history: newHistory.map(m => ({ role: m.role, content: m.content }))
        })
      });
      const data = await res.json();
      setMessages([
        ...newHistory,
        {
          role: 'assistant',
          content: data.response,
          recommendation: data.tactical_recommendation
        }
      ]);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <aside className="fixed inset-y-0 right-0 w-full max-w-lg bg-[#1C2541] text-[#F4F1EA] border-l border-[#9A5B32] flex flex-col shadow-2xl z-50 transition-all font-sans">
      {/* Header */}
      <div className="p-6 bg-[#111827] border-b border-[#9A5B32]/50 flex items-center justify-between">
        <div className="flex items-center space-x-3.5">
          <div className="w-12 h-12 rounded-[3px] bg-[#1C2541] border border-[#9A5B32] flex items-center justify-center text-xl text-[#9A5B32]">
            ⚖️
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="font-serif text-lg font-semibold text-[#F4F1EA] tracking-wide">Chamber of Hiromi Higuruma</h3>
              <span className="text-[9px] bg-[#9A5B32]/20 text-[#9A5B32] border border-[#9A5B32]/40 px-1.5 py-0.2 rounded font-mono font-bold">COUNSEL</span>
            </div>
            <p className="text-[11px] text-[#F4F1EA]/70">Master of Deadly Sentencing (誅伏賜死) &bull; Defense Advocate</p>
          </div>
        </div>
        <button onClick={onClose} className="text-[#F4F1EA]/60 hover:text-[#F4F1EA] p-1.5">
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Motto */}
      <div className="px-6 py-3 bg-[#1C2541] border-b border-[#9A5B32]/30 text-[11px] text-[#F4F1EA]/80 italic font-serif">
        "The law is not a tool to blind people; it is a scale that must balance truth with evidence. Cross-examine every covenant."
      </div>

      {/* Quick Tactical Scenarios */}
      <div className="p-4 bg-[#111827]/70 border-b border-[#9A5B32]/20 space-y-2">
        <div className="text-[10px] uppercase tracking-[0.2em] text-[#9A5B32] font-semibold">
          Evidentiary Cross-Examinations:
        </div>
        <div className="grid grid-cols-2 gap-2 text-[10px]">
          <button 
            onClick={() => handleSend("Cross-Examine Active Draft for loopholes")}
            className="bg-[#1C2541] hover:bg-[#273459] border border-[#9A5B32]/40 text-[#F4F1EA]/90 p-2 rounded-[3px] text-left transition-colors"
          >
            ⚖️ Cross-Examine Active Draft
          </button>
          <button 
            onClick={() => handleSend("Scrutinize Indemnity & Liability limits")}
            className="bg-[#1C2541] hover:bg-[#273459] border border-[#9A5B32]/40 text-[#F4F1EA]/90 p-2 rounded-[3px] text-left transition-colors"
          >
            🔍 Scrutinize Liability Limits
          </button>
          <button 
            onClick={() => handleSend("How do we defend against a breach of contract claim?")}
            className="bg-[#1C2541] hover:bg-[#273459] border border-[#9A5B32]/40 text-[#F4F1EA]/90 p-2 rounded-[3px] text-left transition-colors"
          >
            🛡️ Formulate Breach Defense
          </button>
          <button 
            onClick={() => handleSend("What does Judgeman think of this legal balance?")}
            className="bg-[#1C2541] hover:bg-[#273459] border border-[#9A5B32]/40 text-[#F4F1EA]/90 p-2 rounded-[3px] text-left transition-colors"
          >
            🏛️ Courtroom Philosophy
          </button>
        </div>
      </div>

      {/* Chat Thread */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4 text-xs select-text">
        {messages.map((m, idx) => (
          <div 
            key={idx}
            className={`p-4 rounded-[4px] border leading-relaxed ${
              m.role === 'user' 
                ? 'bg-[#273459]/90 border-[#9A5B32]/30 ml-8 text-[#F4F1EA]' 
                : 'bg-[#111827] border-[#9A5B32]/50 mr-3 text-[#F4F1EA]/90'
            }`}
          >
            <div className="flex items-center space-x-2 text-[#9A5B32] font-serif font-semibold text-sm border-b border-[#9A5B32]/30 pb-1.5 mb-2">
              <span>{m.role === 'user' ? 'Counselor Inquiry:' : '⚖️ Hiromi Higuruma:'}</span>
            </div>
            <div className="whitespace-pre-wrap">{m.content}</div>
            
            {m.recommendation && (
              <div className="mt-3 pt-2.5 border-t border-[#9A5B32]/30 flex items-center justify-between">
                <span className="text-[10px] text-amber-200/80 font-serif italic">Remedial clause formulated.</span>
                <button 
                  onClick={() => onApplyRecommendation(m.recommendation!)}
                  className="bg-[#9A5B32] hover:bg-[#844C27] text-white font-semibold px-3 py-1 rounded-[3px] text-[10px] uppercase tracking-wider transition-colors"
                >
                  Incorporate into Studio
                </button>
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="p-4 bg-[#111827] border border-[#9A5B32]/20 rounded-[4px] text-[#F4F1EA]/70 text-xs italic animate-pulse">
            Higuruma is weighing the evidentiary burden against statutory provisions...
          </div>
        )}
      </div>

      {/* Input */}
      <div className="p-4 bg-[#111827] border-t border-[#9A5B32]/40">
        <div className="flex space-x-2">
          <input 
            type="text" 
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Consult Higuruma on clause vulnerabilities, strategy..."
            className="flex-1 bg-[#1C2541] border border-[#9A5B32]/40 focus:border-[#9A5B32] rounded-[4px] px-3.5 py-2.5 text-xs text-[#F4F1EA] outline-none placeholder:text-[#F4F1EA]/40"
          />
          <button 
            onClick={() => handleSend()}
            className="bg-[#9A5B32] hover:bg-[#844C27] text-white px-5 py-2.5 rounded-[4px] font-semibold text-[11px] uppercase tracking-wider transition-colors"
          >
            Inquire
          </button>
        </div>
      </div>
    </aside>
  );
};
