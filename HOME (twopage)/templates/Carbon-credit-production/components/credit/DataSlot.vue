<template>
	<td
		class="border-t-0 px-1 align-center "
		:class="{
			'text-left': align === 'left',
			'text-center': align === 'center',
			'text-right': align === 'right',
			
		}"
	>
		<slot>{{ text }}</slot>
	</td>
</template>

<script>
	export default {
		props: {
			text: [String,Number],
			align: {
				type: String,
				default: "left",
			},
			
		},
	};
</script>

<style></style>
