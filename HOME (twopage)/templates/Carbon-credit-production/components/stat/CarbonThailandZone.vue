<template>
	<div class="grid grid-cols-1 gap-3">
		<div v-for="item in items" :key="item.th" class="col-span-1 flex items-center justify-between bg-gradient-to-r from-tgo-yellow-500 to-tgo-teal-500 px-4 py-1 text-theme-black-50 rounded-full shadow-sm">
			<span>{{ item[$i18n.locale] }}</span>
			<span class="font-semibold">{{ item.co2.toLocaleString() }}</span>
		</div>
	</div>
</template>

<script>
export default {
	props: {
		title: {
			type: String,
			default: () => "TITLE",
		},
		value: {
			type: Number,
			require: true,
		},
	},
    data(){
        return{
            items:[]
        }
    },
    async mounted(){
		await this.getRegionStat()
		
	},
	methods:{
		getRegionStat(){
			const app = this;
			this.$axios.$get(`/api/v1/stats/statistics/project-location-region`).then((resp) => {
				app.items = resp;
			});
		},
		
	}
};
</script>

<style>
</style>