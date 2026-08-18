'use client';

import React, { useState } from 'react';
import { Lead } from '../lib/types';
import { SignalBadge } from './SignalBadge';
import { ExternalLink, Sparkles, ChevronDown, ChevronUp, MapPin, Building2, CheckCircle2, Zap } from 'lucide-react';

interface Props {
  lead: Lead;
  onSelectOutreach: (lead: Lead) => void;
}

export const LeadCard: React.FC<Props> = ({ lead, onSelectOutreach }) => {
  const [showBreakdown, setShowBreakdown] = useState(false);

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'bg-emerald-600 text-white border-emerald-700';
    if (score >= 60) return 'bg-indigo-600 text-white border-indigo-700';
    if (score >= 40) return 'bg-amber-500 text-white border-amber-600';
    return 'bg-slate-500 text-white border-slate-600';
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm hover:shadow-md transition-all duration-200">
      <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
        {/* Company Meta Header */}
        <div className="flex-1">
          <div className="flex items-center space-x-2.5">
            <h3 className="text-lg font-bold text-slate-900">{lead.company_name}</h3>
            {lead.website && (
              <a
                href={lead.website}
                target="_blank"
                rel="noopener noreferrer"
                className="text-slate-400 hover:text-indigo-600 transition-colors p-1"
                title="Visit Website"
              >
                <ExternalLink className="w-4 h-4" />
              </a>
            )}
          </div>

          <div className="flex flex-wrap items-center gap-3 mt-1.5 text-xs text-slate-500">
            {lead.industry && (
              <span className="flex items-center space-x-1 font-medium bg-slate-100 px-2.5 py-0.5 rounded text-slate-700">
                <Building2 className="w-3.5 h-3.5" />
                <span>{lead.industry}</span>
              </span>
            )}
            {lead.location && (
              <span className="flex items-center space-x-1">
                <MapPin className="w-3.5 h-3.5 text-slate-400" />
                <span>{lead.location}</span>
              </span>
            )}
          </div>

          {lead.description && (
            <p className="mt-2.5 text-xs text-slate-600 leading-relaxed line-clamp-2">
              {lead.description}
            </p>
          )}
        </div>

        {/* Score Badge */}
        <div className="flex flex-col items-end flex-shrink-0">
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setShowBreakdown(!showBreakdown)}
              className="flex items-center space-x-1 text-xs text-slate-500 hover:text-slate-700"
            >
              <span>Breakdown</span>
              {showBreakdown ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
            </button>
            <div className={`px-3 py-1 rounded-xl text-sm font-bold shadow-sm border flex items-center space-x-1 ${getScoreColor(lead.score)}`}>
              <span>{lead.score}</span>
              <span className="text-[10px] opacity-80">/100</span>
            </div>
          </div>
        </div>
      </div>

      {/* Score Breakdown Collapsible Panel */}
      {showBreakdown && lead.score_breakdown && (
        <div className="mt-4 p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs grid grid-cols-2 sm:grid-cols-5 gap-2 text-center animate-fade-in">
          <div>
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">ICP Fit</span>
            <span className="font-bold text-slate-800">{lead.score_breakdown.icp_fit} / 30</span>
          </div>
          <div>
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Signals</span>
            <span className="font-bold text-slate-800">{lead.score_breakdown.signal_strength} / 25</span>
          </div>
          <div>
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Recency</span>
            <span className="font-bold text-slate-800">{lead.score_breakdown.signal_recency} / 20</span>
          </div>
          <div>
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Relevance</span>
            <span className="font-bold text-slate-800">{lead.score_breakdown.company_relevance} / 15</span>
          </div>
          <div>
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Confidence</span>
            <span className="font-bold text-slate-800">{lead.score_breakdown.data_confidence} / 10</span>
          </div>
        </div>
      )}

      {/* Explanations: Why Good & Why Now */}
      <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
        {lead.why_this_is_a_good_lead && (
          <div className="p-3 bg-indigo-50/60 rounded-xl border border-indigo-100">
            <div className="flex items-center space-x-1.5 text-indigo-900 font-semibold mb-1">
              <CheckCircle2 className="w-3.5 h-3.5 text-indigo-600" />
              <span>Why This is a Good Lead</span>
            </div>
            <p className="text-indigo-950 leading-relaxed">{lead.why_this_is_a_good_lead}</p>
          </div>
        )}

        {lead.why_now && (
          <div className="p-3 bg-amber-50/70 rounded-xl border border-amber-100">
            <div className="flex items-center space-x-1.5 text-amber-900 font-semibold mb-1">
              <Zap className="w-3.5 h-3.5 text-amber-600" />
              <span>Why Warm RIGHT NOW</span>
            </div>
            <p className="text-amber-950 leading-relaxed">{lead.why_now}</p>
          </div>
        )}
      </div>

      {/* Signal Tags */}
      {lead.signals && lead.signals.length > 0 && (
        <div className="mt-3.5">
          <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block mb-1.5">
            Detected Signals:
          </span>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {lead.signals.map((sig, idx) => (
              <SignalBadge key={idx} signal={sig} />
            ))}
          </div>
        </div>
      )}

      {/* Card Footer Actions */}
      <div className="mt-4 pt-3 border-t border-slate-100 flex justify-between items-center">
        <span className="text-[11px] text-slate-400">
          {lead.sources?.length ? `${lead.sources.length} verifiable source(s)` : 'Source verified'}
        </span>
        <button
          onClick={() => onSelectOutreach(lead)}
          className="flex items-center space-x-1.5 text-xs bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-semibold px-3 py-1.5 rounded-lg border border-indigo-200 transition-colors"
        >
          <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
          <span>Outreach Hook</span>
        </button>
      </div>
    </div>
  );
};
