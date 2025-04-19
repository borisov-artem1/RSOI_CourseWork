/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        "my-primary-color": "var(--my-primary-color)",
        "my-secondary-color": "var(--my-secondary-color)",
        "my-third-color": "var(--my-third-color)",
      },
      fontSize: {
        "my-large-size": "var(--large-size)",
        "my-high-size": "var(--high-size)",
        "my-medium-size": "var(--medium-size)",
        "my-little-size": "var(--little-size)",
        "my-mini-size": "var(--mini-size)",
      },
      lineHeight: {
        "my-large-height": "var(--my-large-height)",
        "my-high-height": "var(--my-high-height)",
        "my-medium-height": "var(--my-medium-height)",
        "my-little-height": "var(--my-little-height)",
        "my-mini-height": "var(--my-mini-height)",
      }
    },
  },
  plugins: [],
}

