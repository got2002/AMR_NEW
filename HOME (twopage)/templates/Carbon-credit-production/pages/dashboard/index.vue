<template>
	<div class="w-full h-full space-y-6">
		<div class="w-full">
			<span class="font-bold text-2xl text-theme-black-300">{{ $t("dashboard.page_title") }}</span>
		</div>
		<div class="grid lg:grid-cols-3 grid-cols-1 gap-6">
			<DashboardCarbonCreditAmount :title="$t('dashboard.statCO2VolumeTitle.allProject')" :value="stat.total"></DashboardCarbonCreditAmount>
			<DashboardCarbonCreditAmount :title="$t('dashboard.statCO2VolumeTitle.carbonYearly', { year: yearly })" :value="stat.budgetYearCredits"></DashboardCarbonCreditAmount>
			<DashboardCarbonCreditAmount :title="$t('dashboard.statCO2VolumeTitle.total_estimated')" :value="stat.totalEstimatedGreenhouseReduction"></DashboardCarbonCreditAmount>
		</div>
		<div class="grid grid-cols-2  gap-6">
			<div class="2xl:col-span-1 col-span-2  bg-white shadow-sm rounded p-4">
				<span class="font-semibold text-theme-black-300">{{ $t("dashboard.chart.title.categoryProject") }} (tCO<sub>2</sub>eq)</span>
				<DashboardCarbonCategoryBarChart></DashboardCarbonCategoryBarChart>
			</div>
			<div class="2xl:col-span-1 col-span-2  bg-white shadow-sm rounded p-4">
				<span class="font-semibold text-theme-black-300">{{ $t("dashboard.chart.title.yearly") }} (tCO<sub>2</sub>eq)</span>

				<DashboardCarbonLineChart></DashboardCarbonLineChart>
			</div>
		</div>

	
		<loadingCarbon v-if="loading"></loadingCarbon>
	</div>
</template>

<script>
export default {
	layout: "DashboardLayout",
	name: "DashboardIndex",
	middleware: ["auth"],
	data() {
		return {
			yearly: this.$dayjs().format("YYYY"),
			stat: {
				total: 0,
				budgetYearCredits: 0,
				totalEstimatedGreenhouseReduction: 0,
			},
			loading: true,
		};
	},
	watch : {
		'$i18n.locale' : function() {
			this.setDefaultYearly();
		}
	},
	mounted() {
		const app = this;
		app.loading = true;
		this.setDefaultYearly();
		this.$axios
			.$get(`/api/v1/stats/dashboard/credits`)
			.then((resp) => {
				app.stat = resp;
				app.loading = false;
			})
			.catch((err) => {
				console.log(err);
				app.loading = false;
			});
	},
	methods : {
		setDefaultYearly() {
			this.yearly = this.$i18n.locale === "en" ? this.$dayjs().format("YYYY") : this.$dayjs().locale('th').format("BBBB")
		}
	}
};
</script>

<style>
</style>