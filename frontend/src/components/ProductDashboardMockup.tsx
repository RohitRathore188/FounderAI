import { Activity, Shield, Terminal, TrendingUp, CheckCircle, Network } from 'lucide-react';

export default function ProductDashboardMockup() {
  const mockLogs = [
    { time: '11:42:05', agent: 'discovery', text: 'Onboarding data parsed: Dr. Jane Smith' },
    { time: '11:42:08', agent: 'market', text: 'Competitor database scanned: TAM $14.2B validated' },
    { time: '11:42:15', agent: 'legal', text: 'Delaware C-Corp filing forms compiled successfully' },
    { time: '11:42:24', agent: 'funding', text: 'Grant options matched: 14 federal programs matching criteria' }
  ];

  return (
    <div className="w-full h-full bg-slate-950/80 backdrop-blur-md rounded-[1.25rem] border border-white/10 p-4 sm:p-6 flex flex-col gap-4 text-left select-none overflow-hidden relative font-sans">
      {/* Background Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-80 h-80 rounded-full bg-indigo-500/5 blur-[80px] pointer-events-none" />

      {/* Top Header Controls */}
      <div className="flex items-center justify-between border-b border-white/5 pb-3">
        <div className="flex items-center gap-1.5">
          <div className="w-2.5 h-2.5 rounded-full bg-red-500/70" />
          <div className="w-2.5 h-2.5 rounded-full bg-yellow-500/70" />
          <div className="w-2.5 h-2.5 rounded-full bg-emerald-500/70" />
          <span className="text-[10px] text-slate-400 font-mono ml-2 tracking-wider">founder_ai_os_v1.0.4_stable</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          <span className="text-[9px] uppercase tracking-widest text-slate-400 font-bold">SYSTEM ACTIVE</span>
        </div>
      </div>

      {/* Main Grid Content */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-4 flex-grow overflow-hidden">
        {/* Mock Stats Panel (Left Column) */}
        <div className="md:col-span-4 flex flex-col gap-3">
          <div className="p-3.5 rounded-xl border border-white/5 bg-white/2 flex flex-col gap-1.5 shadow-[inset_0_1px_1px_rgba(255,255,255,0.02)]">
            <span className="text-[9px] uppercase tracking-wider text-indigo-300 font-bold flex items-center gap-1">
              <Activity className="w-3 h-3 text-indigo-400" /> System Orchestrator
            </span>
            <p className="text-xl font-bold text-white tracking-tight mt-0.5">10 Active Nodes</p>
            <div className="w-full h-1 bg-white/5 rounded-full overflow-hidden mt-1">
              <div className="w-4/5 h-full bg-indigo-500" />
            </div>
          </div>

          <div className="p-3.5 rounded-xl border border-white/5 bg-white/2 flex flex-col gap-1.5 shadow-[inset_0_1px_1px_rgba(255,255,255,0.02)]">
            <span className="text-[9px] uppercase tracking-wider text-cyan-300 font-bold flex items-center gap-1">
              <TrendingUp className="w-3 h-3 text-cyan-400" /> Market Validation
            </span>
            <p className="text-xl font-bold text-white tracking-tight mt-0.5">Score: 94.8%</p>
            <span className="text-[8px] text-emerald-400 font-bold mt-0.5">+14.2% TAM Confidence Ratio</span>
          </div>

          <div className="p-3.5 rounded-xl border border-white/5 bg-slate-900/20 flex flex-col gap-1.5">
            <span className="text-[9px] uppercase tracking-wider text-purple-300 font-bold flex items-center gap-1">
              <Shield className="w-3 h-3 text-purple-400" /> Legal & Vesting
            </span>
            <span className="text-[10px] text-slate-300 flex items-center gap-1.5 mt-0.5">
              <CheckCircle className="w-3.5 h-3.5 text-emerald-400" /> Incorporation Forms Synced
            </span>
          </div>
        </div>

        {/* Dashboard Visualization (Middle Column) */}
        <div className="md:col-span-8 flex flex-col gap-3 overflow-hidden">
          {/* Node Orchestration Canvas */}
          <div className="p-4 rounded-xl border border-white/5 bg-white/2 flex-grow flex flex-col justify-between overflow-hidden relative shadow-[inset_0_1px_1px_rgba(255,255,255,0.02)]">
            <span className="text-[9px] uppercase tracking-wider text-slate-400 font-bold flex items-center gap-1.5">
              <Network className="w-3.5 h-3.5 text-indigo-400" /> Node Connectivity Map
            </span>
            
            {/* SVG Interactive Graphic */}
            <div className="w-full h-24 flex items-center justify-center relative my-2 overflow-hidden">
              <svg className="w-full h-full" viewBox="0 0 200 80">
                {/* Connection lines */}
                <path d="M 30,40 L 70,25 M 30,40 L 70,55 M 70,25 L 130,25 M 70,55 L 130,55 M 130,25 L 170,40 M 130,55 L 170,40" stroke="rgba(99,102,241,0.2)" strokeWidth="1" strokeDasharray="3 3" />
                <path d="M 30,40 L 70,25 L 130,25 L 170,40" stroke="url(#activeBeam)" strokeWidth="1.5" className="connection-beam" />
                
                {/* Nodes */}
                <circle cx="30" cy="40" r="4" fill="#3b82f6" className="animate-pulse" />
                <circle cx="70" cy="25" r="5" fill="#8b5cf6" />
                <circle cx="70" cy="55" r="4.5" fill="#06b6d4" />
                <circle cx="130" cy="25" r="4.5" fill="#8b5cf6" />
                <circle cx="130" cy="55" r="5" fill="#3b82f6" />
                <circle cx="170" cy="40" r="5.5" fill="#06b6d4" className="animate-pulse" />
                
                <defs>
                  <linearGradient id="activeBeam" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stopColor="#3b82f6" stopOpacity="0.2" />
                    <stop offset="50%" stopColor="#8b5cf6" stopOpacity="1" />
                    <stop offset="100%" stopColor="#06b6d4" stopOpacity="0.2" />
                  </linearGradient>
                </defs>
              </svg>
              <div className="absolute inset-0 bg-gradient-to-t from-slate-950/40 via-transparent to-slate-950/40 pointer-events-none" />
            </div>

            <div className="flex justify-between items-center text-[9px] text-slate-400 font-mono mt-1 border-t border-white/5 pt-2">
              <span>Primary Node: HOST_COMPILER</span>
              <span>Sync Status: 100% SECURE</span>
            </div>
          </div>

          {/* Activity Terminal */}
          <div className="p-3.5 rounded-xl border border-white/5 bg-slate-950/90 font-mono text-[10px] flex flex-col gap-2">
            <span className="text-[9px] uppercase tracking-wider text-slate-400 font-bold flex items-center gap-1.5 pb-1 border-b border-white/5">
              <Terminal className="w-3.5 h-3.5 text-indigo-400" /> Active System logs
            </span>
            <div className="space-y-1 overflow-y-auto max-h-[72px] scroll-glass pr-1">
              {mockLogs.map((log, index) => (
                <div key={index} className="flex gap-2 text-slate-400 leading-normal">
                  <span className="text-slate-600">{log.time}</span>
                  <span className="text-indigo-400">[{log.agent}]</span>
                  <span className="text-slate-200">{log.text}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
