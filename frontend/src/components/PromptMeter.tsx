/**
 * DraftMate AI: Prompt Enhancement & Prompt Meter Component
 * Shows real-time prompt strength percentage, legal advice tip, and "+ Improve Prompt" action.
 */

import React from 'react';
import { Sparkles } from 'lucide-react';

interface PromptMeterProps {
  score: number;
  tip: string;
  onImprovePrompt: () => void;
  isLoading?: boolean;
}

export const PromptMeter: React.FC<PromptMeterProps> = ({
  score,
  tip,
  onImprovePrompt,
  isLoading
}) => {
  const getColorClasses = () => {
    if (score >= 80) return { text: 'text-emerald-600', bar: 'bg-emerald-600' };
    if (score >= 50) return { text: 'text-blue-600', bar: 'bg-blue-600' };
    return { text: 'text-amber-600', bar: 'bg-amber-500' };
  };

  const { text, bar } = getColorClasses();

  return (
    <div className="bg-gradient-to-r from-blue-50/50 via-slate-50 to-indigo-50/50 border border-slate-200/80 rounded-xl p-3.5 shadow-xs flex flex-col md:flex-row items-start md:items-center justify-between gap-3 text-xs">
      <div className="flex-1">
        <div className="flex items-center space-x-2">
          <span className="font-bold text-slate-700">Prompt Strength:</span>
          <span className={`font-extrabold ${text}`}>{score}%</span>
          <div className="w-32 bg-slate-200 rounded-full h-2 overflow-hidden ml-2">
            <div 
              className={`${bar} h-2 rounded-full transition-all duration-300`} 
              style={{ width: `${score}%` }} 
            />
          </div>
        </div>
        <p className="text-slate-500 text-[11px] mt-1 leading-normal">
          {tip || 'Tip: Add the purpose, jurisdiction and specific requirements to get a more accurate response.'}
        </p>
      </div>

      <button 
        onClick={onImprovePrompt} 
        disabled={isLoading}
        className="shrink-0 flex items-center space-x-1.5 bg-white hover:bg-blue-50 border border-blue-200 text-blue-700 font-semibold px-3 py-1.5 rounded-lg shadow-xs transition hover:border-blue-300 disabled:opacity-50"
      >
        <Sparkles className="w-3.5 h-3.5 text-blue-600" />
        <span>+ Improve Prompt</span>
      </button>
    </div>
  );
};
