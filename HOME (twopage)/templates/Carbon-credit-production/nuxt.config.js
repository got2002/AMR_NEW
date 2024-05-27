import locale_th from "./assets/locales/th/index";
import locale_en from "./assets/locales/en/index";
export default {
	// Global page headers: https://go.nuxtjs.dev/config-head
	dev: process.env.NODE_ENV !== "production",
	target: "static",
	head: {
		title: "TGO Carbon Registry System",
		htmlAttrs: {
			lang: "en",
		},
		meta: [{ charset: "utf-8" }, { name: "viewport", content: "width=device-width, initial-scale=1" }, { hid: "description", name: "description", content: "" }, { name: "format-detection", content: "telephone=no" }],
		link: [
			{ rel: "icon", type: "image/png", href: "/images/TGO_logo.png" },
			{ rel: "stylesheet", href: "https://fonts.googleapis.com/css2?family=Prompt&display=swap" },
			{ rel: "stylesheet", href: "//unpkg.com/leaflet/dist/leaflet.css" },
		],
		script: [
			{
				src: "https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.1/moment.min.js",
			},
			{
				src: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.js",

				// src: '@/static/leaflet/heatmap.min.js',
				// src: '@/static/leaflet/leaflet-heatmap.js',

				// src: '//unpkg.com/leaflet/dist/leaflet.js',
			},
		],
	},

	static: {
		prefix: false,
	},

	vue: {
		config: {
			productionTip: true,
			devtools: process.env.NODE_ENV !== "production",
		},
	},

	server: {
		port: 3000, // default: 3000
		host: "0.0.0.0", // default: localhost,
	},

	// Global CSS: https://go.nuxtjs.dev/config-css
	css: [
		{ src: "@/assets/css/main.css" },
		"@fortawesome/fontawesome-svg-core/styles.css",
		// 'leaflet-draw/dist/leaflet.draw.css'
	],

	// Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
	plugins: [
		{ src: "@/plugins/leaflet", ssr: false },
		"@/plugins/country-flag",
		"@/plugins/lodash",
		"@/plugins/v-select",
		"@/plugins/vue-the-mask",
		"@/plugins/vue-datepicker",
		"@/plugins/vuelidate",
		"@/plugins/vue-sweetalert2",
		"@/plugins/font-awesome.js",
		"@/plugins/vue-tailwind.js",
		"@/plugins/vue-js-modal.js",
		{ src: "~/plugins/vuex-persist.js", mode: "client" },

		{ src: "@/plugins/vue-pdf.js", mode: "client" },
		

		{ src: "@/plugins/vue-pdf-app.js", mode: "client" },
		{ src: "@/plugins/vue-html2pdf.js", mode: "client" },
		// '@/plugins/chart.js',
		// '@/plugins/vue-easy-lightbox.js',
		// '@/plugins/d3',
	],

	// Auto import components: https://go.nuxtjs.dev/config-components
	components: true,

	// Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
	buildModules: [
		// https://go.nuxtjs.dev/eslint
		"@nuxtjs/eslint-module",
		// https://go.nuxtjs.dev/tailwindcss
		"@nuxtjs/tailwindcss",
		"@nuxtjs/moment",
	],

	// Modules: https://go.nuxtjs.dev/config-modules
	modules: ["@nuxtjs/i18n", "@nuxtjs/auth-next", "@nuxtjs/axios", "@nuxtjs/toast", "vue-sweetalert2/nuxt", "@nuxtjs/dayjs"],
	// Optional
	dayjs: {
		locales: ["en", "th"],
		defaultLocale: "th",
		defaultTimeZone: "Asia/Bangkok",
		plugins: [
			"utc", // import 'dayjs/plugin/utc'
			"timezone", // import 'dayjs/plugin/timezone',
			"buddhistEra",
		], // Your Day.js plugin
	},

	router: {
		linkExactActiveClass: "bg-tgo-teal-500 text-white border-l-4 border-tgo-yellow-500",
	},
	i18n: {
		locales: ["en", "th"],
		defaultLocale: "th",
		vueI18n: {
			fallbackLocale: "th",
			messages: {
				en: locale_en,
				th: locale_th,
			},
		},
	},

	// Build Configuration: https://go.nuxtjs.dev/config-build
	build: {
		analyze: false,
		loaders: {
			vue: {
				prettify: false,
			},
		},
		// or
	},
	env: {
		baseUrl: process.env.BASE_URL || "http://localhost:3002",
	},
	rules: {
		"vue/multi-word-component-names": 0,
	},
	axios: {
		credentials: false,
		baseURL: process.env.BASE_URL || "http://localhost:3001",
	},
	auth: {
		redirect: {
			login: "/auth/signin",
			home: "/",
			logout: "/",
			callback: false, // not used here in our case
		},
		cookie: false,
		strategies: {
			// 'laravelJWT': {
			//     provider: 'laravel/jwt',
			//     url: process.env.BASE_URL || "http://localhost:3001",
			//     endpoints: {
			//         login: { url: '/api/v1/auth/login', method: 'post' },
			//         logout: { url: '/api/v1/auth/logout', method: 'post' },
			//         user: { url: '/api/v1/auth/me', method: 'get' }
			//     },
			//     token: {
			//         property: 'access_token',
			//         maxAge: 1800,
			//         global: true,
			//         // type: 'Bearer'
			//     },
			//     refreshToken: {
			//         property: 'refresh_token',
			//         data: 'refresh_token',
			//         maxAge: 60 * 60 * 24 * 30
			//     },
			// },

			local: {
				token: {
					property: "token",
					global: true,
					maxAge: false,
					// required: true,
					// type: 'Bearer'
				},
				user: {
					property: false,
					// autoFetch: true
				},
				url: process.env.BASE_URL || "http://localhost:3002",
				endpoints: {
					login: { url: "/api/v1/auth/login", method: "post" },
					logout: { url: "/api/v1/auth/logout", method: "post" },
					user: { url: "/api/v1/auth/me", method: "get" },
				},
			},
		},
	},
	toast: {
		position: "top-center",
	},
};
