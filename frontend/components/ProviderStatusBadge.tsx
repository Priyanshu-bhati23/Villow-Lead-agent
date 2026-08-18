'use client';

import React from 'react';
import { ProviderStatusResponse } from '../lib/types';
import { ShieldCheck, Cpu, Database, AlertCircle } from 'lucide-react';

interface Props {
  status: ProviderStatusResponse | null;
  loading: boolean;
  error?: string | null;
}

export const ProviderStatusBadge: React.FC<Props> = ({ status, loading, error }) => {
  if (loading) {
    return (
      <div className="flex items-center space-x-2 text-xs text-slate-500 animate-pulse bg-white/60 px-3 py-1.5 rounded-full border border-slate-200">
        <div className="w-2 h-2 rounded-full bg-indigo-500 animate-ping" />
        <span>Connecting to Backend Agent...</span>
      </div>
    );
  }

  if (error || !status) {
    return (
      <div className="flex items-center space-x-1.5 text-xs text-amber-700 bg-amber-50 px-3 py-1.5 rounded-full border border-amber-200">
        <AlertCircle className="w-3.5 h-3.5 text-amber-600" />
        <span>Backend Disconnected ({error || 'Offline'})</span>
      </div>
    );
  }

  return (
    <div className="flex flex-wrap items-center gap-2">
      <div className={`flex items-center space-x-1.5 text-xs px-3 py-1 rounded-full font-medium border ${
        status.is_mock
          ? 'bg-amber-50 text-amber-700 border-amber-200'
          : 'bg-emerald-50 text-emerald-700 border-emerald-200'
      }`}>
        <ShieldCheck className="w-3.5 h-3.5" />
        <span>{status.active_provider}</span>
      </div>

      <div className="flex items-center space-x-1.5 text-xs bg-slate-100 text-slate-700 px-3 py-1 rounded-full border border-slate-200">
        <Cpu className="w-3.5 h-3.5 text-indigo-600" />
        <span>Groq: {status.has_groq ? status.groq_model : 'Fallback Mode'}</span>
      </div>

      <div className="flex items-center space-x-1.5 text-xs bg-slate-100 text-slate-700 px-3 py-1 rounded-full border border-slate-200">
        <Database className="w-3.5 h-3.5 text-blue-600" />
        <span>DB: {status.has_database ? 'Neon Postgres' : 'SQLite'}</span>
      </div>
    </div>
  );
};
