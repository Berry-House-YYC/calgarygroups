const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
  darkMode: "class",
  content: ["./src/**/*.{njk,md,html,js}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Noto Sans", ...defaultTheme.fontFamily.sans]
      },
      colors: {
        brand: {
          orange: "#fc7a1e",
          cream: "#ede1de",
          pink: "#b56eaf",
          coffee: "#18020c",
          cyan: "#4a888d"
        }
      }
    }
  },
  plugins: []
};
