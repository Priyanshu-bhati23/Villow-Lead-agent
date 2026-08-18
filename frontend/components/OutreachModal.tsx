'use client';

import React, { useState } from 'react';
import { Lead } from '../lib/types';
import { X, Copy, Check, Sparkles, Send } from 'lucide-react';

interface Props {
  lead: Lead | null;
  onClose: () => void;
}

export const OutreachModal: React.FC<Props> = ({ lead, onClose }) => {
  const [copied, setCopied] = useState(false);

  if (!lead) return null;

  const handleCopy = () => {
    if (lead.outreach_hook) {
      navigator.clipboard.writeText(lead.outreach_hook);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">
      <div className="bg-white rounded-2xl max-w-xl w-full p-6 shadow-2xl border border-slate-100 relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-slate-600 p-1.5 rounded-full hover:bg-slate-100"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center space-x-2.5 mb-4">
          <div className="p-2 bg-indigo-100 rounded-xl text-indigo-600">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-slate-900">Personalized Outreach Hook</h3>
            <p className="text-xs text-slate-500">{lead.company_name} • {lead.location}</p>
          </div>
        </div>

        {/* Why Now Context */}
        {lead.why_now && (
          <div className="mb-4 p-3 bg-amber-50 rounded-xl border border-amber-100 text-xs">
            <span className="font-semibold text-amber-800 uppercase tracking-wider block text-[10px] mb-1">
              🔥 Why Warm Right Now:
            </span>
            <p className="text-amber-900 leading-relaxed">{lead.why_now}</p>
          </div>
        )}

        {/* Outreach Hook Textbox */}
        <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 mb-6">
          <p className="text-sm font-medium text-slate-800 leading-relaxed italic">
            "{lead.outreach_hook || 'No outreach hook generated.'}"
          </p>
        </div>

        {/* Sources */}
        {lead.sources && lead.sources.length > 0 && (
          <div className="mb-6">
            <span className="text-xs font-semibold text-slate-500 block mb-1">Supporting Fact Sources:</span>
            <div className="flex flex-wrap gap-1.5">
              {lead.sources.map((src, i) => (
                <a
                  key={i}
                  href={src}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-[11px] text-indigo-600 hover:underline bg-indigo-50 px-2 py-0.5 rounded border border-indigo-100 truncate max-w-xs"
                >
                  {src}
                </a>
              ))}
            </div>
          </div>
        )}

        <div className="flex justify-end space-x-3">
          <button
            onClick={onClose}
            className="px-4 py-2 text-xs font-medium text-slate-600 hover:bg-slate-100 rounded-lg"
          >
            Close
          </button>
          <button
            onClick={handleCopy}
            className="flex items-center space-x-1.5 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-semibold shadow-md transition-colors"
          >
            {copied ? (
              <>
                <Check className="w-4 h-4 text-emerald-300" />
                <span>Copied to Clipboard!</span>
              </>
            ) : (
              <>
                <Copy className="w-4 h-4" />
                <span>Copy Outreach Hook</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};
