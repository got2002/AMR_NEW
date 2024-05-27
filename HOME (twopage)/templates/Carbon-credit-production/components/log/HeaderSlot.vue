<template>
	<th class="px-3 bg-tgo-teal-500 text-sm font-medium text-white align-middle py-3 " :class="{ 'text-left': align == 'left', 'text-center': align == 'center' }">
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
.text-shadow-sm{
	text-shadow: 0.5px 0.5px #555555;
}
.text-shadow-sm{
	text-shadow: 2px 2px #555555;
}
.text-shadow-lg{
	text-shadow: 4px 4px #555555;
}
</style>