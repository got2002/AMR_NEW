<template>
	<section>
		<div class="grid grid-cols-1 gap-2 text-sm">
			<div class="col-span-1 flex flex-col" v-for="(address, i) in form.address" :key="i">
				<div class="flex items-center">
					<!-- <label class="w-32 px-3 py-2 text-center border-2 bg-gray-200">{{ $t("project.create_page.address.subtitle") }} ({{ i + 1 }})</label> -->
					<span type="text" class="w-full px-3 py-2 text-center border-2">{{form.address[i]}}</span>
				</div>
			</div>
		</div>
	</section>
</template>

<script>

export default {
	props: ["form","isSubmitted"],
};
</script>

<style>
</style>