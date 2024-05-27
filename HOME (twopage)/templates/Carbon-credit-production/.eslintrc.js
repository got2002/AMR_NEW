module.exports = {
  root: true,
  env: {
    browser: true,
    node: true,
  },
  parserOptions: {
    parser: '@babel/eslint-parser',
    requireConfigFile: false,
  },
  extends: ['@nuxtjs', 'plugin:nuxt/recommended', 'prettier'],
  plugins: [],
  // add your custom rules here
  rules: {
    "no-console": 0,
    "vue/multi-word-component-names": 0,
    "object-shorthand": 0,
    "new-cap": 0,
    "prefer-const":0,
    "no-var":0,
    "no-unused-vars":0,
    "vue/no-mutating-props":0,
    "no-lonely-if":0
  },
}
