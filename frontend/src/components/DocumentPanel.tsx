/**
 * DraftMate AI: Document Management Side Panel Component
 * Supports MarkItDown conversion, sample matters, templates, and style adaptation toggle.
 */

import React, { useState } from 'react';
import { Files, X, FileText, File, Sparkles } from 'lucide-react';

interface DocumentItem {
  name: string;
  sample_file: string;
  type: string;
  category: string;
  size: string;
  date: string;
}

interface DocumentPanelProps {
  isOpen: boolean;
  onClose: () => void;
  documents: DocumentItem[];
  onAddSelected: (selectedDocs: DocumentItem[], adaptStyle: boolean) => void;
}

export const DocumentPanel: React.FC<DocumentPanelProps> = ({
  isOpen,
  onClose,
  documents,
  onAddSelected
}) => {
  const [activeCategory, setActiveCategory] = useState<string>('all');
  const [selected, setSelected] = useState<DocumentItem[]>([]);
  const [adaptStyle, setAdaptStyle] = useState<boolean>(false);

  if (!isOpen) return null;

  const filteredDocs = activeCategory === 'all' 
    ? documents 
    : documents.filter(d => d.category.toLowerCase().includes(activeCategory.toLowerCase()));

  const toggleSelect = (doc: DocumentItem) => {
    if (selected.some(s => s.name === doc.name)) {
      setSelected(selected.filter(s => s.name !== doc.name));
    } else {
      setSelected([...selected, doc]);
    }
  };

  return (
    <aside className="w-80 bg-white border-l border-slate-200 flex flex-col shrink-0 shadow-lg h-full z-40">
      <div className="p-4 border-b border-slate-200 flex items-center justify-between bg-slate-50">
        <div className="flex items-center space-x-2">
          <Files className="w-4 h-4 text-blue-600" />
          <h2 className="text-xs font-bold text-slate-800 uppercase tracking-wider">DraftMate Documents</h2>
        </div>
        <button onClick={onClose} className="text-slate-400 hover:text-slate-600 p-1 rounded">
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Categories Tabs */}
      <div className="px-3 pt-2 border-b border-slate-100 text-xs flex space-x-1 overflow-x-auto">
        {['all', 'Active Matters', 'Templates', 'Shared with Me'].map(cat => (
          <button
            key={cat}
            onClick={() => setActiveCategory(cat)}
            className={`px-2.5 py-1.5 capitalize ${activeCategory === cat ? 'font-bold text-blue-600 border-b-2 border-blue-600' : 'text-slate-500 hover:text-slate-700'}`}
          >
            {cat === 'all' ? 'All' : cat.split(' ')[0]}
          </button>
        ))}
      </div>

      {/* Document List */}
      <div className="flex-1 overflow-y-auto p-3 space-y-2 text-xs">
        {filteredDocs.map(d => {
          const isChecked = selected.some(s => s.name === d.name);
          return (
            <div 
              key={d.name}
              className={`p-2.5 rounded-xl border transition flex items-start space-x-2.5 ${isChecked ? 'border-blue-400 bg-blue-50/30' : 'border-slate-200 bg-white hover:border-slate-300'}`}
            >
              <input 
                type="checkbox" 
                checked={isChecked}
                onChange={() => toggleSelect(d)}
                className="mt-1 rounded text-blue-600 focus:ring-0" 
              />
              <div className="flex-1 min-w-0">
                <div className="flex items-center space-x-1.5">
                  {d.name.endsWith('.pdf') ? <FileText className="w-3.5 h-3.5 text-blue-600 shrink-0" /> : <File className="w-3.5 h-3.5 text-blue-600 shrink-0" />}
                  <span className="font-semibold text-slate-800 truncate" title={d.name}>{d.name}</span>
                </div>
                <div className="flex items-center space-x-2 text-[10px] text-slate-400 mt-1">
                  <span className="bg-slate-100 text-slate-600 px-1 rounded">{d.type}</span>
                  <span>{d.size}</span>
                  <span>&bull;</span>
                  <span>{d.date}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Panel Footer */}
      <div className="p-3 border-t border-slate-200 bg-slate-50 space-y-2">
        <label className="flex items-center space-x-1.5 cursor-pointer text-[11px] text-slate-600">
          <input 
            type="checkbox" 
            checked={adaptStyle}
            onChange={(e) => setAdaptStyle(e.target.checked)}
            className="rounded text-blue-600 focus:ring-0" 
          />
          <span>Learn & Adapt Drafting Style</span>
        </label>

        <div className="flex items-center space-x-2">
          <button 
            disabled={selected.length === 0}
            onClick={() => {
              onAddSelected(selected, adaptStyle);
              setSelected([]);
            }}
            className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-1.5 rounded-lg text-xs transition shadow-xs disabled:opacity-50"
          >
            Add Selected ({selected.length})
          </button>
          <button 
            onClick={() => setSelected([])} 
            className="bg-slate-200 hover:bg-slate-300 text-slate-700 py-1.5 px-3 rounded-lg text-xs font-medium transition"
          >
            Clear
          </button>
        </div>
      </div>
    </aside>
  );
};
