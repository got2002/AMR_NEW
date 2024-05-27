<template>
	<div class="flex w-full items-center">
		<div class="2xl:w-3/12 xl:w-5/12 w-6/12 bg-gray-200 px-3 py-2 border-2 text-center">{{ label }} <span v-if="required" class="text-red-500">*</span></div>
		<input :value="value" @input="$emit('input', $event.target.value)" class="2xl:w-9/12 xl:w-7/12 w-6/12 px-3 py-2 bg-gray-50 border-2 text-center outline-none" />
	</div>
</template>

<script>
export default {
	props: {
		value: String,
		label: String,
		required: {
			type: Boolean,
			default: () => false,
		},
		disabled: {
			type: Boolean,
			default: () => false,
		},
	},
};
</script>

<style>
</style>