<template>
	<div class="flex w-full items-center border-2" id="project_search_dropdown_input">
		<div class="w-3/12 bg-gray-200 px-3 py-2 text-center">{{ label }} <span v-if="required" class="text-red-500">*</span></div>
		<div v-if="!disabled" class="w-9/12">
			<UIDropdownSearch @input="$emit('input', $event)" :value="value" :options="options" :valueAttr="valueAttr" :textAttr="textAttr" alignment="center"/>
		</div>

		<div v-else class="px-3 py-1.5 w-9/12 text-center">{{ options.find((item) => item?.value === value)?.text }}</div>
	</div>
</template>

<script>
export default {
	props: {
		value: {
			default: () => "",
		},
		label: String,
		options: { type: Array, default: () => [] },
		required: {
			type: Boolean,
			default: () => false,
		},
		disabled: {
			type: Boolean,
			default: () => false,
		},
		valueAttr: {
			type: String,
			default: () => "value",
		},
		textAttr: {
			type: String,
			default: () => "text",
		},
		searchable:{
			type: Boolean,
			default: () => true,
		}
	},

	updated() {
		if (this.$refs.dropdown) {
			this.$refs.dropdown.value = this.value;
		}
	},
};
</script>

<style>
</style>