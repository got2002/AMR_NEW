module.exports = {
	purge: [],
	darkMode: false, // or 'media' or 'class'
	theme: {
		extend: {
			colors: {
				status: {
					DEFAULT: "#C14D0C",
					true: "#96C8BE",
				},

				carbon: {
					"sorf-dark": "#525152",
					dark: "#343434",
					darker: "#252525",
					green: "#4CA365",
					"green-logo": "#c9da2a",
					"blue-logo": "#00b0d8",
				},

				stone: {
					100: "#e3e3e3",
					200: "#c7c7c7",
					300: "#ababab",
					400: "#8f8f8f",
					500: "#737373",
					600: "#5c5c5c",
					700: "#454545",
					800: "#2e2e2e",
					900: "#171717",
				},

				"tgo-yellow": {
					100: "#f4f8d4",
					200: "#e9f0aa",
					300: "#dfe97f",
					400: "#d4e155",
					500: "#c9da2a",
					600: "#a1ae22",
					700: "#798319",
					800: "#505711",
					900: "#282c08",
				},
				"tgo-teal": {
					100: "#cceff7",
					200: "#99dfef",
					300: "#66d0e8",
					400: "#33c0e0",
					500: "#00b0d8",
					600: "#008dad",
					700: "#006a82",
					800: "#004656",
					900: "#00232b",
				},
				theme: {
					white: "#F9F9F9",
					black: {
						50: "#EEEEEE",
						100: "#555555",
						200: "#343434",
						300: "#252525",
					},
					brown: {
						100: "#D1C7C1",
						200: "#9B928D",
						300: "#766962",
					},
					green: {
						100: "#D4EBD9",
						200: "#56BA71",
						300: "#c9da2a",
					},
				},
			},
			spacing: {
				128: "32rem",
			},
		},
	},
	variants: {
		extend: {},
	},
	plugins: [
		// require('tailwind-accent-color')(),
	],
};
