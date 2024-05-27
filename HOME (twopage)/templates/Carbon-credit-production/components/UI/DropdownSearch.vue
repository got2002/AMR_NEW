<template>
	<div class="relative w-full" v-clickOutside="() => (drop = false)">
		<div @click="openDropdown" :class="{ 'bg-gray-100 text-gray-400': disabled, 'bg-transparent': !disabled }" class="px-3 py-2 text-center outline-none h-full truncate overflow-x-hidden flex w-full">
			<!-- <span :title="textValue()">{{ textValue() }}</span> -->
			<input type="text" :value="textValue" disabled :class="classes" />
			<IconArrowDown class="transform" :class="{ '-rotate-180 duration-200': drop && !disabled, 'right-0 duration-200': !drop && !disabled }" />
		</div>
		<div v-show="drop && !disabled" id="dropdowns" class="w-full absolute left-0" :class="{ 'top-10': !overScreen, 'bottom-10': overScreen }" style="z-index: 1000">
			<div data-aos="fade-down" data-aos-anchor-placement="top-center" class="w-full min-w-full bg-white shadow-md border border-gray-300">
				<div class="p-2" v-if="searchable">
					<UISearch @keyup="filterOptions" v-model="search" />
				</div>
				<div v-if="valueAttr !== '' && textAttr !== ''" class="divide-y overflow-y-auto max-h-60">
					<div @click="selectValue(item)" v-for="(item, i) in filteredOptions" :key="i" class="px-4 py-2 hover:bg-gray-100 cursor-pointer truncate text-sm w-full overflow-x-hidden font-thin" :title="item[textAttr]">{{ item[textAttr] }}</div>
				</div>
				<div v-else class="divide-y overflow-y-auto max-h-60">
					<div @click="selectValue(item)" v-for="(item, i) in filteredOptions" :key="i" class="px-4 py-2 hover:bg-gray-100 cursor-pointer truncate text-sm w-full overflow-x-hidden font-thin" :title="item">{{ item }}</div>
				</div>
				<div v-if="tmpOptions.length === 0" class="px-8 py-4 bg-gray-50 text-center text-gray-500 m-2">{{ $t("no_data") }}</div>
			</div>
		</div>
	</div>
</template>

<script>
import vClickOutside from "v-click-outside";
import AOS from "aos";
import "aos/dist/aos.css";
export default {
	directives: {
		clickOutside: vClickOutside.directive,
	},
	props: {
		value: {
			default: () => null,
		},

		options: { type: Array, default: () => [] },
		valueAttr: {
			type: String,
			default: () => "value",
		},
		textAttr: {
			type: String,
			default: () => "text",
		},
		searchable: {
			type: Boolean,
			default: () => true,
		},
		disabled: {
			type: Boolean,
			default: () => false,
		},
		alignment: {
			type: String,
			default: () => "left",
		},
	},
	computed: {
		classes() {
			let class_ = "bg-transparent outline-none w-full cursor-pointer";
			if (this.alignment === "left") class_ += " text-left";
			else if (this.alignment === "center") class_ += " text-center";
			else if (this.alignment === "right") class_ += " text-right";
			return class_;
		},
		textValue() {
			if (this.value === null || this.value === undefined || this.value === "") return `--- ${this.$t("select")} ---`;
			else {
				if (this.valueAttr !== "" && this.textAttr !== "") {
					const findValue = this.options.find((item) => item[this.valueAttr] === this.value);
					if (findValue) {
						return findValue[this.textAttr];
					} else return null;
				} else {
					const findValue = this.options.find((item) => item === this.value);
					if (findValue) {
						return findValue;
					} else return null;
				}
			}
		},

		filteredOptions() {
			if (this.valueAttr !== "" && this.textAttr !== "") {
				const filterOptions = this.options.filter((item) => item[this.textAttr].toLowerCase().includes(this.search.toLowerCase()));
				// console.log(filterOptions);
				return filterOptions;
			} else {
				const filterOptions = this.options.filter((item) => item.includes(this.search));
				// console.log(filterOptions);
				return filterOptions;
			}
		},
	},
	data() {
		return {
			tmpOptions: this.options,
			drop: false,
			search: "",
			overScreen: false,
		};
	},

	updated() {
		if (this.$refs.dropdown) {
			// console.log(this.options);
			// console.log(this.options);
			this.$refs.dropdown.value = this.value;
		}
		if (this.options?.length > 0) {
			this.tmpOptions = this.options;
		}
	},
	watch: {
		drop(value) {
			this.filterOptions(this.search);
		},
		"options.length"(value) {
			if (value > 0) {
				this.tmpOptions = this.options;
			}
		},
	},
	mounted() {
		AOS.init();
	},
	methods: {
		openDropdown(e) {
			// console.log(e);
			if (this.disabled) {
				this.drop = false;
				return;
			}
			this.drop = !this.drop;

			if (e.y + 350 >= window.innerHeight) {
				// console.log(e.y + 350, window.innerHeight);
				this.overScreen = true;
			} else {
				// console.log(e.y, window.innerHeight, "sss");
				this.overScreen = false;
			}
		},
		filterOptions(value) {
			if (this.valueAttr !== "" && this.textAttr !== "") {
				const filterOptions = this.options.filter((item) => item[this.textAttr].toLowerCase().includes(value.toLowerCase()));
				// console.log(filterOptions);
				this.tmpOptions = filterOptions;
			} else {
				const filterOptions = this.options.filter((item) => item.includes(value));
				// console.log(filterOptions);
				this.tmpOptions = filterOptions;
			}
		},
		selectValue(item) {
			// console.log(item[this.valueAttr]);
			// this.search = item[this.textAttr]

			this.drop = false;
			if (this.valueAttr !== "" && this.textAttr !== "") this.$emit("input", item[this.valueAttr]);
			else this.$emit("input", item);
		},
		// textValue() {
		// 	if (this.value === null || this.value === undefined || this.value === "") return `--- ${this.$t("select")} ---`;
		// 	else {
		// 		if (this.valueAttr !== "" && this.textAttr !== "") {
		// 			const findValue = this.options.find((item) => item[this.valueAttr] === this.value);
		// 			if (findValue) {
		// 				return findValue[this.textAttr];
		// 			} else return null;
		// 		} else {
		// 			const findValue = this.options.find((item) => item === this.value);
		// 			if (findValue) {
		// 				return findValue;
		// 			} else return null;
		// 		}
		// 	}
		// },
	},
};
</script>

<style>
</style>