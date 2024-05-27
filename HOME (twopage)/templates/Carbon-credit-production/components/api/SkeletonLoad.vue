<template>
	<div class="w-7/12 border-r-2 pr-4 text-sm">
		<div class="flex justify-between mt-5">
			<div class="flex flex-col justify-center">
				<div data-placeholder class="h-3 w-60 rounded-full overflow-hidden relative bg-gray-200"></div>
			</div>
			<div data-placeholder class="h-14 w-1/2 overflow-hidden relative bg-gray-200"></div>
		</div>
		<div class="flex justify-between mt-5">
			<div class="flex flex-col justify-center">
				<div data-placeholder class="h-3 w-60 rounded-full overflow-hidden relative bg-gray-200"></div>
			</div>
			<div data-placeholder class="h-14 w-1/2 overflow-hidden relative bg-gray-200"></div>
		</div>
		<div class="flex justify-between mt-5">
			<div class="flex flex-col justify-center">
				<div data-placeholder class="h-3 w-60 rounded-full overflow-hidden relative bg-gray-200"></div>
			</div>
			<div data-placeholder class="h-14 w-1/2 overflow-hidden relative bg-gray-200"></div>
		</div>
		<div class="flex justify-between mt-5">
			<div class="flex flex-col justify-center">
				<div data-placeholder class="h-3 w-60 rounded-full overflow-hidden relative bg-gray-200"></div>
			</div>
			<div data-placeholder class="h-14 w-1/2 overflow-hidden relative bg-gray-200"></div>
		</div>

		<div class="flex justify-between mt-5">
			<div class="flex flex-col justify-center">
				<div data-placeholder class="h-3 w-60 rounded-full overflow-hidden relative bg-gray-200"></div>
			</div>
			<div data-placeholder class="h-14 w-1/2 overflow-hidden relative bg-gray-200"></div>
		</div>

		<div class="flex mt-5">
			<div class="flex flex-col w-1/2 justify-start">
				<div data-placeholder class="h-3 w-60 rounded-full overflow-hidden relative bg-gray-200"></div>
			</div>
			<div class="w-1/2">
				<div class="flex items-center mt-2" v-for="i in 10" :key="i">
					<div data-placeholder class="h-8 w-8 overflow-hidden relative bg-gray-200 mr-2"></div>
					<div class="flex flex-col justify-center">
						<div data-placeholder class="h-3 w-60 rounded-full overflow-hidden relative bg-gray-200 mb-2"></div>
						<div data-placeholder class="h-3 w-20 rounded-full overflow-hidden relative bg-gray-200"></div>
						<!-- <div class="text-sm text-gray-500">{{ permission.description }}</div> -->
					</div>
				</div>
			</div>
		</div>
	</div>
	
</template>

<script>
export default {};
</script>

<style>
[data-placeholder]::after {
	content: " ";
	box-shadow: 0 0 50px 9px rgb(255, 255, 255);
	position: absolute;
	top: 0;
	left: -100%;
	height: 100%;
	animation: load 2s infinite;
}
@keyframes load {
	0% {
		left: -100%;
	}
	100% {
		left: 150%;
	}
}
</style>