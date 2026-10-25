/**
 * DraftMate AI: Citation & Legal Authority Inspector Component
 * Displays Verified, Partially Verified, and Unverified citation badges,
 * official court/statute repository links, and hallucination guardrail warnings.
 */

import React from 'react';
import { ExternalLink, ShieldCheck, ShieldAlert, AlertTriangle } from 'lucide-react';

export interface CitationItem {
  citation_text: string;
  authority_title: string;
  status: 'verified' | 'partially_verified' | 'unverified';
  badge: string;
  badge_color: string;
  court: string;
  year: number | string;
  summary: string;
  source_url: string;
  confidence: number;
  notes: string;
}

export interface CitationAuditResult {
  total_citations: number;
  verified_count: number;
  partially_verified_count: number;
  unverified_count: number;
  integrity_score: number;
  guardrail_status: string;
  summary: string;
  citations: CitationItem[];
}

interface CitationInspectorProps {
  audit: CitationAuditResult;
}

export const CitationInspector: React.FC<CitationInspectorProps> = ({ audit }) => {
  return (
    <div className="space-y-4">
      {/* Integrity Summary Banner */}
      <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 flex flex-col md:flex-row items-start md:items-center justify-between gap-3">
        <div>
          <div className="flex items-center space-x-2">
            <span className="font-bold text-slate-800 text-xs">Citation Integrity Score:</span>
            <span className={`font-extrabold text-sm ${audit.integrity_score >= 80 ? 'text-emerald-600' : 'text-amber-600'}`}>
              {audit.integrity_score}%
            </span>
            <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded ${audit.guardrail_status === 'SECURE' ? 'bg-emerald-100 text-emerald-800' : 'bg-red-100 text-red-800'}`}>
              {audit.guardrail_status}
            </span>
          </div>
          <p className="text-slate-500 text-[11px] mt-0.5">{audit.summary}</p>
        </div>

        <div className="flex items-center space-x-2 text-xs">
          <span className="px-2.5 py-1 bg-green-50 text-green-700 rounded font-medium border border-green-200">
            {audit.verified_count} Verified
          </span>
          <span className="px-2.5 py-1 bg-amber-50 text-amber-700 rounded font-medium border border-amber-200">
            {audit.partially_verified_count} Partially Verified
          </span>
          <span className="px-2.5 py-1 bg-red-50 text-red-700 rounded font-medium border border-red-200">
            {audit.unverified_count} Flagged
          </span>
        </div>
      </div>

      {/* Citations List */}
      <div className="space-y-3">
        {audit.citations.map((c, i) => {
          const isVerified = c.status === 'verified';
          const isPartial = c.status === 'partially_verified';

          return (
            <div 
              key={i} 
              className={`p-4 rounded-xl border space-y-2 transition ${
                isVerified 
                  ? 'bg-emerald-50/20 border-emerald-200' 
                  : isPartial 
                    ? 'bg-amber-50/20 border-amber-200' 
                    : 'bg-red-50/20 border-red-200'
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span className={`text-[10px] font-extrabold px-2 py-0.5 rounded uppercase tracking-wider text-white ${
                    isVerified ? 'bg-emerald-600' : isPartial ? 'bg-amber-600' : 'bg-red-600'
                  }`}>
                    {c.badge}
                  </span>
                  <span className="font-bold text-xs text-slate-800">{c.authority_title}</span>
                </div>
                <span className="text-[11px] text-slate-500 font-mono">{c.year || ''}</span>
              </div>

              <div className="text-xs text-slate-700 font-mono bg-white/70 p-2 rounded border border-slate-200/50">
                "{c.citation_text}"
              </div>

              <p className="text-[11px] text-slate-600">{c.summary || c.notes}</p>

              <div className="flex items-center justify-between pt-1 border-t border-slate-200/40 text-[10px]">
                <span className="text-slate-500">
                  Authority: <strong>{c.court || 'Official Gazette'}</strong>
                </span>

                {c.source_url ? (
                  <a 
                    href={c.source_url} 
                    target="_blank" 
                    rel="noopener noreferrer" 
                    className="text-blue-600 hover:underline flex items-center space-x-1 font-semibold"
                  >
                    <span>View Official Record</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                ) : (
                  <span className="text-red-500 font-semibold flex items-center space-x-1">
                    <ShieldAlert className="w-3 h-3" />
                    <span>Guardrail: Lack of verified record</span>
                  </span>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
