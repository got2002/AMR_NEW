<template>
	<div class="flex w-full items-center border-2">
		<div class="2xl:w-3/12 xl:w-5/12  w-6/12 bg-gray-200 py-2 text-center">{{ label }} <span v-if="required" class="text-red-500">*</span></div>

		<!-- <select v-if="!disabled" ref="dropdown" :value="value" @input="$emit('input', $event.target.value)" class="px-3 py-1.5 bg-gray-50 w-9/12 text-center outline-none h-full">
			<slot name="options">
				<option v-for="item in options" :key="item.value" :value="item[valueAttr]">{{ item[textAttr] }}</option>
			</slot>
		</select> -->
		<div v-if="!disabled" class="2xl:w-9/12 xl:w-7/12  w-6/12">
			<UIDropdownSearch @input="$emit('input', $event)" :searchable="searchable" :value="value" :options="options" :valueAttr="valueAttr" :textAttr="textAttr" alignment="center"/>
		</div>
		<p v-else class="px-3 py-1.5 w-9/12 text-center">{{ options.find((item) => item?.value === value)?.text }}</p>
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
		valueAttr:{
			type: String,
			default: () => 'value',
		},
		textAttr:{
			type: String,
			default: () => 'text',
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