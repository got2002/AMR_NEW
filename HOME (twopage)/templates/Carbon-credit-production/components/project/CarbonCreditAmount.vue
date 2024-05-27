<template>
	<div class="col-span-1 bg-white p-4 flex gap-3 shadow-sm rounded">
		<div class="w-16 h-16 rounded-sm bg-tgo-teal-500 text-white inline-flex justify-center items-center">
			<svg v-if="icon == 1" width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
				<path d="M17.593 3.32206C18.693 3.45006 19.5 4.39906 19.5 5.50706V21.0001L12 17.2501L4.5 21.0001V5.50706C4.5 4.39906 5.306 3.45006 6.407 3.32206C10.1232 2.89069 13.8768 2.89069 17.593 3.32206V3.32206Z" stroke="#F9F9F9" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
			</svg>
			<svg v-else-if="icon == 2" width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
				<path d="M9 12.75L11.25 15L15 9.75M21 12C21 13.1819 20.7672 14.3522 20.3149 15.4442C19.8626 16.5361 19.1997 17.5282 18.364 18.364C17.5282 19.1997 16.5361 19.8626 15.4442 20.3149C14.3522 20.7672 13.1819 21 12 21C10.8181 21 9.64778 20.7672 8.55585 20.3149C7.46392 19.8626 6.47177 19.1997 5.63604 18.364C4.80031 17.5282 4.13738 16.5361 3.68508 15.4442C3.23279 14.3522 3 13.1819 3 12C3 9.61305 3.94821 7.32387 5.63604 5.63604C7.32387 3.94821 9.61305 3 12 3C14.3869 3 16.6761 3.94821 18.364 5.63604C20.0518 7.32387 21 9.61305 21 12Z" stroke="#F9F9F9" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
			</svg>
			<svg v-else-if="icon == 3" width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
				<path d="M12 9V12.75M21 12C21 13.1819 20.7672 14.3522 20.3149 15.4442C19.8626 16.5361 19.1997 17.5282 18.364 18.364C17.5282 19.1997 16.5361 19.8626 15.4442 20.3149C14.3522 20.7672 13.1819 21 12 21C10.8181 21 9.64778 20.7672 8.55585 20.3149C7.46392 19.8626 6.47177 19.1997 5.63604 18.364C4.80031 17.5282 4.13738 16.5361 3.68508 15.4442C3.23279 14.3522 3 13.1819 3 12C3 9.61305 3.94821 7.32387 5.63604 5.63604C7.32387 3.94821 9.61305 3 12 3C14.3869 3 16.6761 3.94821 18.364 5.63604C20.0518 7.32387 21 9.61305 21 12ZM12 15.75H12.008V15.758H12V15.75Z" stroke="#F9F9F9" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
			</svg>
			<svg v-else width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
				<path d="M18.3641 18.3641C20.0519 16.6762 21.0001 14.387 21.0001 12.0001C21.0001 9.61309 20.0519 7.32389 18.3641 5.63606C16.6762 3.94822 14.387 3 12.0001 3C9.61309 3 7.32389 3.94822 5.63606 5.63606M18.3641 18.3641C16.6762 20.0519 14.387 21.0001 12.0001 21.0001C9.61309 21.0001 7.32389 20.0519 5.63606 18.3641C3.94822 16.6762 3 14.387 3 12.0001C3 9.61309 3.94822 7.32389 5.63606 5.63606M18.3641 18.3641L5.63606 5.63606" stroke="#F9F9F9" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
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