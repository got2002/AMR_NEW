<template>
	<div @click="linkPage" class="xl:col-span-3 lg:col-span-4 col-span-6 bg-white rounded shadow-sm border-2 hover:border-tgo-teal-500 hover:border-2 transition ease-in cursor-pointer transform duration-100 hover:-translate-y-2">
		<div class="relative">
			<!-- <div class="absolute z-10 flex items-center gap-2 top-2 left-2"></div> -->
			<div class="absolute z-10 flex items-center gap-2 bottom-2 left-2">
				<p @mouseover="blurBG = true" @mouseleave="blurBG = false" class="bg-tgo-yellow-500 shadow-md rounded px-2 py-1 text-xs" :title="vintageYearUnique.join(', ')">{{ vintageYearValue(vintageYearUnique) }}</p>
				<p @mouseover="blurBG = true" @mouseleave="blurBG = false" class="bg-tgo-teal-500 text-white shadow-md rounded px-2 py-1 text-xs" :title="data.project_type[$i18n.locale]">{{ data.project_type.abbr }}</p>
			</div>
			<div class="absolute z-10 flex items-center gap-2 top-2 right-2">
				<div v-if="data.environment" class="w-6 h-6 rounded-full flex items-center justify-center bg-tgo-teal-500 shadow-md">
					<ShowroomLeafIcon />
				</div>
				<div v-if="data.society" class="w-6 h-6 rounded-full flex items-center justify-center bg-tgo-teal-500 shadow-md">
					<ShowroomUserIcon />
				</div>
				<div v-if="data.economy" class="w-6 h-6 rounded-full flex items-center justify-center bg-tgo-teal-500 shadow-md">
					<ShowroomCloudMoneyIcon />
				</div>
			</div>
			<img class="w-full object-cover rounded-t h-40" :class="{'filter blur-sm transition duration-200 ease-in-out':blurBG}" :src="imgUrl(data.projectPicture)" />
		</div>
		<div class="p-4 space-y-2">
			<p class="text-sm text-gray-500">{{$t('showroom.project_card.project_id')}}: {{ data.projectID }}</p>
			<div class="h-12 flex items-center">
			<p class="text-base font-semibold break-words " :title="projectName(data.projectName)">{{ sliceText(projectName(data.projectName)) }}</p>
			</div>

			<div class="flex items-end justify-between">
				<div>
					<p class="text-sm text-gray-500">{{$t('showroom.project_card.availability')}}:</p>
					<p class="text-lg font-medium">{{ data.availableTonne?.toLocaleString() }}</p>
					<p class="text-sm text-gray-500">{{$t('showroom.project_card.price_range')}}/tCO<sub>2</sub>e:</p>
					<p class="">
						<span class="text-lg font-medium">{{ data.price.min?.toLocaleString() || 0 }}฿ - {{ data.price.max?.toLocaleString() || 0 }}฿</span>
					</p>
				</div>
				
			</div>
		</div>
	</div>
</template>

<script>
export default {
	props: ["data"],
	computed: {
		vintageYearUnique() {
			return this._.chain(this.data.vintageYears)
				.uniq()
				.map((year) => {
					if (this.$i18n.locale === "th") return this.$dayjs(year).locale("th").format("BBBB");
					else return this.$dayjs(year).locale("en").format("YYYY");
				})
				.sort()
				.value();
		},
	},
	data(){
		return{
			blurBG:false
		}
	},
	methods: {
		vintageYearValue(data) {
			if (data.length > 1) {
				if (this.$i18n.locale === "th") return data[0] + " - " + data[data.length - 1];
				else return data[0] + " - " + data[data.length - 1];
			} else {
				if (this.$i18n.locale === "th") return data[0];
				else return data[0];
			}
		},
		sliceText(text) {
			if (text.length > 40) {
				return text.slice(0, 40) + "...";
			} else return text;
		},
		imgUrl(url) {
			if (url !== null) {
				return process.env.baseUrl + url;
			} else return "https://images.unsplash.com/photo-1516937941344-00b4e0337589?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80";
		},
		projectName(name) {
			if (this.$i18n.locale === "th") return name.th;
			else return name.en;
		},
		linkPage() {
			this.$router.push(this.localePath(`/showroom/${this.data._id}/info`));
		},
	},
};
</script>

<style>
</style>