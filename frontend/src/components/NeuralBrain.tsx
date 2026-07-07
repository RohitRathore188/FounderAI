interface BrainNode {
  id: string;
  name: string;
  angle: number;
  status: 'idle' | 'active' | 'completed' | 'error';
}

interface NeuralBrainProps {
  activeNodeId?: string | null;
  nodes: BrainNode[];
}

export default function NeuralBrain({ nodes }: NeuralBrainProps) {
  const orbitRadius = 140;

  return (
    <div className="relative w-full max-w-[380px] aspect-square flex items-center justify-center">
      {/* Central Glowing AI Brain */}
      <div className="absolute z-10 w-[120px] h-[120px] rounded-full flex items-center justify-center brain-pulsing bg-gradient-to-tr from-indigo-600/40 via-violet-600/40 to-cyan-500/40 backdrop-blur-md border border-white/10 shadow-[0_0_50px_rgba(99,102,241,0.3)]">
        <div className="w-[86px] h-[86px] rounded-full bg-slate-950/80 border border-white/5 flex flex-col items-center justify-center p-2 text-center">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-4 h-4 text-white">
              <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 21L14.907 13H10.187L11 9L5 17h4.813zM15 10.5V3.75a.75.75 0 00-1.5 0v6.75a.75.75 0 001.5 0zM19.5 12h-6.75a.75.75 0 000 1.5h6.75a.75.75 0 000-1.5z" />
            </svg>
          </div>
          <span className="text-[10px] font-bold text-white tracking-widest uppercase mt-1.5">CORE OS</span>
        </div>
      </div>

      {/* SVG for connecting links */}
      <svg className="absolute inset-0 w-full h-full pointer-events-none" viewBox="0 0 380 380">
        <defs>
          <radialGradient id="glowGrad" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#818CF8" stopOpacity="0.4" />
            <stop offset="100%" stopColor="#818CF8" stopOpacity="0" />
          </radialGradient>
        </defs>
        
        {/* Connecting Lines */}
        {nodes.map((node) => {
          const x = 190 + orbitRadius * Math.cos((node.angle * Math.PI) / 180);
          const y = 190 + orbitRadius * Math.sin((node.angle * Math.PI) / 180);
          const isActive = node.status === 'active';
          const isCompleted = node.status === 'completed';

          return (
            <g key={node.id}>
              {/* Path connector line */}
              <line
                x1={190}
                y1={190}
                x2={x}
                y2={y}
                stroke={isActive ? '#818CF8' : isCompleted ? '#10B981' : '#1E293B'}
                strokeWidth={isActive ? 2 : 1}
                opacity={isActive ? 0.95 : isCompleted ? 0.6 : 0.25}
                className={isActive ? 'connection-beam' : ''}
              />
              {/* Glow filter under active paths */}
              {isActive && (
                <circle cx={x} cy={y} r="25" fill="url(#glowGrad)" />
              )}
            </g>
          );
        })}
      </svg>

      {/* Outer Floating Agent Node Dots */}
      {nodes.map((node) => {
        const x = 190 + orbitRadius * Math.cos((node.angle * Math.PI) / 180);
        const y = 190 + orbitRadius * Math.sin((node.angle * Math.PI) / 180);
        const isActive = node.status === 'active';
        const isCompleted = node.status === 'completed';

        return (
          <div
            key={node.id}
            style={{
              position: 'absolute',
              left: `${x - 22}px`,
              top: `${y - 22}px`,
              transition: 'all 0.5s cubic-bezier(0.16, 1, 0.3, 1)'
            }}
            className={`w-11 h-11 rounded-full flex items-center justify-center border backdrop-blur-md shadow-lg transition-transform hover:scale-110 cursor-help ${
              isActive
                ? 'bg-indigo-950/80 border-indigo-400 text-indigo-400 animate-pulse shadow-[0_0_15px_rgba(99,102,241,0.4)]'
                : isCompleted
                ? 'bg-emerald-950/80 border-emerald-500 text-emerald-400 shadow-[0_0_10px_rgba(16,185,129,0.25)]'
                : 'bg-slate-900/60 border-slate-800 text-slate-500'
            }`}
            title={`${node.name} (${node.status})`}
          >
            <span className="text-[10px] font-mono font-bold">A{nodes.indexOf(node) + 1}</span>
          </div>
        );
      })}
    </div>
  );
}
