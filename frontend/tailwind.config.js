/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'bg-dark': '#03070C',
        'bg-navy': '#080E1A',
        'glass-bg': 'rgba(8, 14, 26, 0.45)',
        'glass-bg-active': 'rgba(99, 102, 241, 0.08)',
        'glass-bg-card': 'rgba(13, 20, 35, 0.5)',
        'glass-border': 'rgba(255, 255, 255, 0.04)',
        'glass-border-glow': 'rgba(99, 102, 241, 0.2)',
        'color-primary': '#3B82F6',
        'color-secondary': '#8B5CF6',
        'color-accent': '#06B6D4',
        'color-success': '#10B981',
        'color-warning': '#F59E0B',
        'color-danger': '#EF4444',
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', '-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'Roboto', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      borderRadius: {
        'sm': '8px',
        'md': '14px',
        'lg': '24px',
        'xl': '28px',
      }
    },
  },
  plugins: [],
}
