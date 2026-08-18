'use client';

import React, { useState } from 'react';
import { LeadGenerateRequest } from '../lib/types';
import { Sparkles, Search, Globe, Building2 } from 'lucide-react';

interface Props {
  onSubmit: (data: LeadGenerateRequest) => void;
  loading: boolean;
}

export const LeadForm: React.FC<Props> = ({ onSubmit, loading }) => {
  const [icp, setIcp] = useState('Find Healthcare & Diagnostics companies in India opening new diagnostic centers and hiring medical staff.');
  const [industry, setIndustry] = useState('Healthcare & Biotech');
  const [geography, setGeography] = useState('India');
  const [numberOfLeads, setNumberOfLeads] = useState(5);
  const [activePreset, setActivePreset] = useState<string>('healthcare');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!icp.trim()) return;
    onSubmit({
      icp,
      industry: industry.trim() || undefined,
      geography: geography.trim() || undefined,
      number_of_leads: numberOfLeads,
    });
  };

  const handleQuickPreset = (key: string, presetText: string, presetIndustry: string, presetGeo: string) => {
    setActivePreset(key);
    setIcp(presetText);
    setIndustry(presetIndustry);
    setGeography(presetGeo);
  };

  const handleSelectGeography = (geo: string) => {
    setGeography(geo);
    if (!icp.toLowerCase().includes(geo.toLowerCase())) {
      setIcp(`Find ${industry || 'commercial'} companies in ${geo} expanding operations and hiring.`);
    }
  };

  const handleSelectIndustry = (ind: string) => {
    setIndustry(ind);
    if (!icp.toLowerCase().includes(ind.toLowerCase())) {
      setIcp(`Find ${ind} companies in ${geography || 'India'} with active operational expansion.`);
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <div className="p-2 bg-indigo-50 rounded-xl text-indigo-600">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-slate-900">Universal B2B Ideal Customer Profile (ICP)</h2>
            <p className="text-xs text-slate-500">Universal lead generation engine across ALL sectors (Healthcare, Manufacturing, Retail, Real Estate, SaaS, Fintech, Legal).</p>
          </div>
        </div>
      </div>

      {/* Cross-Industry Preset Examples */}
      <div className="mb-5 space-y-2">
        <div className="flex items-center space-x-2">
          <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Universal Presets:</span>
        </div>
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => handleQuickPreset('healthcare', 'Find Healthcare & Diagnostics companies in India opening new diagnostic centers and hiring medical staff.', 'Healthcare & Biotech', 'India')}
            className={`text-xs font-semibold px-3 py-1.5 rounded-xl border transition-all ${
              activePreset === 'healthcare'
                ? 'bg-indigo-600 text-white border-indigo-700 shadow-sm'
                : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
            }`}
          >
            🏥 Healthcare & FDA/ISO Approvals
          </button>
          <button
            type="button"
            onClick={() => handleQuickPreset('manufacturing', 'Find Precision Manufacturing companies in India setting up new factories and hiring plant managers.', 'Manufacturing & Industrial', 'India')}
            className={`text-xs font-semibold px-3 py-1.5 rounded-xl border transition-all ${
              activePreset === 'manufacturing'
                ? 'bg-indigo-600 text-white border-indigo-700 shadow-sm'
                : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
            }`}
          >
            🏭 Manufacturing & Factory Expansion
          </button>
          <button
            type="button"
            onClick={() => handleQuickPreset('retail', 'Find D2C Brands & Retailers in India that raised Series A funding and are expanding CMO marketing teams.', 'E-Commerce & Retail', 'India')}
            className={`text-xs font-semibold px-3 py-1.5 rounded-xl border transition-all ${
              activePreset === 'retail'
                ? 'bg-indigo-600 text-white border-indigo-700 shadow-sm'
                : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
            }`}
          >
            🛒 E-Commerce D2C + Series A Funding
          </button>
          <button
            type="button"
            onClick={() => handleQuickPreset('realestate', 'Find Real Estate Developers in India constructing commercial tech parks and hiring project architects.', 'Real Estate & Construction', 'India')}
            className={`text-xs font-semibold px-3 py-1.5 rounded-xl border transition-all ${
              activePreset === 'realestate'
                ? 'bg-indigo-600 text-white border-indigo-700 shadow-sm'
                : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
            }`}
          >
            🏢 Commercial Real Estate Projects
          </button>
          <button
            type="button"
            onClick={() => handleQuickPreset('saas', 'Find SaaS companies in India with 50-500 employees that recently raised funding and are hiring engineers.', 'SaaS & Technology', 'India')}
            className={`text-xs font-semibold px-3 py-1.5 rounded-xl border transition-all ${
              activePreset === 'saas'
                ? 'bg-indigo-600 text-white border-indigo-700 shadow-sm'
                : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
            }`}
          >
            💻 SaaS & Tech Hiring
          </button>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
            Universal ICP Prompt Description *
          </label>
          <textarea
            value={icp}
            onChange={(e) => setIcp(e.target.value)}
            rows={3}
            required
            className="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600 transition-all text-slate-800"
            placeholder="Describe any industry criteria: Healthcare, Manufacturing, Real Estate, Legal, Retail, SaaS, Fintech..."
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Universal Industry Selection */}
          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
              Industry Sector
            </label>
            <input
              type="text"
              value={industry}
              onChange={(e) => setIndustry(e.target.value)}
              className="w-full px-3.5 py-2 text-sm rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600 transition-all text-slate-800 mb-2"
              placeholder="e.g. Healthcare, Manufacturing, Retail"
            />
            <div className="flex flex-wrap gap-1">
              {['Healthcare & Biotech', 'Manufacturing', 'E-Commerce & D2C', 'Real Estate', 'Legal & Services', 'Fintech', 'SaaS & Tech'].map((ind) => (
                <button
                  key={ind}
                  type="button"
                  onClick={() => handleSelectIndustry(ind)}
                  className={`text-[11px] px-2 py-0.5 rounded-lg border font-medium transition-colors ${
                    industry === ind
                      ? 'bg-indigo-100 text-indigo-800 border-indigo-300 font-bold'
                      : 'bg-slate-50 text-slate-600 border-slate-200 hover:bg-slate-100'
                  }`}
                >
                  {ind}
                </button>
              ))}
            </div>
          </div>

          {/* Geography Selection */}
          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
              Geography / Region
            </label>
            <input
              type="text"
              value={geography}
              onChange={(e) => setGeography(e.target.value)}
              className="w-full px-3.5 py-2 text-sm rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600 transition-all text-slate-800 mb-2"
              placeholder="e.g. India, United States"
            />
            <div className="flex flex-wrap gap-1">
              {['India', 'United States', 'Europe', 'Global'].map((geo) => (
                <button
                  key={geo}
                  type="button"
                  onClick={() => handleSelectGeography(geo)}
                  className={`text-[11px] px-2 py-0.5 rounded-lg border font-medium transition-colors ${
                    geography === geo
                      ? 'bg-indigo-100 text-indigo-800 border-indigo-300 font-bold'
                      : 'bg-slate-50 text-slate-600 border-slate-200 hover:bg-slate-100'
                  }`}
                >
                  📍 {geo}
                </button>
              ))}
            </div>
          </div>

          {/* Count Slider */}
          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
              Lead Target Count ({numberOfLeads})
            </label>
            <div className="flex items-center space-x-3 pt-1">
              <input
                type="range"
                min="1"
                max="20"
                value={numberOfLeads}
                onChange={(e) => setNumberOfLeads(parseInt(e.target.value))}
                className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
              />
              <span className="text-xs font-bold text-slate-800 min-w-[20px]">{numberOfLeads}</span>
            </div>
          </div>
        </div>

        <div className="pt-3 flex justify-end">
          <button
            type="submit"
            disabled={loading || !icp.trim()}
            className="w-full md:w-auto flex items-center justify-center space-x-2 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white px-6 py-2.5 rounded-xl font-bold text-sm shadow-md transition-all duration-200"
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                <span>Running Universal Pipeline...</span>
              </>
            ) : (
              <>
                <Search className="w-4 h-4" />
                <span>Generate & Qualify Leads</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};
