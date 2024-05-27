<template>
	<td
		class="border-t-0 whitespace-nowrap align-center "
		:class="{
			'text-left': align === 'left',
			'text-center': align === 'center',
			'text-right': align === 'right',
			
		}"
	>
		<slot name="data">{{ text }}</slot>
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
			classes:{
				type: String,
				default: "",
			}
			
		},
	};
</script>

<style></style>
