import Vue from 'vue'
import VueHtmlToPaper  from 'vue-html-to-paper'

const options = {
    name: '_blank',
    specs: [
      'titlebar=yes',
      'scrollbars=yes'
    ],
    styles: [
      'https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css',
      'vue-select/dist/vue-select.css'
    ],
    timeout: 1000, // default timeout before the print window appears
    autoClose: true, // if false, the window will not close after printing
  }

Vue.use(VueHtmlToPaper, options)