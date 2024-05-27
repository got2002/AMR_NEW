<template>
	<div>
		<label :for="id" class="cursor-pointer">
			<div class="w-full h-11 bg-gray-50 border border-gray-400 rounded relative flex items-center px-4 truncate">
				<p class="text-sm">{{ filename }}</p>
				<div class="w-40 h-full flex items-center justify-center bg-gray-300 border-l border-gray-400 text-sm absolute z-10 right-0 top-0">{{ $t("button.choosefile") }}</div>
			</div>
		</label>
		<input type="file" :id="id" accept="image/*,.pdf" hidden @input="$emit('upload',$event)" />
	</div>
</template>

<script>
export default {
	props: {
		id: String,
		filename:String
	},
	data() {
		return {
			file: {},
		};
	},
	
};
</script>

<style>
</style>