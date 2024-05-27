<template>
	<div class="col-span-1 bg-theme-white p-4 flex gap-3 shadow-sm rounded-sm">
		<div class="w-16 h-16 rounded-sm bg-tgo-teal-500 text-white inline-flex justify-center items-center">
			<svg v-if="icon == 1" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-key" viewBox="0 0 16 16">
				<path d="M0 8a4 4 0 0 1 7.465-2H14a.5.5 0 0 1 .354.146l1.5 1.5a.5.5 0 0 1 0 .708l-1.5 1.5a.5.5 0 0 1-.708 0L13 9.207l-.646.647a.5.5 0 0 1-.708 0L11 9.207l-.646.647a.5.5 0 0 1-.708 0L9 9.207l-.646.647A.5.5 0 0 1 8 10h-.535A4 4 0 0 1 0 8zm4-3a3 3 0 1 0 2.712 4.285A.5.5 0 0 1 7.163 9h.63l.853-.854a.5.5 0 0 1 .708 0l.646.647.646-.647a.5.5 0 0 1 .708 0l.646.647.646-.647a.5.5 0 0 1 .708 0l.646.647.793-.793-1-1h-6.63a.5.5 0 0 1-.451-.285A3 3 0 0 0 4 5z" />
				<path d="M4 8a1 1 0 1 1-2 0 1 1 0 0 1 2 0z" />
			</svg>
			<svg v-else-if="icon == 2" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-check-circle" viewBox="0 0 16 16">
				<path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z" />
				<path d="M10.97 4.97a.235.235 0 0 0-.02.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-1.071-1.05z" />
			</svg>
			<svg v-else-if="icon == 3" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-dash-circle" viewBox="0 0 16 16">
				<path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z" />
				<path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 4 8z" />
			</svg>
		</div>
		<div class="uppercase py-2">
			<p class="text-xs text-theme-black-300">{{ title }}</p>
			<p class="text-2xl font-semibold text-theme-black-300">{{ value }}</p>
		</div>
	</div>
</template>

<script>
export default {
	props: {
		icon: {
			type: Number,
		},
		title: {
			type: String,
			default: () => "TITLE",
		},
		value: {
			type: Number,
			require: true,
		},
	},
};
</script>

<style>
</style>