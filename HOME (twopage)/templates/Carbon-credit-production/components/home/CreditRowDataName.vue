<template>
	<td class="border-t-0 px-1 whitespace-nowrap align-center">
		<div class="w-full flex flex-col items-center justify-start">
			<div class="w-80 text-center">
				<p :title="text" class="truncate font-bold cursor-pointer">{{ text }}</p>
				<p class="text-xs text-gray-500">{{ sub_text }}</p>
			</div>
		</div>
	</td>
</template>

<script>
	export default {
		props: {
			text: {},
			sub_text: {},
			align: {
				type: String,
				default: "left",
			},
		},
	};
</script>

<style></style>
