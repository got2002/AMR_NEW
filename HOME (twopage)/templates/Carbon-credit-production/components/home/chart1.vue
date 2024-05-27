<template>
	<div class="h-full w-full p-4 space-y-4" id="verified-carbon-credit">
		<!-- <div class="grid grid-cols-1 gap-2">
			<div class="col-span-1 flex gap-2" v-for="(label,i) in ChartData.labels" :key="i">
				<p class="w-4 h-4 " :style="`background-color:${ChartData.datasets[0].backgroundColor[i]}`"></p>
				<span class="text-xs">{{ label }}</span>
			</div>
		</div> -->
		<div class="w-full">
			<!-- <ChartBar ref="homeChart1" :data="ChartData" :option="ChartOptions"  :height="300"></ChartBar> -->

			<!-- <ChartBarHorizontal ref="homeChart1" :data="ChartData" :option="ChartOptions" :updateChart="updateChart" :height="300" /> -->
			<ChartBarWithLabelTop ref="homeChart1" :data="ChartData" :option="ChartOptions" :topLabelData="projectClassifiedByType" type="horizontalBar" :height="500"></ChartBarWithLabelTop>
			<div class="flex justify-center my-4">
				<div class="flex flex-wrap gap-6">
					<div class="flex items-center justify-center gap-2">
						<div class="w-5 h-5 bg-tgo-yellow-500 shadow-sm"></div>
						<span class="text-xs">{{ $t("statistics.chart.labels.carbon_credits_classified_by_project_type") }} (tCO<sub>2</sub>eq)</span>
					</div>
					<div class="flex items-center justify-center gap-2">
						<div class="w-5 h-5 rounded-full bg-tgo-teal-500 shadow-sm"></div>
						<span class="text-xs">{{ $t("statistics.chart.labels.project_classified_by_project_type") }}</span>
					</div>
				</div>
			</div>
		</div>
		<!-- <div class="flex flex-wrap gap-2 bg-gray-200 p-2 mt-4" v-if="chartLabel.length > 0">
			<div class="w-auto px-2 py-1 flex gap-2" v-for="(label, i) in chartLabel" :key="i">
				<p class="text-xs font-bold">({{ i + 1 }})</p>
				<span class="text-xs">{{ ccmgm(label) }}</span>
			</div>
		</div> -->
	</div>
</template>

