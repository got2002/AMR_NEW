<template>
	<div class="relative">
		<div class="w-full flex items-center bg-white border rounded">
			<div class="bg-gray-300 py-2 px-4">Min</div>
			<UINumberInput customClass="p-2 w-full outline-none text-center" type="number" v-model.number="value.min" :min="0" :max="value.max"/>
			<div class="bg-gray-300 py-2 px-4">Max</div>
			<UINumberInput customClass="p-2 w-full outline-none text-center" type="number" v-model.number="value.max" :min="value.min" :max="500"/>
		</div>
	</div>
</template>

<script>
export default {
	props: {
		value: Object,
		type: {
			type: String,
			default: () => "text",
		},
	},
};
</script>

<style>
</style>