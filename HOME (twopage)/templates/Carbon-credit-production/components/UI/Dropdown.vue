<template>
	<div id="user-input">
		<v-select ref="dropdown" :disabled="disabled" :options="option" :reduce="(item) => item[valueAttr]" :label="labelAttr" :value="value" @input="$emit('input', $event)" />
	</div>
</template>

<script>
export default {
	props: {
		value: [String, Number],
		option: Array,
		labelAttr: {
			type: String,
			default: () => "text",
		},
		valueAttr:{
			type: [String, Number],
			default: () => "value",
		},
		disabled:{
			type: Boolean,
			default: () => false,
		}
	},
	updated() {
		// console.log();
		this.$refs.dropdown.value = this.value;
	},
	methods: {
		test(e) {
			console.log(e);
		},
	},
};
</script>

<style>
#user-input .vs__dropdown-toggle {
	-webkit-appearance: none;
	-moz-appearance: none;
	appearance: none;
	background: #f9fafb;

	border: 1px solid rgba(60, 60, 60, 0.26) !important;

	border-radius: 4px !important;

	display: flex;
	align-items: center;
	padding: 6px 4px 6px 4px !important;
	white-space: normal;
}
</style>