<template>
	<div class="grid grid-cols-12 gap-4">
		<div class="col-span-2 rounded border border-gray-500">
			<img :src="imgUrl(data?.project_picture)" class="w-full object-center" />
		</div>
		<div class="col-span-8">
			<p class="font-semibold break-words text-sm truncate" :title="projectName(data.project_name)">{{ projectName(data.project_name) }}</p>
			<div class="flex items-center gap-2">
				<div class="font-light text-xs w-28 text-gray-600">{{$t('cart.vintage_card.project_code')}}:</div>
				<div class="font-medium text-xs text-tgo-teal-500">{{ data.project_code }}</div>
			</div>
			<div class="flex items-center gap-2">
				<div class="font-light text-xs w-28 text-gray-600">{{$t('cart.vintage_card.vintage_year')}}:</div>
				<div class="font-medium text-xs">{{ data.vintageYear }}</div>
			</div>
			<div class="flex items-center gap-2">
				<div class="font-light text-xs w-28 text-gray-600">{{$t('cart.vintage_card.block_number')}}:</div>
				<div class="font-medium text-xs">{{ data.blockStart }} - {{ data.blockEnd }}</div>
			</div>

			<!-- <div class="font-medium text-xs text-red-500">{{ "remove" }}</div> -->
		</div>
		<div class="col-span-2 space-y-2">
			<div class="px-2 py-1 border border-gray-300 rounded text-gray-600 text-center text-sm">{{ data.quantity }}</div>
			<p class="text-center font-semibold text-sm text-tgo-teal-700">{{ sum()?.toLocaleString() }} ฿</p>
		</div>
	</div>
</template>

<script>
export default {
	props: ["data"],
	methods: {
		imgUrl(url) {
			if (url?.length > 0) {
				return process.env.baseUrl + url[0].src;
			} else return "https://images.unsplash.com/photo-1516937941344-00b4e0337589?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80";
		},
		projectOwnertext(data) {
			if (this.$i18n.locale === "th") return data.project_owner;
			else return data.project_owner_en;
		},
		projectName(name) {
			if (this.$i18n.locale === "th") return name?.th;
			else return name?.en;
		},
		sum() {
			return this.data.price * this.data.quantity;
		},
	},
};
</script>

<style>
</style>