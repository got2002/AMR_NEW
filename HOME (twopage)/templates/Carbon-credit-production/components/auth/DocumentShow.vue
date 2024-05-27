<template>
	<div @click="$emit('click')" class="w-full p-2 rounded border bg-gray-100 border-gray-500 flex items-center gap-2 cursor-pointer hover:bg-gray-200">
		<div class="w-8 h-8 rounded-full bg-gray-500 text-white flex items-center justify-center">
			<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
				<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
			</svg>
		</div>
		<p class="text-sm w-3/4 truncate">{{ document.name }}</p>
	</div>
</template>

<script>
export default {
	props: ["document"],
};
</script>

<style>
</style>