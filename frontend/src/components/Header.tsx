/**
 * DraftMate AI: Header Component with Model Selector & Voice Agent trigger
 */

import React, { useState } from 'react';
import { Scale, Mic, Folder, ChevronDown, Sparkles } from 'lucide-react';

interface ModelOption {
  id: string;
  name: string;
  badge: string;
  description: string;
}

interface HeaderProps {
  activeModel: string;
  models: ModelOption[];
  onSelectModel: (modelId: string) => void;
  onOpenVoice: () => void;
  onToggleDocs: () => void;
  attachedDocsCount: number;
}

export const Header: React.FC<HeaderProps> = ({
  activeModel,
  models,
  onSelectModel,
  onOpenVoice,
  onToggleDocs,
  attachedDocsCount
}) => {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const selectedModel = models.find(m => m.id === activeModel) || models[0];

  return (
    <header className="bg-white border-b border-slate-200 px-5 py-2.5 flex items-center justify-between z-30 shrink-0 shadow-sm">
      <div className="flex items-center space-x-3">
        <div className="w-9 h-9 rounded-lg bg-gradient-to-tr from-blue-700 to-indigo-600 flex items-center justify-center text-white shadow-md">
          <Scale className="w-5 h-5" />
        </div>
        <div>
          <div className="flex items-center space-x-2">
            <span className="font-bold text-lg text-slate-900 tracking-tight">DraftMate</span>
            <span className="bg-blue-50 text-blue-700 text-[10px] font-semibold px-2 py-0.5 rounded border border-blue-200 uppercase tracking-wider">Studio 2.0</span>
          </div>
          <p className="text-[11px] text-slate-500 font-medium leading-none">Your AI Assistant in Law</p>
        </div>
      </div>

      {/* Model Selection Dropdown */}
      <div className="relative">
        <button 
          onClick={() => setDropdownOpen(!dropdownOpen)} 
          className="flex items-center space-x-2.5 bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-700 px-3.5 py-1.5 rounded-lg text-xs font-medium transition shadow-sm"
        >
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <span className="font-semibold text-slate-800">{selectedModel?.name}</span>
          <span className="bg-indigo-50 text-indigo-700 text-[10px] px-1.5 py-0.2 rounded font-medium">
            {selectedModel?.badge}
          </span>
          <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
        </button>

        {dropdownOpen && (
          <div className="absolute top-full mt-1.5 left-1/2 -translate-x-1/2 w-80 bg-white border border-slate-200 rounded-xl shadow-xl p-2 z-50">
            <div className="px-2.5 py-1 text-[11px] font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-100 pb-1.5 mb-1">
              Select AI Drafting Engine
            </div>
            <div className="space-y-1">
              {models.map(m => (
                <button
                  key={m.id}
                  onClick={() => {
                    onSelectModel(m.id);
                    setDropdownOpen(false);
                  }}
                  className={`w-full text-left px-3 py-2 rounded-lg text-xs hover:bg-slate-50 transition flex items-center justify-between group ${activeModel === m.id ? 'bg-blue-50/70 text-blue-700' : 'text-slate-700'}`}
                >
                  <div>
                    <div className="font-semibold">{m.name}</div>
                    <div className="text-[10px] text-slate-400 leading-tight">{m.description}</div>
                  </div>
                  <span className={`text-[10px] px-1.5 py-0.5 rounded font-medium ${m.badge === 'Advanced' ? 'bg-indigo-50 text-indigo-700' : 'bg-emerald-50 text-emerald-700'}`}>
                    {m.badge}
                  </span>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="flex items-center space-x-3">
        <button 
          onClick={onOpenVoice} 
          className="flex items-center space-x-1.5 bg-gradient-to-r from-indigo-50 to-blue-50 hover:from-indigo-100 hover:to-blue-100 text-indigo-700 border border-indigo-200 px-3 py-1.5 rounded-lg text-xs font-medium transition shadow-sm group"
        >
          <Mic className="w-4 h-4 text-indigo-600 group-hover:scale-110 transition-transform" />
          <span>Voice Agent</span>
        </button>

        <button 
          onClick={onToggleDocs} 
          className="flex items-center space-x-1.5 bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-700 px-3 py-1.5 rounded-lg text-xs font-medium transition shadow-sm"
        >
          <Folder className="w-4 h-4 text-slate-500" />
          <span>Documents</span>
          {attachedDocsCount > 0 && (
            <span className="bg-blue-600 text-white text-[10px] px-1.5 py-0.2 rounded-full font-bold">
              {attachedDocsCount}
            </span>
          )}
        </button>

        <div className="w-8 h-8 rounded-full bg-slate-900 text-white flex items-center justify-center font-bold text-xs ring-2 ring-blue-500/20">
          SM
        </div>
      </div>
    </header>
  );
};
