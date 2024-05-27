<template>
	<div class="w-full">
		<div class="grid grid-cols-1 gap-2">
			<div class="col-span-1 flex items-center justify-between">
				<div class="flex items-center gap-2">
					<div data-placeholder class="h-8 w-14 rounded overflow-hidden relative bg-gray-50"></div>
					<div data-placeholder class="h-8 w-40 rounded overflow-hidden relative bg-gray-50"></div>
					<div data-placeholder class="h-8 w-40 rounded overflow-hidden relative bg-gray-50"></div>
				</div>
				<div data-placeholder class="h-8 w-40 rounded overflow-hidden relative bg-gray-50"></div>
			</div>
			<div class="col-span-1">
				<div data-placeholder class="h-40 w-full rounded overflow-hidden relative bg-gray-50"></div>
			</div>
			<div class="col-span-1 h-10"></div>

			<div class="col-span-1 flex items-center justify-between">
				<div class="flex items-center gap-2">
					<div data-placeholder class="h-8 w-14 rounded overflow-hidden relative bg-gray-50"></div>
					<div data-placeholder class="h-8 w-40 rounded overflow-hidden relative bg-gray-50"></div>
					<div data-placeholder class="h-8 w-40 rounded overflow-hidden relative bg-gray-50"></div>
				</div>
				<div data-placeholder class="h-8 w-40 rounded overflow-hidden relative bg-gray-50"></div>
			</div>
			<div class="col-span-1">
				<div data-placeholder class="h-40 w-full rounded overflow-hidden relative bg-gray-50"></div>
			</div>
		</div>
	</div>
</template>

<script>
export default {};
</script>

<style scoped>
[data-placeholder]::after {
	content: " ";
	box-shadow: 0 0 30px 50px rgb(255, 255, 255);
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