import React, { Suspense, lazy, useMemo } from 'react';

const Spline = lazy(() => import('@splinetool/react-spline'));

interface SplineSceneProps {
  scene: string;
  className?: string;
  fallback?: React.ReactNode;
}

interface SplineSceneBoundaryState {
  hasError: boolean;
}

class SplineSceneBoundary extends React.Component<
  { children: React.ReactNode; fallback: React.ReactNode },
  SplineSceneBoundaryState
> {
  constructor(props: { children: React.ReactNode; fallback: React.ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.warn('Spline scene failed to load:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }

    return this.props.children;
  }
}

export default function SplineScene({ scene, className = '', fallback }: SplineSceneProps) {
  const memoizedScene = useMemo(() => scene, [scene]);
  
  const defaultFallback = fallback ?? (
    <div className="w-full h-full flex items-center justify-center relative overflow-hidden bg-slate-950/20 rounded-[1.35rem]">
      {/* Background Orbs */}
      <div className="absolute w-44 h-44 rounded-full bg-indigo-500/10 blur-[60px] animate-pulse" />
      <div className="absolute w-32 h-32 rounded-full bg-cyan-400/8 blur-[40px] animate-pulse delay-700" />
      
      {/* Outer Rotating Orbit Ring */}
      <svg className="absolute w-60 h-60 animate-[spin_20s_linear_infinite]" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="44" stroke="rgba(255,255,255,0.03)" strokeWidth="0.5" fill="none" />
        <circle cx="50" cy="50" r="44" stroke="rgba(99, 102, 241, 0.4)" strokeWidth="1" fill="none" strokeDasharray="20 40" strokeLinecap="round" />
        <circle cx="94" cy="50" r="2.5" fill="#8b5cf6" className="animate-ping origin-center" style={{ transformOrigin: '50px 50px' }} />
      </svg>

      {/* Inner Reverse Orbit Ring */}
      <svg className="absolute w-48 h-48 animate-[spin_12s_linear_infinite_reverse]" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="40" stroke="rgba(255,255,255,0.02)" strokeWidth="0.5" fill="none" />
        <circle cx="50" cy="50" r="40" stroke="rgba(6, 182, 212, 0.3)" strokeWidth="1" fill="none" strokeDasharray="10 50" strokeLinecap="round" />
        <circle cx="10" cy="50" r="2" fill="#06b6d4" />
      </svg>

      {/* Central Glowing Core */}
      <div className="relative w-20 h-20 rounded-full bg-gradient-to-tr from-indigo-500 via-purple-600 to-cyan-400 p-[1.5px] shadow-[0_0_40px_rgba(99,102,241,0.35)] flex items-center justify-center z-10">
        <div className="w-full h-full rounded-full bg-slate-950/95 flex items-center justify-center relative overflow-hidden">
          {/* Internal Pulse Ring */}
          <div className="absolute w-12 h-12 rounded-full bg-indigo-500/10 border border-indigo-400/20 animate-ping" />
          
          {/* Inner Core Ball */}
          <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-400 to-cyan-300 animate-pulse flex items-center justify-center">
            <div className="w-4 h-4 rounded-full bg-slate-950 flex items-center justify-center">
              <div className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
            </div>
          </div>
        </div>
      </div>
      
      {/* Node connectivity lines radiating outwards */}
      <div className="absolute inset-0 opacity-15 flex items-center justify-center">
        <div className="w-56 h-[1px] bg-gradient-to-r from-transparent via-indigo-500 to-transparent rotate-45" />
        <div className="w-56 h-[1px] bg-gradient-to-r from-transparent via-cyan-500 to-transparent -rotate-45" />
      </div>
    </div>
  );

  return (
    <div className={`spline-scene ${className}`.trim()}>
      <SplineSceneBoundary fallback={defaultFallback}>
        <Suspense fallback={defaultFallback}>
          <Spline scene={memoizedScene} />
        </Suspense>
      </SplineSceneBoundary>
    </div>
  );
}
