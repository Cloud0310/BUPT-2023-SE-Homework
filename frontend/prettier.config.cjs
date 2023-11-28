// prettier.config.js
module.exports = {
  arrowParens: "avoid",
  bracketSpacing: true,
  endOfLine: "crlf",
  semi: true,
  printWidth: 120,
  trailingComma: "none",
  plugins: ["prettier-plugin-tailwindcss"],
  overrides: [
    {
      files: ["*.css", "*.ts", "*.js", "*.json"],
      options: {
        tabWidth: 4
      }
    }
  ]
};
