<template>
	<div class="h-full w-full p-4 space-y-4">
		<ChartBar ref="homeStatistic" :data="ChartData" :option="ChartOptions" :height="500"></ChartBar>
		<div class="flex justify-center ">
			<div class="flex flex-wrap gap-6">
				<div class=" flex items-center gap-2">
					<div class="w-5 h-5 bg-tgo-yellow-500 shadow-sm"></div>
					<span class="text-xs">{{ $t("statistics.chart.title.yearly_verified_carbon_credit") }} (tCO<sub>2</sub>eq)</span>
				</div>
				<div class=" flex items-center gap-2">
					<div class="w-5 h-5 bg-tgo-teal-500 shadow-sm"></div>
					<span class="text-xs">{{ $t("statistics.chart.title.estimated_greenhouse_gases_reduction") }} (tCO<sub>2</sub>eq)</span>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	data() {
		return {
			ChartOptions: {
				maintainAspectRatio: false,
				responsive: true,
				tooltips: {
					titleFontFamily: '"Prompt", sans-serif',
					titleFontColor: "#000",
					bodyFontFamily: '"Prompt", sans-serif',
					bodyFontColor: "#000",
					backgroundColor: "#fff",
					borderColor: "#64A6E8",
					borderWidth: 1,
					callbacks: {
						label: function (tooltipItem, data) {
							
							var label = data.datasets[tooltipItem.datasetIndex].label || "";

							if (label) {
								label += ": ";
							}
							label += tooltipItem.yLabel.toLocaleString()
							return label;
						},
					},
				},
				legend: {
					display: false,
				},

				scales: {
					yAxes: [
						{
							ticks: {
								callback: function (value, index, values) {
									if (value <= 0) return "";
									if (value < 1e3) return value;
									if (value >= 1e3 && value < 1e6) return +(value / 1e3).toFixed(1) + "K";
									if (value >= 1e6 && value < 1e9) return +(value / 1e6).toFixed(1) + "M";
									if (value >= 1e9 && value < 1e12) return +(value / 1e9).toFixed(1) + "B";
									if (value >= 1e12) return +(value / 1e12).toFixed(1) + "T";
								},

								fontColor: "#252525",
								fontFamily: '"Prompt", sans-serif',
							},
							gridLines: {
								display: true,
								borderDash: [2, 2],
								color: "#525152",
							},
						},
					],
					xAxes: [
						{
							ticks: {
								fontColor: "#252525",
								fontFamily: '"Prompt", sans-serif',
								// padding: 5,
							},
							gridLines: {
								display: false,
								// tickMarkLength:30
							},
						},
					],
				},
			},

			ChartData: {
				labels: [],
				datasets: [
					{
						label: this.$t("statistics.chart.title.yearly_verified_carbon_credit"),
						// borderColor: this.getGradient,
						backgroundColor: "#c9da2a",
						fill: true,
						// lineTension:0,
						data: [],
					},
					{
						label: this.$t("statistics.chart.title.estimated_greenhouse_gases_reduction"),
						// borderColor: this.getGradient,
						backgroundColor: "#00b0d8",
						fill: true,
						// lineTension:0,
						data: [],
					},
				],
			},
		};
	},
	async mounted() {
		
		await this.getVerificatedCreditStat();
		await this.getStatisticClassifiedReductionGas();
	},
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
				gradient.addColorStop(0, "#c9da2a");
				gradient.addColorStop(1, "#00b0d8");
				// gradient.addColorStop(1, "#a7c4e1");
			}

			return gradient;
		},
		getBackgroundGradient(context) {
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
				gradient.addColorStop(0, "#c9da2a");
				gradient.addColorStop(1, "#00b0d8");
				// gradient.addColorStop(1, "#a7c4e1");
			}

			return gradient;
		},
		async getVerificatedCreditStat() {
			const app = this;
			return await app.$axios
				.$get(`/api/v1/home/statistics/credits-classified-years`)
				.then((resp) => {
					app.ChartData.labels = resp.labels;
					app.ChartData.datasets[0].data = resp.datasets;
					// console.log(app.$refs.verifiedCredit._data._chart);
					// app.$refs.verifiedCredit._data._chart.config.type = 'horizontalBar'
					app.$refs.homeStatistic._data._chart.update();
				})
				.catch((err) => err);
		},
		async getStatisticClassifiedReductionGas() {
			const app = this;
			return await app.$axios
				.$get(`/api/v1/home/statistics/approx-carbon-reduction-years`)
				.then((resp) => {
					// app.ChartData.labels = resp.labels;
					app.ChartData.datasets[1].data = resp.datasets;
					// console.log(app.$refs.verifiedCredit._data._chart);
					// app.$refs.verifiedCredit._data._chart.config.type = 'horizontalBar'
					app.$refs.homeStatistic._data._chart.update();
				})
				.catch((err) => err);
		},
	},
};
</script>

<style>
</style>