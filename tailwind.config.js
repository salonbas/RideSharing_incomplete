/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  safelist: [
    'px-3', 'py-2', 'text-white', 'bg-red-500', 'bg-blue-600', 'text-xl',
    'p-6', 'rounded', 'shadow', 'bg-green-500', 'text-sm', 'mt-4'
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Poppins', 'sans-serif'],
      },
      gridTemplateColumns: {
        '70/30': '70% 28%',
      },
    },
  },
  plugins: [],
}
