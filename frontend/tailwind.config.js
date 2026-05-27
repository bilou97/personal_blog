/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js}'],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        serif: ['Lora', 'ui-serif', 'Georgia', 'serif'],
      },
      typography: {
        DEFAULT: {
          css: {
            fontFamily: 'Lora, ui-serif, Georgia, serif',
            fontSize: '1.0625rem',
            lineHeight: '1.8',
            'h1, h2, h3, h4, h5, h6': {
              fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif',
            },
          },
        },
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
}
