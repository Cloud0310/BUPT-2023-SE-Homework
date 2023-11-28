// prettier.config.cjs
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
      files: ["*.css", "*.ts", "*.js", "*.json", "*.cjs", "*.mjs"],
      options: {
        tabWidth: 4
      }
    }
  ]
};
