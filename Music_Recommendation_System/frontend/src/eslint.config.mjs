import globals from "globals";
import js from "@eslint/js";
import vue from "eslint-plugin-vue";

/** @type {import('eslint').Linter.FlatConfig[]} */
export default [
  {
    files: ["**/*.{js,mjs,cjs,vue}"],
    languageOptions: {
      globals: { ...globals.browser, ...globals.node },
    },
  },
  js.configs.recommended,
  vue.configs.essential,
];
