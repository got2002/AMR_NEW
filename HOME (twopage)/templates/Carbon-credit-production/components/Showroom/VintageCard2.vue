<template>
	<div class="col-span-4 bg-white rounded shadow-md">
		<div class="w-full h-40 bg-tgo-teal-500 rounded-t p-4 flex items-center justify-center">
			<div class="text-white relative">
				<div class="absolute z-10 top-0 -left-2.5">฿</div>
				<span class="text-6xl">500</span>
				<span class="text-sm">/Tonne</span>
			</div>
		</div>
		<div class="p-8 space-y-8">
			<div class="flex justify-between items-center">
				<div>
					<label class="text-gray-500 text-sm">Availability(tonnes)</label>
					<p class="text-lg font-medium">200,000</p>
				</div>
				<div>
					<label class="text-gray-500 text-sm">Vintage Year</label>
					<p class="text-lg font-medium">2020</p>
				</div>
			</div>
			<div>
				<UITextInput type="number" class="text-center" />
			</div>
			<div>
				<p class="text-center text-gray-400 text-sm">total</p>
				<p class="text-center text-2xl text-tgo-teal-700">1,000</p>
			</div>
			<div class="flex items-center justify-center">
				<button class="px-4 py-2 rounded bg-tgo-teal-500 hover:bg-tgo-teal-600 shadow-md text-white">ADD TO CART</button>
			</div>
		</div>
	</div>
</template>

<script>
export default {};
</script>

<style>
</style>