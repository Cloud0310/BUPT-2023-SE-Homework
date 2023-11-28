import colors from "tailwindcss/colors";

/** @type {import('tailwindcss').Config} */
export default {
    content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
    theme: {
        extend: {},
        colors: {
            transparent: "transparent",
            current: "currentColor",
            black: "#000",
            white: "#fff",
            primary: colors.violet,
            neutral: colors.slate,
            green: colors.green,
            red: colors.red,
            orange: colors.orange
        },
        fontFamily: {
            sans: ["Source Han Sans SC VF", "sans-serif"]
        }
    },
    plugins: []
};
