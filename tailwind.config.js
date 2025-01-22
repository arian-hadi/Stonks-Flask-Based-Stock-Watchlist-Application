/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./**/templates/**/*.html", // Covers templates for all apps
    "./**/templates/**/*.htm",  // For .htm files in any app
    "./src/**/*.js"             // Include any shared JavaScript files
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

