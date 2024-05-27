<template>
	<div class="mx-auto container 2xl:w-6/12 lg:w-8/12 w-11/12">
		<div class="flex justify-between items-center pb-2">
			<div data-placeholder class="h-5 w-20 rounded-full overflow-hidden relative bg-gray-200"></div>
		</div>
		<div class="grid grid-cols-2 gap-4 bg-white p-4">
			<div class="col-span-2 flex items-center gap-2">
				<div data-placeholder class="h-5 w-20 rounded-full overflow-hidden relative bg-gray-200"></div>
				
			</div>

			<div class="col-span-2 border"></div>
			<div class="col-span-1">
				<div data-placeholder class="mb-2 h-4 w-20 rounded-full overflow-hidden relative bg-gray-200"></div>
				<div data-placeholder class="h-10 w-full rounded overflow-hidden relative bg-gray-200"></div>
			</div>
			<div class="col-span-1">
				<div data-placeholder class="mb-2 h-4 w-20 rounded-full overflow-hidden relative bg-gray-200"></div>
				<div data-placeholder class="h-10 w-full rounded overflow-hidden relative bg-gray-200"></div>
			</div>
			<div class="col-span-1">
				<div data-placeholder class="mb-2 h-4 w-20 rounded-full overflow-hidden relative bg-gray-200"></div>
				<div data-placeholder class="h-10 w-full rounded overflow-hidden relative bg-gray-200"></div>
			</div>
			<div class="col-span-1">
				<div data-placeholder class="mb-2 h-4 w-20 rounded-full overflow-hidden relative bg-gray-200"></div>
				<div data-placeholder class="h-10 w-full rounded overflow-hidden relative bg-gray-200"></div>
			</div>
			<div class="col-span-2">
				<div data-placeholder class="mb-2 h-4 w-20 rounded-full overflow-hidden relative bg-gray-200"></div>
				<div data-placeholder class="h-10 w-full rounded overflow-hidden relative bg-gray-200"></div>
			</div>
			<div class="col-span-2 mt-4"></div>
			<div class="col-span-2 flex items-center gap-2">
				<div data-placeholder class="h-5 w-20 rounded-full overflow-hidden relative bg-gray-200"></div>
				<div data-placeholder class="h-5 w-40 rounded-full overflow-hidden relative bg-gray-200"></div>
			</div>

			<div class="col-span-2 border"></div>
			<div class="col-span-1">
				<div data-placeholder class="mb-2 h-4 w-20 rounded-full overflow-hidden relative bg-gray-200"></div>
				<div data-placeholder class="h-10 w-full rounded overflow-hidden relative bg-gray-200"></div>
			</div>
			<div class="col-span-1">
				<div data-placeholder class="mb-2 h-4 w-20 rounded-full overflow-hidden relative bg-gray-200"></div>
				<div data-placeholder class="h-10 w-full rounded overflow-hidden relative bg-gray-200"></div>
			</div>

			<div class="col-span-2 mt-4"></div>
			<div class="col-span-2 flex items-center gap-2">
				<div data-placeholder class="h-5 w-20 rounded-full overflow-hidden relative bg-gray-200"></div>
				<div data-placeholder class="h-5 w-40 rounded-full overflow-hidden relative bg-gray-200"></div>
			</div>

			<div class="col-span-2 border"></div>
			<div class="col-span-2 flex gap-4">
				<div data-placeholder class="h-20 w-full rounded overflow-hidden relative bg-gray-200"></div>
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