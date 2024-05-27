<template>
	<td
		class="border-t-0 p-2 whitespace-nowrap align-center "
		:class="{
			'text-left': align === 'left',
			'text-center': align === 'center',
			'text-right': align === 'right',
		}"
	>
		<p class="font-bold text-xs mb-1">{{ userId }}</p>
		<div class="text-xs text-gray-500 ">{{ name }}</div>
	</td>
</template>

<script>
	export default {
		props: {
			name: {
				type: String,
			},
			userId: {
				type: String,
			},
			align: {
				type: String,
				default: "left",
			},
		},
	};
</script>

<style></style>
