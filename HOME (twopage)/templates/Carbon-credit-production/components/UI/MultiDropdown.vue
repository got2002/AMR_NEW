<template>
	<t-select :value="value" @input="$emit('input', $event)" :classes="classes" :fixedClasses="fixedClasses" multiple :options="options" :closeOnSelect="false" :hideSearchBox="true" valueAttribute="value" textAttribute="text">
		<template v-slot:label>
			<div class="w-full flex items-center gap-2">
				<div class="px-2 py-0.5 text-sm bg-tgo-teal-500 rounded-sm shadow flex items-center gap-2" v-for="(tag, i) in value" :key="i">
					<ShowroomLeafIcon v-if="tag === 'env'" />

					<ShowroomUserIcon v-else-if="tag === 'social'" />
					<ShowroomCloudMoneyIcon v-else />
					<span class="text-white">{{ options.find((item) => item.value === tag).text }}</span>
				</div>
			</div>
		</template>

		<template v-slot:option="{ isSelected, option }">
			<div class="px-3 py-1 flex items-center gap-2" :class="{ 'bg-tgo-teal-300': isSelected }">
				<ShowroomLeafIcon color="#000" v-if="option.raw.value === 'env'" />

				<ShowroomUserIcon color="#000" v-else-if="option.raw.value === 'social'" />
				<ShowroomCloudMoneyIcon color="#000" v-else />
				<span class="text-sm">{{ option.raw.text }}</span>
			</div>
		</template>
	</t-select>
</template>

<script>
export default {
	props: {
		value: Array,
		options: Array,
	},
	data() {
		return {
			classes: {
				wrapper: "",
				buttonWrapper: "",
				selectButton: "px-4 py-2  text-black transition duration-100 ease-in-out bg-white border border-gray-300 outline-none disabled:opacity-50 disabled:cursor-not-allowed",
				selectButtonLabel: "",
				selectButtonTagWrapper: "-mx-2 -my-2.5 py-1 pr-8",
				selectButtonTag: "bg-tgo-teal-500 block duration-100 ease-in-out  rounded shadow-sm text-xs text-white overflow-hidden  flex items-center",
				selectButtonTagText: "px-3",
				selectButtonTagDeleteButton: "-ml-1.5 h-full hover:bg-tgo-teal-600 hover:shadow-sm inline-flex items-center px-2 transition",
				selectButtonTagDeleteButtonIcon: "",
				selectButtonPlaceholder: "text-gray-400",
				selectButtonIcon: "text-gray-600",
				selectButtonClearButton: "hover:bg-blue-100 text-gray-600 rounded transition duration-100 ease-in-out",
				selectButtonClearIcon: "",
				dropdown: "-mt-1 bg-white border-b border-gray-300 border-l border-r rounded-b shadow-sm",
				dropdownFeedback: "pb-2 px-3 text-gray-400 text-sm",
				loadingMoreResults: "pb-2 px-3 text-gray-400 text-sm",
				optionsList: "",
				searchWrapper: "p-2 placeholder-gray-400",
				searchBox: "px-3 py-2 bg-gray-50 text-sm rounded border focus:outline-none focus:shadow-outline border-gray-300",
				optgroup: "text-gray-400 uppercase text-xs py-1 px-2 font-semibold",
				option: "",
				disabledOption: "",
				highlightedOption: "bg-blue-100",
				selectedOption: "font-semibold bg-gray-100 bg-blue-500 font-semibold text-white",
				selectedHighlightedOption: "font-semibold bg-gray-100 bg-blue-600 font-semibold text-white",
				optionContent: "flex justify-between items-center px-3 py-2",
				optionLabel: "",
				selectedIcon: "",
				enterClass: "opacity-0",
				enterActiveClass: "transition ease-out duration-100",
				enterToClass: "opacity-100",
				leaveClass: "opacity-100",
				leaveActiveClass: "transition ease-in duration-75",
				leaveToClass: "opacity-0",
			},
			fixedClasses: {
				wrapper: "relative",
				buttonWrapper: "inline-block relative w-full",
				selectButton: "w-full flex text-left justify-between items-center rounded",
				selectButtonLabel: "block truncate",
				selectButtonTagWrapper: "flex flex-wrap overflow-hidden",
				selectButtonTag: "bg-blue-500 block disabled:cursor-not-allowed disabled:opacity-50 duration-100 ease-in-out focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 rounded shadow-sm text-sm text-white transition white-space-no m-0.5 max-w-full overflow-hidden h-8 flex items-center",
				selectButtonTagText: "px-3",
				selectButtonTagDeleteButton: "-ml-1.5 h-full hover:bg-blue-600 hover:shadow-sm inline-flex items-center px-2 transition",
				selectButtonTagDeleteButtonIcon: "w-3 h-3",
				selectButtonPlaceholder: "block truncate",
				selectButtonIcon: "fill-current flex-shrink-0 ml-1 h-4 w-4",
				selectButtonClearButton: "flex flex-shrink-0 items-center justify-center absolute right-0 top-0 m-2 h-6 w-6",
				selectButtonClearIcon: "fill-current h-3 w-3",
				dropdown: "absolute w-full z-50 divide-y",
				dropdownFeedback: "",
				loadingMoreResults: "",
				optionsList: "overflow-auto",
				searchWrapper: "inline-block w-full",
				searchBox: "inline-block w-full",
				optgroup: "",
				option: "cursor-pointer",
				disabledOption: "opacity-50 cursor-not-allowed",
				highlightedOption: "cursor-pointer",
				selectedOption: "cursor-pointer",
				selectedHighlightedOption: "cursor-pointer",
				optionContent: "",
				optionLabel: "truncate block",
				selectedIcon: "fill-current h-4 w-4",
				enterClass: "",
				enterActiveClass: "",
				enterToClass: "",
				leaveClass: "",
				leaveActiveClass: "",
				leaveToClass: "",
			},
		};
	},
};
</script>

<style>
</style>