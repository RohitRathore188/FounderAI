import { Brain, BookOpen, Filter, Coins, Scale, FileText, Rocket, Check } from 'lucide-react';

interface TimelinePhase {
  id: string;
  name: string;
  time: string;
  activeRange: [number, number];
  icon: React.ReactNode;
  description: string;
}

interface OrchestrationTimelineProps {
  progress: number;
}

export default function OrchestrationTimeline({ progress }: OrchestrationTimelineProps) {
  const phases: TimelinePhase[] = [
    {
      id: 'discovery',
      name: 'Discovery Phase',
      time: '00:00 - 15:00',
      activeRange: [1, 25],
      description: 'AI Brain & Digital Book synthesis',
      icon: (
        <div className="relative w-8 h-8 flex items-center justify-center">
          <Brain className="w-6 h-6 text-indigo-400 absolute -top-1 -left-1 animate-pulse" />
          <BookOpen className="w-4 h-4 text-cyan-400 absolute bottom-0 right-0" />
        </div>
      )
    },
    {
      id: 'validation',
      name: 'Validation Phase',
      time: '15:00 - 35:00',
      activeRange: [26, 50],
      description: 'Funnel & Currency analysis',
      icon: (
        <div className="relative w-8 h-8 flex items-center justify-center">
          <Filter className="w-6 h-6 text-purple-400 absolute -top-1 -left-1" />
          <Coins className="w-4 h-4 text-amber-400 absolute bottom-0 right-0 animate-bounce" />
        </div>
      )
    },
    {
      id: 'legal',
      name: 'Legal Agent',
      time: '35:00 - 50:00',
      activeRange: [51, 75],
      description: 'Gavel & Document verification',
      icon: (
        <div className="relative w-8 h-8 flex items-center justify-center">
          <Scale className="w-6 h-6 text-emerald-400 absolute -top-1 -left-1" />
          <FileText className="w-4 h-4 text-teal-400 absolute bottom-0 right-0" />
        </div>
      )
    },
    {
      id: 'launch',
      name: 'Launch Readiness',
      time: '50:00 - 60:00',
      activeRange: [76, 100],
      description: 'Rocket deployment system',
      icon: (
        <div className="relative w-8 h-8 flex items-center justify-center">
          <Rocket className="w-7 h-7 text-rose-400 absolute -top-1.5 -left-1 hover:translate-y-[-4px] transition-transform" />
        </div>
      )
    }
  ];

  return (
    <div className="w-full py-4">
      {/* Outer Tube Container */}
      <div className="relative w-full h-36 rounded-3xl border border-white/10 bg-slate-950/60 backdrop-blur-xl shadow-[inset_0_0_24px_rgba(99,102,241,0.12)] flex items-center justify-between px-6 sm:px-12 overflow-hidden">
        
        {/* Animated Particle Stream Background Line */}
        <div className="absolute inset-x-0 top-1/2 -translate-y-1/2 h-[2px] bg-slate-800">
          <div 
            className="h-full bg-gradient-to-r from-indigo-500 via-violet-500 to-cyan-400 transition-all duration-500 timeline-beam-flow" 
            style={{ width: `${progress}%` }} 
          />
        </div>

        {/* Floating background grids inside the tube */}
        <div className="absolute inset-0 bg-grid-timeline pointer-events-none opacity-20" />

        {phases.map((phase) => {
          const isCompleted = progress > phase.activeRange[1];
          const isActive = progress >= phase.activeRange[0] && progress <= phase.activeRange[1];

          return (
            <div key={phase.id} className="relative z-10 flex flex-col items-center gap-2 group cursor-pointer">
              
              {/* Node Hologram Container */}
              <div 
                className={`w-16 h-16 rounded-2xl border flex items-center justify-center relative transition-all duration-500 transform hover:scale-110 [transform:rotateX(12deg)_rotateY(-12deg)] ${
                  isActive 
                    ? 'bg-slate-900/90 border-indigo-400 shadow-[0_0_20px_rgba(99,102,241,0.45)]' 
                    : isCompleted 
                    ? 'bg-emerald-950/40 border-emerald-500/40 shadow-[0_0_15px_rgba(16,185,129,0.2)]'
                    : 'bg-slate-950/80 border-white/5 opacity-50'
                }`}
              >
                {/* Active pulsating ring */}
                {isActive && (
                  <span className="absolute inset-0 rounded-2xl border border-indigo-400 animate-ping opacity-60" />
                )}

                {/* Corner highlight lines */}
                <div className="absolute top-1 left-1 w-1.5 h-1.5 border-t border-l border-white/20 rounded-tl" />
                <div className="absolute bottom-1 right-1 w-1.5 h-1.5 border-b border-r border-white/20 rounded-br" />

                {/* Phase Icon */}
                <div className="relative z-10">
                  {phase.icon}
                </div>

                {/* Complete overlay checkmark */}
                {isCompleted && (
                  <div className="absolute -top-1.5 -right-1.5 w-5 h-5 rounded-full bg-emerald-500 border border-slate-950 flex items-center justify-center shadow">
                    <Check className="w-3 h-3 text-slate-950 stroke-[3]" />
                  </div>
                )}
              </div>

              {/* Text labels below the tube */}
              <div className="text-center flex flex-col items-center mt-1">
                <span className={`text-[10px] font-bold tracking-wider uppercase ${
                  isActive ? 'text-indigo-300' : isCompleted ? 'text-emerald-400' : 'text-slate-500'
                }`}>
                  {phase.name}
                </span>
                <span className="text-[8px] text-slate-400 font-mono mt-0.5">
                  {phase.time}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
