<template>
	<div class="w-full h-full space-y-4">
		<div class="w-full h-full space-y-6">
			<div class="w-full">
				<span class="font-bold text-2xl text-theme-black-300">{{ $t("statistics.page_title") }}</span>
			</div>
			<div class="grid lg:grid-cols-3 grid-cols-1 gap-6">
				<StatCarbonCreditAmount :title="$t('statistics.statCO2VolumeTitle.approved_carbon_credits')" :value="stat.verifiedCredits"></StatCarbonCreditAmount>
				<StatCarbonCreditAmount :title="$t('statistics.statCO2VolumeTitle.compensated_carbon_credits')" :value="stat.tradedCredits"></StatCarbonCreditAmount>
				<StatCarbonCreditAmount :title="$t('statistics.statCO2VolumeTitle.carbon_credits_available')" :value="stat.remainCredits"></StatCarbonCreditAmount>
			</div>
			<div class="grid grid-cols-2 gap-6">
				<div class="col-span-2 bg-theme-white shadow-sm rounded p-4">
					<StatTransferChart></StatTransferChart>
				</div>
				<div class="col-span-2 2xl:col-span-1 xl:col-span-1 bg-theme-white shadow-sm rounded p-4">
					<span class="font-semibold text-theme-black-300 pt-4">{{ $t("statistics.chart.title.verify_carbon_credit") }} (tCO<sub>2</sub>eq)</span>
					<StatCarbonCategoryBarChart></StatCarbonCategoryBarChart>
				</div>
				<div class="col-span-2 2xl:col-span-1 xl:col-span-1 bg-theme-white shadow-sm rounded p-4">
					<span class="font-semibold text-theme-black-300 pt-4">{{ $t("statistics.chart.title.yearly_verified_carbon_credit") }} (tCO<sub>2</sub>eq)</span>

					<StatCarbonYearlyLineChart></StatCarbonYearlyLineChart>
				</div>
				<div class="col-span-2 2xl:col-span-1 xl:col-span-1 bg-theme-white shadow-sm rounded p-4">
					<span class="font-semibold text-theme-black-300 pt-4">{{ $t("statistics.chart.title.registered_project") }}</span>

					<StatCarbonProjectYearlyLineChart></StatCarbonProjectYearlyLineChart>
				</div>
				<div class="col-span-2 2xl:col-span-1 xl:col-span-1 bg-theme-white shadow-sm rounded p-4">
					<span class="font-semibold text-theme-black-300 pt-4">{{ $t("statistics.chart.title.estimated_greenhouse_gases_reduction") }} (tCO<sub>2</sub>eq)</span>

					<StatCarbonValidateYearlyLineChart></StatCarbonValidateYearlyLineChart>
				</div>
			</div>
			<div class="grid grid-cols-3 gap-6">
				<div class="col-span-3 shadow-sm rounded">
					<StatMapDashboard></StatMapDashboard>
				</div>
				<!-- <div class="col-span-1">
					<span class="font-semibold mb-4">{{$t('statistics.chart.title.greenhouse_gases_by_region')}}</span>
					<StatCarbonThailandZone></StatCarbonThailandZone>
				</div> -->
			</div>
			<loadingCarbon v-if="loading"></loadingCarbon>
		</div>
	</div>
</template>

<script>
	export default {
		layout: "DashboardLayout",
		name: "StatisticsIndex",
		middleware: ["auth"],
		data() {
			return {
				stat: {
					verifiedCredits: 10,
					tradedCredits: 10,
					remainCredits: 0,
				},
				loading: true,
			};
		},

		async mounted() {
			await this.getCreditStat();
			this.loading = false;
		},
		methods: {
			getCreditStat() {
				const app = this;
				this.$axios.$get(`/api/v1/stats/statistics/credits`).then((resp) => {
					app.stat = resp;
				});
			},
		},
	};
</script>

<style></style>
