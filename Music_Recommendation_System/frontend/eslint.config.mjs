import globals from "globals";
import pluginJs from "@eslint/js";
import pluginVue from "eslint-plugin-vue";
import babelParser from "@babel/eslint-parser";

/** @type {import('eslint').Linter.FlatConfig[]} */
export default [
  {
    files: ["**/*.{js,mjs,cjs,vue}"], // Target JavaScript and Vue files
    languageOptions: {
      parser: babelParser, // Use Babel parser
      globals: { ...globals.browser, ...globals.node },
      parserOptions: {
        requireConfigFile: false, // Required for @babel/eslint-parser
        ecmaVersion: "latest", // Use the latest ECMAScript standard
        sourceType: "module", // Use ES modules
      },
    },
    rules: {
      "no-console": "warn",
      "no-debugger": "warn",
    },
  },
  // JavaScript recommended rules
  pluginJs.configs.recommended,
  // Vue essential rules
  ...pluginVue.configs["flat/essential"],
];
