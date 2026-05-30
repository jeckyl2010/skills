// ESLint flat config for Astro projects with TypeScript frontmatter
// Packages: eslint, eslint-plugin-astro, eslint-plugin-jsx-a11y, @typescript-eslint/parser
//
// This config handles:
//   - Astro-native rules via eslint-plugin-astro (flat/recommended)
//   - Accessibility rules via eslint-plugin-jsx-a11y (bundled in flat/recommended)
//   - TypeScript syntax in .astro frontmatter via @typescript-eslint/parser
//
// Without @typescript-eslint/parser, any .astro file using TypeScript syntax
// (interface declarations, 'as' casts, typed props) causes a parse error and
// masks all real findings with false-positive parser failures.

import eslintPluginAstro from 'eslint-plugin-astro';
import tsParser from '@typescript-eslint/parser';

export default [
  ...eslintPluginAstro.configs['flat/recommended'],

  {
    files: ['**/*.astro'],
    languageOptions: {
      parserOptions: {
        parser: tsParser,
        extraFileExtensions: ['.astro'],
      },
    },
    rules: {
      // XSS risk — only acceptable for hardcoded static SVG/HTML, not user input.
      // Downgrade to warn rather than error when set:html is used intentionally.
      'astro/no-set-html-directive':          'warn',
      'astro/no-unused-define-vars-in-style': 'error',
    },
  },

  {
    ignores: ['dist/**', 'node_modules/**'],
  },
];
