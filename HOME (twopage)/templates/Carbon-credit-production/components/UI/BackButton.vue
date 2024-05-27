<template>
	<button @click="$emit('click')" :class="`bg-gray-300 border border-gray-400 rounded shadow-sm hover:bg-gray-400 ${padding} hover:text-gray-100`">
		<slot>Click Me</slot>
	</button>
</template>

<script>
export default {
	props:{
		padding:{
			type:String,
			default:()=>'px-4'
		}
	}
};
</script>

<style>
</style>