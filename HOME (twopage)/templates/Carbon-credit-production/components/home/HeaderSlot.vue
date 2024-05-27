<template>
	<th class="text-sm font-medium align-middle whitespace-nowrap p-3 " 
	:class="{
		'text-left':header.align === 'left',
		'text-center':header.align === 'center',
		'text-right':header.align === 'right',
	}">
		{{ header.name }}
	</th>
</template>

<script>
	export default {
		props: {
			header: {
				type: Object,
				require: true,
			},
		},
	};
</script>

<style></style>
