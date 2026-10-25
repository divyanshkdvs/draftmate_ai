/**
 * DraftMate AI: Legal Drafting Studio - Sidebar Navigation Component
 * Modeled after reference layout: Home, Drafter, Matters, Documents, Skills Library, etc.
 */

import React from 'react';
import { 
  Home, 
  FileEdit, 
  Search, 
  Briefcase, 
  Files, 
  MessageSquare, 
  Sparkles, 
  LayoutTemplate, 
  ShieldCheck, 
  Landmark, 
  Cpu, 
  Settings 
} from 'lucide-react';

interface SidebarProps {
  activeView: string;
  onSelectView: (view: string) => void;
  onOpenSkills: () => void;
  onToggleDocs: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeView,
  onSelectView,
  onOpenSkills,
  onToggleDocs
}) => {
  return (
    <aside className="w-60 bg-white border-r border-slate-200 flex flex-col shrink-0 select-none h-full">
      <div className="p-3 space-y-1 flex-1 overflow-y-auto">
        <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider px-3 py-1">
          Workspace
        </div>

        <button 
          onClick={() => onSelectView('home')} 
          className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-xs font-medium transition ${activeView === 'home' ? 'bg-blue-50 text-blue-700 font-semibold' : 'text-slate-600 hover:bg-slate-50'}`}
        >
          <Home className="w-4 h-4 text-slate-400" />
          <span>Home</span>
        </button>

        <button 
          onClick={() => onSelectView('drafter')} 
          className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-xs font-semibold transition ${activeView === 'drafter' ? 'bg-blue-50 text-blue-700 border border-blue-100 shadow-xs' : 'text-slate-600 hover:bg-slate-50'}`}
        >
          <FileEdit className="w-4 h-4 text-blue-600" />
          <span>Drafter</span>
        </button>

        <button 
          onClick={() => onSelectView('research')} 
          className="w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-50 transition"
        >
          <Search className="w-4 h-4 text-slate-400" />
          <span>Research</span>
        </button>

        <button 
          onClick={() => onSelectView('matters')} 
          className="w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-50 transition"
        >
          <Briefcase className="w-4 h-4 text-slate-400" />
          <span>Matters</span>
        </button>

        <button 
          onClick={onToggleDocs} 
          className="w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-50 transition"
        >
          <Files className="w-4 h-4 text-slate-400" />
          <span>Documents</span>
        </button>

        <button 
          onClick={() => onSelectView('conversations')} 
          className="w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-50 transition"
        >
          <MessageSquare className="w-4 h-4 text-slate-400" />
          <span>Conversations</span>
        </button>

        <div className="pt-3 pb-1">
          <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider px-3 py-1">
            Legal Intelligence
          </div>
        </div>

        <button 
          onClick={onOpenSkills} 
          className="w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-50 transition group"
        >
          <Sparkles className="w-4 h-4 text-indigo-500 group-hover:scale-110 transition-transform" />
          <span className="flex-1 text-left">Skills Library</span>
          <span className="bg-indigo-50 text-indigo-700 text-[10px] font-bold px-1.5 rounded">60+</span>
        </button>

        <button 
          onClick={() => onSelectView('templates')} 
          className="w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-50 transition"
        >
          <LayoutTemplate className="w-4 h-4 text-slate-400" />
          <span>Templates</span>
        </button>

        <button 
          onClick={() => onSelectView('compliance')} 
          className="w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-50 transition"
        >
          <ShieldCheck className="w-4 h-4 text-slate-400" />
          <span>Compliance</span>
        </button>

        <button 
          onClick={() => onSelectView('case-law')} 
          className="w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-50 transition"
        >
          <Landmark className="w-4 h-4 text-slate-400" />
          <span>Court & Case Law</span>
        </button>

        <button 
          onClick={() => onSelectView('ai-tools')} 
          className="w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-50 transition"
        >
          <Cpu className="w-4 h-4 text-slate-400" />
          <span>AI Tools</span>
        </button>
      </div>

      <div className="p-3 border-t border-slate-200">
        <button 
          onClick={() => onSelectView('settings')} 
          className="w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-50 transition"
        >
          <Settings className="w-4 h-4 text-slate-400" />
          <span>Settings</span>
        </button>
      </div>
    </aside>
  );
};