<script>
export default {
	data() {
		return {
			updateChart: true,
			chartLabel: [],
			ChartData: {
				labels: [],
				datasets: [
					{
						label: this.$t("statistics.chart.labels.carbon_credits_classified_by_project_type"),
						// backgroundColor: this.getGradient,
						backgroundColor: "#c9da2a",
						// yAxisID: "carbon-credit-classified-by-type",
						data: [],
					},
				],
			},
			projectClassifiedByType: {
				labels: [],
				datasets: [],
			},
			ChartOptions: {
				responsive: true,
				maintainAspectRatio: false,

				scales: {
					xAxes: [
						{
							// stacked: true,
							// id: "carbon-credit-classified-by-type",
							// type: "linear",
							// position: "left",
							// scaleLabel: {
							// 	display: true,
							// 	fontFamily: '"Prompt", sans-serif',
							// 	fontSize: 10,
							// 	labelString: this.$t("statistics.chart.labels.carbon_credits_classified_by_project_type") + " (" + this.$t("unit.ton") + ")",
							// },
							ticks: {
								beginAtZero: true,
								fontFamily: '"Prompt", sans-serif',

								autoSkip: false,
								callback: function (value, index, values) {
									return value.abbr;
								},
							},
							gridLines: { display: true },
						},
					],
					yAxes: [
						{
							// stacked: true,
							ticks: {
								fontFamily: '"Prompt", sans-serif',
								callback: function (value, index, values) {
									if (value <= 0) return "";
									if (value < 1e3) return value;
									if (value >= 1e3 && value < 1e6) return +(value / 1e3).toFixed(1) + "K";
									if (value >= 1e6 && value < 1e9) return +(value / 1e6).toFixed(1) + "M";
									if (value >= 1e9 && value < 1e12) return +(value / 1e9).toFixed(1) + "B";
									if (value >= 1e12) return +(value / 1e12).toFixed(1) + "T";
								},
								// max: 1e3,
							},
							gridLines: { display: true },
						},
					],
				},
				tooltips: {
					titleFontFamily: '"Prompt", sans-serif',
					titleFontColor: "#000",
					bodyFontFamily: '"Prompt", sans-serif',
					bodyFontColor: "#000",
					backgroundColor: "#fff",
					borderColor: "#c9da2a",
					borderWidth: 1,
					callbacks: {
						label: function (tooltipItem, data) {
							var label = data.datasets[tooltipItem.datasetIndex].label || "";

							if (label) {
								label += ": ";
							}
							label += tooltipItem.yLabel.toLocaleString();
							return label;
						},
						title:(tooltipItem)=>{
						
							return tooltipItem[0].xLabel[this.$i18n.locale]
						}
					},
				},

				legend: {
					display: false,
				},
				title: {
					display: false,
				},
			},
		};
	},

	async mounted() {
		await this.getVerificatedCreditStat();
		await this.getProjectClassifiedByType();

		// await this.addValueOnTopBarChart();
	},
	// watch:{
	// 	'$i18n.locale':async function(val){
	// 		console.log(this._.map(this.ChartData.labels,item=>this.ccmgm(item)));
	// 		console.log(this.ChartData.labels);

	// 		this.$refs.homeChart1._data._chart.data.labels = await this._.map(this.ChartData.labels,item=>this.ccmgm(item))
	// 		await this.$refs.homeChart1._data._chart.update();
	// 	}
	// },

	methods: {
		
		getGradient(context) {
			const chart = context.chart;
			const { ctx, chartArea } = chart;

			if (!chartArea) {
				// This case happens on initial chart load
				return;
			}
			let width, height, gradient;
			const chartWidth = chartArea.right - chartArea.left;
			const chartHeight = chartArea.bottom - chartArea.top;
			if (!gradient || width !== chartWidth || height !== chartHeight) {
				// Create the gradient because this is either the first render
				// or the size of the chart has changed
				width = chartWidth;
				height = chartHeight;
				gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
				gradient.addColorStop(0, "#4DA366");
				gradient.addColorStop(1, "#2061a2");
				// gradient.addColorStop(1, "#a7c4e1");
			}

			return gradient;
		},
		async getVerificatedCreditStat() {
			const app = this;
			return await app.$axios
				.$get(`/api/v1/home/statistics/carbon-credit-classified-by-type`)
				.then((resp) => {
					app.ChartData.labels = app._.clone(resp.labels);
					app.chartLabel = app._.clone(resp.labels);

					app.ChartData.datasets[0].data = resp.datasets;

					// app.$refs.verifiedCredit._data._chart.config.type = 'horizontalBar'
					const max = app._.max(resp.datasets);
					app.$refs.homeChart1._data._chart.options.scales.yAxes[0].ticks.max = max + 1000000;
					// app.$refs.homeChart1._data._chart.data.labels = app._.map(resp.labels, (item) => app.ccmgm(item));

					app.$refs.homeChart1._data._chart.update();
					// app.updateChart = !app.updateChart
				})
				.catch((err) => err);
		},
		async getProjectClassifiedByType() {
			const app = this;
			return await app.$axios
				.$get(`/api/v1/home/statistics/project-classified-by-type`)
				.then((resp) => {
					app.projectClassifiedByType.labels = resp.labels;
					app.projectClassifiedByType.datasets = resp.datasets;

					// app.ChartData.labels = resp.labels;
					// app.ChartData.datasets[0].data = resp.datasets;
					// // app.$refs.verifiedCredit._data._chart.config.type = 'horizontalBar'
					// const max = app._.max(resp.datasets);
					// app.$refs.homeChart1._data._chart.options.scales.yAxes[0].ticks.max = max + 100;
					// // console.log(app.$refs.homeChart1._data._chart.options.scales.yAxes[0].ticks.max);

					app.$refs.homeChart1._data._chart.update();
					// app.updateChart = !app.updateChart
				})
				.catch((err) => err);
		},
	},
};
</script>

<style></style>
