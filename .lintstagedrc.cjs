module.exports = {
  "**/*.{css,scss}": [
    "stylelint --fix --color"
  ],
  "**/*.ts": [
    "eslint --fix",
    // https://github.com/okonet/lint-staged#example-run-tsc-on-changes-to-typescript-files-but-do-not-pass-any-filename-arguments
    () => 'tsc --noEmit',
  ],
  "**/*.js": [
    "eslint --fix"
  ]
}
