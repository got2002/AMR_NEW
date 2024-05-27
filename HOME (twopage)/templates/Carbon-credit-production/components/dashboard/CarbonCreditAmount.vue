<template>
	<div class="col-span-1 bg-white p-4 flex gap-3 shadow-sm rounded">
		<div class="w-20 h-20 rounded-sm flex items-center justify-center bg-tgo-teal-500 text-theme-white relative p-2">
			<p class="text-xl text-center font-semibold m-0 p-0">tCO<sub>2</sub>eq</p>
		</div>
		<div class="uppercase py-2 flex flex-col justify-center">
			<p class="text-xs text-gray-500">{{ title }}</p>
			<p class="text-2xl font-semibold text-theme-black-300">{{ value.toLocaleString() }}</p>
		</div>
	</div>
</template>

<script>
export default {
	props: {
		title: {
			type: String,
			default: () => "TITLE",
		},
		value: {
			type: Number,
			require: true,
		},
	},
};
</script>

<style>
</style>