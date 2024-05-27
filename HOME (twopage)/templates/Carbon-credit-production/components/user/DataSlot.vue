<template>
	<td
		class="border-t-0 px-3 whitespace-nowrap align-center "
		:class="{
			'text-left': align === 'left',
			'text-center': align === 'center',
			'text-right': align === 'right',
			
		}"
	>
		{{ text }}
	</td>
</template>

<script>
	export default {
		props: {
			text: {
				
			},
			align: {
				type: String,
				default: "left",
			},
			
		},
	};
</script>

<style></style>
