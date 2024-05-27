<template>
	<div class="grid grid-cols-12 gap-4 bg-white shadow-sm rounded p-4 text-sm">
		<div class="col-span-6">
			<div data-placeholder class="h-3 w-20 rounded-full overflow-hidden relative bg-gray-200 mb-2"></div>
			<div data-placeholder class="h-8 w-full overflow-hidden relative bg-gray-200"></div>
		</div>
		<div class="col-span-6">
			<div data-placeholder class="h-3 w-20 rounded-full overflow-hidden relative bg-gray-200 mb-2"></div>
			<div data-placeholder class="h-8 w-full overflow-hidden relative bg-gray-200"></div>
		</div>
		<div class="col-span-12">
			<div data-placeholder class="h-3 w-20 rounded-full overflow-hidden relative bg-gray-200 mb-2"></div>
			<div class="flex gap-4">
				<div data-placeholder class="h-8 w-20 overflow-hidden relative bg-gray-200"></div>
				<div data-placeholder class="h-8 w-40 overflow-hidden relative bg-gray-200"></div>
			</div>
		</div>
		<div class="col-span-12">
			<div data-placeholder class="h-3 w-20 rounded-full overflow-hidden relative bg-gray-200 mb-2"></div>
			<div data-placeholder class="h-8 w-full overflow-hidden relative bg-gray-200"></div>
		</div>
		<div class="col-span-5">
			<div data-placeholder class="h-3 w-20 rounded-full overflow-hidden relative bg-gray-200 mb-2"></div>
			<div data-placeholder class="h-8 w-full overflow-hidden relative bg-gray-200"></div>
		</div>
		<div class="col-span-5">
			<div data-placeholder class="h-3 w-20 rounded-full overflow-hidden relative bg-gray-200 mb-2"></div>
			<div data-placeholder class="h-8 w-full overflow-hidden relative bg-gray-200"></div>
		</div>
		<div class="col-span-2">
			<div data-placeholder class="h-3 w-20 rounded-full overflow-hidden relative bg-gray-200 mb-2"></div>
			<div data-placeholder class="h-8 w-full overflow-hidden relative bg-gray-200"></div>
		</div>

		<div class="col-span-4">
			<div data-placeholder class="h-3 w-20 rounded-full overflow-hidden relative bg-gray-200 mb-2"></div>
			<div data-placeholder class="h-8 w-full overflow-hidden relative bg-gray-200"></div>
		</div>
		<div class="col-span-4">
			<div data-placeholder class="h-3 w-20 rounded-full overflow-hidden relative bg-gray-200 mb-2"></div>
			<div data-placeholder class="h-8 w-full overflow-hidden relative bg-gray-200"></div>
		</div>
		<div class="col-span-4">
			<div data-placeholder class="h-3 w-20 rounded-full overflow-hidden relative bg-gray-200 mb-2"></div>
			<div data-placeholder class="h-8 w-full overflow-hidden relative bg-gray-200"></div>
		</div>

		<div class="col-span-4">
			<div data-placeholder class="h-3 w-20 rounded-full overflow-hidden relative bg-gray-200 mb-2"></div>
			<div data-placeholder class="h-8 w-full overflow-hidden relative bg-gray-200"></div>
		</div>
		<div class="col-span-4">
			<div data-placeholder class="h-3 w-20 rounded-full overflow-hidden relative bg-gray-200 mb-2"></div>
			<div data-placeholder class="h-8 w-full overflow-hidden relative bg-gray-200"></div>
		</div>
		<div class="col-span-4">
			<div data-placeholder class="h-3 w-20 rounded-full overflow-hidden relative bg-gray-200 mb-2"></div>
			<div data-placeholder class="h-8 w-full overflow-hidden relative bg-gray-200"></div>
		</div>

		<div class="col-span-4">
			<div data-placeholder class="h-3 w-20 rounded-full overflow-hidden relative bg-gray-200 mb-2"></div>
			<div data-placeholder class="h-8 w-full overflow-hidden relative bg-gray-200"></div>
		</div>
		<div class="col-span-4">
			<div data-placeholder class="h-3 w-20 rounded-full overflow-hidden relative bg-gray-200 mb-2"></div>
			<div data-placeholder class="h-8 w-full overflow-hidden relative bg-gray-200"></div>
		</div>
		<div class="col-span-4">
			<div data-placeholder class="h-3 w-20 rounded-full overflow-hidden relative bg-gray-200 mb-2"></div>
			<div data-placeholder class="h-8 w-full overflow-hidden relative bg-gray-200"></div>
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