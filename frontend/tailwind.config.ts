import type { Config } from 'tailwindcss';

export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#18181b',
        paper: '#f6f1e8',
        ember: '#b45309',
        moss: '#4d6b57',
        steel: '#34495e',
        haze: '#ece6db',
      },
      fontFamily: {
        sans: ['Pretendard Variable', 'SUIT Variable', 'Noto Sans KR', 'sans-serif'],
        display: ['IBM Plex Sans KR', 'Pretendard Variable', 'sans-serif'],
      },
      boxShadow: {
        panel: '0 18px 45px rgba(24, 24, 27, 0.08)',
      },
      keyframes: {
        rise: {
          '0%': { opacity: '0', transform: 'translateY(14px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
      animation: {
        rise: 'rise 420ms ease-out both',
      },
    },
  },
  plugins: [],
} satisfies Config;

