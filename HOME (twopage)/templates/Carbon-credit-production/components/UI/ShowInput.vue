<template>
	<p class="px-2 py-2 h-10 border border-gray-300 w-full rounded outline-none focus:border-green-500 bg-gray-50">{{ value }}</p>
</template>

<script>
export default {
	props: {
		value:{
			default:()=>''
		},
		
	},
};
</script>

<style>
</style>