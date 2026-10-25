/**
 * DraftMate AI: Voice Agent Modal Component
 * References: OpenWhispr & VoxCPM
 */

import React from 'react';
import { Mic, X } from 'lucide-react';

interface VoiceAgentModalProps {
  isOpen: boolean;
  onClose: () => void;
  isRecording: boolean;
  transcript: string;
  onToggleRecording: () => void;
  onSimulatePhrase: (phrase: string) => void;
}

export const VoiceAgentModal: React.FC<VoiceAgentModalProps> = ({
  isOpen,
  onClose,
  isRecording,
  transcript,
  onToggleRecording,
  onSimulatePhrase
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6 text-center border border-slate-200 relative">
        <button onClick={onClose} className="absolute top-4 right-4 text-slate-400 hover:text-slate-600">
          <X className="w-5 h-5" />
        </button>

        <div className="w-16 h-16 rounded-full bg-blue-50 text-blue-600 flex items-center justify-center mx-auto mb-4 border border-blue-200">
          <Mic className="w-8 h-8" />
        </div>

        <h3 className="text-lg font-bold text-slate-900">Voice Drafting Agent</h3>
        <p className="text-xs text-slate-500 mt-1">Speak legal instructions or dictations. Built-in OpenWhispr & VoxCPM workflows.</p>

        {/* Audio Waveform */}
        <div className="flex items-center justify-center space-x-1.5 my-6 h-12 bg-slate-50 rounded-xl p-2 border border-slate-100">
          {[0.1, 0.3, 0.2, 0.4, 0.15].map((delay, idx) => (
            <div 
              key={idx}
              className={`w-1.5 rounded-full ${idx % 2 === 0 ? 'bg-blue-600' : 'bg-indigo-600'}`}
              style={{
                height: isRecording ? '24px' : '8px',
                transition: 'height 0.2s ease-in-out'
              }}
            />
          ))}
        </div>

        {/* Transcript Box */}
        <div className="bg-slate-100 p-3 rounded-xl text-xs text-slate-700 min-h-[60px] flex items-center justify-center text-center font-medium italic border border-slate-200/60">
          {transcript || '"Listening for instructions... (e.g. \'Draft an NDA\', \'Review this contract\', \'Verify citations\')"'}
        </div>

        {/* Quick Suggestion Chips */}
        <div className="mt-4 flex flex-wrap gap-1.5 justify-center text-[11px]">
          <button 
            onClick={() => onSimulatePhrase('Draft a Mutual NDA under Indian law')} 
            className="bg-blue-50 hover:bg-blue-100 text-blue-700 px-2.5 py-1 rounded-full border border-blue-200 transition"
          >
            "Draft a Mutual NDA"
          </button>
          <button 
            onClick={() => onSimulatePhrase('Review this contract for risks')} 
            className="bg-rose-50 hover:bg-rose-100 text-rose-700 px-2.5 py-1 rounded-full border border-rose-200 transition"
          >
            "Review contract"
          </button>
          <button 
            onClick={() => onSimulatePhrase('Verify legal citations')} 
            className="bg-emerald-50 hover:bg-emerald-100 text-emerald-700 px-2.5 py-1 rounded-full border border-emerald-200 transition"
          >
            "Verify citations"
          </button>
        </div>

        {/* Stop/Action Button */}
        <div className="mt-6">
          <button 
            onClick={onToggleRecording} 
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-xl text-xs transition shadow-md"
          >
            {isRecording ? 'Stop Listening & Process' : 'Start Voice Input'}
          </button>
        </div>
      </div>
    </div>
  );
};
