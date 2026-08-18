'use client';

import React, { useState, useEffect, useMemo } from 'react';
import { LeadForm } from '../components/LeadForm';
import { LeadCard } from '../components/LeadCard';
import { OutreachModal } from '../components/OutreachModal';
import { ProviderStatusBadge } from '../components/ProviderStatusBadge';
import { generateLeads, fetchProviderStatus } from '../lib/api';
import { Lead, LeadGenerateRequest, ProviderStatusResponse } from '../lib/types';
import { Sparkles, ArrowUpDown, RefreshCw, AlertCircle, Inbox, Layers } from 'lucide-react';

export default function Home() {
  const [providerStatus, setProviderStatus] = useState<ProviderStatusResponse | null>(null);
  const [statusLoading, setStatusLoading] = useState(true);
  const [statusError, setStatusError] = useState<string | null>(null);

  const [leads, setLeads] = useState<Lead[]>([]);
  const [requestId, setRequestId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [selectedLeadForOutreach, setSelectedLeadForOutreach] = useState<Lead | null>(null);
  const [sortBy, setSortBy] = useState<'score' | 'name' | 'signals'>('score');

  const loadStatus = async () => {
    setStatusLoading(true);
    setStatusError(null);
    try {
      const data = await fetchProviderStatus();
      setProviderStatus(data);
    } catch (err: any) {
      setStatusError(err.message || 'Failed to connect to backend.');
    } finally {
      setStatusLoading(false);
    }
  };

  useEffect(() => {
    loadStatus();
  }, []);

  const handleGenerate = async (reqData: LeadGenerateRequest) => {
    setLoading(true);
    setError(null);
    try {
      const res = await generateLeads(reqData);
      setLeads(res.leads);
      setRequestId(res.request_id);
    } catch (err: any) {
      setError(err.message || 'An error occurred while generating leads.');
    } finally {
      setLoading(false);
    }
  };

  const sortedLeads = useMemo(() => {
    const copy = [...leads];
    if (sortBy === 'score') {
      return copy.sort((a, b) => b.score - a.score);
    }
    if (sortBy === 'name') {
      return copy.sort((a, b) => a.company_name.localeCompare(b.company_name));
    }
    if (sortBy === 'signals') {
      return copy.sort((a, b) => (b.signals?.length || 0) - (a.signals?.length || 0));
    }
    return copy;
  }, [leads, sortBy]);

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900 pb-16">
      {/* Top Navigation Bar */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-40 shadow-sm">
        <div className="max-w-6xl mx-auto px-4 py-3.5 flex flex-col md:flex-row items-center justify-between gap-3">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-xl bg-indigo-600 flex items-center justify-center text-white font-bold shadow-md shadow-indigo-200">
              <Layers className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-base font-extrabold text-slate-900 tracking-tight">
                Villow Lead Generation Agent
              </h1>
              <p className="text-[11px] text-slate-500 font-medium">
                Founding Publisher Program MVP • Groq LLM + Real Data Signals
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            <ProviderStatusBadge status={providerStatus} loading={statusLoading} error={statusError} />
            <button
              onClick={loadStatus}
              className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100 transition-colors"
              title="Refresh Provider Status"
            >
              <RefreshCw className={`w-4 h-4 ${statusLoading ? 'animate-spin' : ''}`} />
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-4 pt-6 space-y-6">
        {/* Form Container */}
        <LeadForm onSubmit={handleGenerate} loading={loading} />

        {/* Error State */}
        {error && (
          <div className="p-4 bg-red-50 rounded-2xl border border-red-200 flex items-start space-x-3 text-red-800 text-sm">
            <AlertCircle className="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" />
            <div>
              <span className="font-bold block">Lead Generation Failed</span>
              <p className="text-xs text-red-700 mt-0.5">{error}</p>
            </div>
          </div>
        )}

        {/* Loading Indicator */}
        {loading && (
          <div className="bg-white rounded-2xl border border-slate-200 p-8 text-center space-y-3 animate-pulse">
            <div className="w-10 h-10 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin mx-auto" />
            <h3 className="text-sm font-bold text-slate-800">Agent Pipeline Running</h3>
            <p className="text-xs text-slate-500 max-w-md mx-auto">
              Parsing ICP prompt → Discovering candidate companies → Enriching verifiable signals → Computing 0-100 score matrix → Generating personalized hooks...
            </p>
          </div>
        )}

        {/* Results Container */}
        {!loading && leads.length > 0 && (
          <div className="space-y-4">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 bg-white px-5 py-3.5 rounded-xl border border-slate-200 shadow-sm">
              <div>
                <h2 className="text-sm font-bold text-slate-900">
                  Qualified Leads ({leads.length})
                </h2>
                {requestId && (
                  <span className="text-[11px] text-slate-400 font-mono">Req ID: {requestId}</span>
                )}
              </div>

              {/* Sorting Bar */}
              <div className="flex items-center space-x-2 text-xs">
                <span className="text-slate-500 font-medium flex items-center space-x-1">
                  <ArrowUpDown className="w-3.5 h-3.5 text-slate-400" />
                  <span>Sort By:</span>
                </span>
                <button
                  onClick={() => setSortBy('score')}
                  className={`px-3 py-1 rounded-lg border font-medium transition-colors ${
                    sortBy === 'score'
                      ? 'bg-indigo-50 text-indigo-700 border-indigo-200'
                      : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
                  }`}
                >
                  Score (High to Low)
                </button>
                <button
                  onClick={() => setSortBy('name')}
                  className={`px-3 py-1 rounded-lg border font-medium transition-colors ${
                    sortBy === 'name'
                      ? 'bg-indigo-50 text-indigo-700 border-indigo-200'
                      : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
                  }`}
                >
                  Company Name
                </button>
                <button
                  onClick={() => setSortBy('signals')}
                  className={`px-3 py-1 rounded-lg border font-medium transition-colors ${
                    sortBy === 'signals'
                      ? 'bg-indigo-50 text-indigo-700 border-indigo-200'
                      : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
                  }`}
                >
                  Signal Count
                </button>
              </div>
            </div>

            {/* Lead Cards List */}
            <div className="space-y-4">
              {sortedLeads.map((lead, idx) => (
                <LeadCard
                  key={lead.id || idx}
                  lead={lead}
                  onSelectOutreach={(l) => setSelectedLeadForOutreach(l)}
                />
              ))}
            </div>
          </div>
        )}

        {/* Empty State */}
        {!loading && leads.length === 0 && !error && (
          <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center text-slate-500 max-w-md mx-auto">
            <Inbox className="w-12 h-12 text-slate-300 mx-auto mb-3" />
            <h3 className="text-sm font-bold text-slate-700">No Leads Generated Yet</h3>
            <p className="text-xs text-slate-400 mt-1">
              Enter your Ideal Customer Profile criteria above and click "Generate & Qualify Leads" to run the agent.
            </p>
          </div>
        )}
      </div>

      {/* Modal for Outreach Hook */}
      <OutreachModal
        lead={selectedLeadForOutreach}
        onClose={() => setSelectedLeadForOutreach(null)}
      />
    </main>
  );
}
