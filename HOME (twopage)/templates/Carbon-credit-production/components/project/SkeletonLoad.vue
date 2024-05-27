<template>
	<div class="w-full flex gap-4">
		<div class="w-1/2 bg-white p-4">
			<div class="grid grid-cols-2 gap-4">
				<div class="col-span-2 space-y-2">
					<div data-placeholder class="h-5 w-full rounded-full overflow-hidden relative bg-gray-200"></div>
					<div data-placeholder class="h-5 w-60 rounded-full overflow-hidden relative bg-gray-200"></div>
				</div>

				<div class="col-span-2 space-y-2">
					<div data-placeholder class="h-5 w-40 rounded overflow-hidden relative bg-gray-200"></div>
					<div data-placeholder class="h-28 w-full rounded overflow-hidden relative bg-gray-200"></div>
				</div>

				<div class="col-span-2 space-y-2">
					<div data-placeholder class="h-5 w-40 rounded overflow-hidden relative bg-gray-200"></div>
					<div data-placeholder class="h-40 w-full rounded overflow-hidden relative bg-gray-200"></div>
				</div>

				<div class="col-span-2 space-y-2">
					<div data-placeholder class="h-5 w-40 rounded overflow-hidden relative bg-gray-200"></div>
					<div data-placeholder class="h-40 w-full rounded overflow-hidden relative bg-gray-200"></div>
				</div>
			</div>
		</div>
		<div class="w-1/2 bg-white p-4">
			<div class="grid grid-cols-2 gap-4">
				<div class="col-span-2 flex justify-between">
					<div data-placeholder class="h-5 w-60 rounded-full overflow-hidden relative bg-gray-200"></div>
					<div data-placeholder class="h-10 w-20 rounded-sm overflow-hidden relative bg-gray-200"></div>
				</div>

				<div class="col-span-2 space-y-2">
					<div data-placeholder class="h-5 w-40 rounded overflow-hidden relative bg-gray-200"></div>
					<div class="flex items-center gap-2">
						<div v-for="i in 4" :key="i" data-placeholder class="h-20 w-20 rounded overflow-hidden relative bg-gray-200"></div>
					</div>
				</div>

				<div class="col-span-2 space-y-2">
					<div data-placeholder class="h-5 w-40 rounded overflow-hidden relative bg-gray-200"></div>
					<div data-placeholder class="h-80 w-full rounded overflow-hidden relative bg-gray-200"></div>
				</div>

				<div class="col-span-2 space-y-2">
					<div data-placeholder class="h-16 w-full rounded overflow-hidden relative bg-gray-200"></div>
				</div>

				<div class="col-span-2 space-y-2">
					<div class="grid grid-cols-2 gap-2">
						<div class="col-span-2" v-for="i in 6" :key="i">
							<div data-placeholder class="h-14 w-full rounded overflow-hidden relative bg-gray-200"></div>
						</div>
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
</style>