<template>
	<th class="px-3 bg-tgo-teal-500 text-sm font-medium text-gray-200 align-middle py-3 " :class="{ 'text-left': align == 'left', 'text-center': align == 'center' }">
		{{ text }}
	</th>
</template>

<script>
export default {
	props: {
		text: {
			type: String,
			required: true,
		},
		align: {
			type: String,
			required: true,
		},
		
	},
};
</script>
<style>

</style>