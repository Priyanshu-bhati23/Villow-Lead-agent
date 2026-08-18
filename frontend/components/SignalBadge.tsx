'use client';

import React from 'react';
import { Signal } from '../lib/types';
import { TrendingUp, Users, Code2, Briefcase, ExternalLink, Factory, ShieldCheck, Sparkles } from 'lucide-react';

interface Props {
  signal: Signal;
}

export const SignalBadge: React.FC<Props> = ({ signal }) => {
  const getIcon = (type: string) => {
    const t = type.toLowerCase();
    if (t.includes('fund') || t.includes('capital')) {
      return <TrendingUp className="w-3.5 h-3.5 text-emerald-600" />;
    }
    if (t.includes('hir') || t.includes('recruit') || t.includes('team')) {
      return <Users className="w-3.5 h-3.5 text-blue-600" />;
    }
    if (t.includes('tech') || t.includes('stack')) {
      return <Code2 className="w-3.5 h-3.5 text-purple-600" />;
    }
    if (t.includes('expand') || t.includes('plant') || t.includes('factory') || t.includes('office')) {
      return <Factory className="w-3.5 h-3.5 text-amber-600" />;
    }
    if (t.includes('approval') || t.includes('fda') || t.includes('iso') || t.includes('compliance')) {
      return <ShieldCheck className="w-3.5 h-3.5 text-teal-600" />;
    }
    if (t.includes('job') || t.includes('posting')) {
      return <Briefcase className="w-3.5 h-3.5 text-indigo-600" />;
    }
    return <Sparkles className="w-3.5 h-3.5 text-slate-500" />;
  };

  const getTypeStyle = (type: string) => {
    const t = type.toLowerCase();
    if (t.includes('fund') || t.includes('capital')) {
      return 'bg-emerald-50 text-emerald-800 border-emerald-200';
    }
    if (t.includes('hir') || t.includes('recruit')) {
      return 'bg-blue-50 text-blue-800 border-blue-200';
    }
    if (t.includes('tech') || t.includes('stack')) {
      return 'bg-purple-50 text-purple-800 border-purple-200';
    }
    if (t.includes('expand') || t.includes('plant') || t.includes('factory')) {
      return 'bg-amber-50 text-amber-800 border-amber-200';
    }
    if (t.includes('approval') || t.includes('fda') || t.includes('iso')) {
      return 'bg-teal-50 text-teal-800 border-teal-200';
    }
    return 'bg-slate-50 text-slate-700 border-slate-200';
  };

  return (
    <div className={`flex items-start justify-between p-2.5 rounded-lg border text-xs ${getTypeStyle(signal.signal_type)}`}>
      <div className="flex items-start space-x-2">
        <div className="mt-0.5">{getIcon(signal.signal_type)}</div>
        <div>
          <span className="font-semibold uppercase tracking-wider text-[10px] block opacity-75">
            {signal.signal_type}
          </span>
          <p className="mt-0.5 leading-snug">{signal.signal_text}</p>
        </div>
      </div>
      {signal.source_url && (
        <a
          href={signal.source_url}
          target="_blank"
          rel="noopener noreferrer"
          className="ml-2 mt-0.5 hover:opacity-80 text-current flex-shrink-0"
          title="View Source"
        >
          <ExternalLink className="w-3.5 h-3.5" />
        </a>
      )}
    </div>
  );
};
