<template>
	<div class="relative">
		<div @click="$emit('click')" class="w-full text-center py-2 border border-gray-300 rounded outline-none hover:border-green-500 bg-gray-50">{{ min }} - {{ max }}</div>
        <slot name="config"></slot>
	</div>
</template>

<script>
export default {
	props: {
		max: Number,
		min: Number,
		type: {
			type: String,
			default: () => "text",
		},
	},
	
};
</script>

<style>
</style>