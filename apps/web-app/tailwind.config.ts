import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // LUCA brand colors
        luca: {
          primary: '#3B82F6',
          secondary: '#10B981',
          accent: '#F59E0B',
          dark: '#1F2937',
          light: '#F3F4F6',
        },
        // Layer-specific colors
        layer: {
          0: '#9333EA',  // Root Kernel - Purple
          10: '#F59E0B', // DS-STAR - Amber
          11: '#10B981', // Metabolism - Green
          12: '#3B82F6', // Evolution - Blue
        },
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'consciousness': 'consciousness 5s ease-in-out infinite',
      },
      keyframes: {
        consciousness: {
          '0%, 100%': { opacity: '0.5', transform: 'scale(1)' },
          '50%': { opacity: '1', transform: 'scale(1.05)' },
        },
      },
    },
  },
  plugins: [],
}
export default config
