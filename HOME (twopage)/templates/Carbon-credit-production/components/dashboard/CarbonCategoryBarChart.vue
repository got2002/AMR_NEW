<template>
	<div class="h-full w-full p-4" id="verified-carbon-credit">
		<div class="w-full">
			<ChartBar ref="classifyByType" :data="ChartData" :option="ChartOptions" type="horizontalBar" :height="500"></ChartBar>
		</div>
	</div>
</template>

<script>
import dropdowns from "../../mixins/dropdowns";

export default {
	mixins: [dropdowns],
	watch: {
		"$i18n.locale": function (locale) {
			this.ChartData.datasets[0].label = this.$t("dashboard.chart.data_label");
			this.$refs.classifyByType._data._chart.update();
		},
	},
	data() {
		return {
			chartLabel: [],
			ChartData: {
				labels: [],
				datasets: [
					{
						label: this.$t("dashboard.chart.data_label"),
						backgroundColor: "#00b0d8",
						
						data: [],
						// borderRadius:30
					},
				],
			},
			ChartOptions: {
				responsive: true,
				maintainAspectRatio: false,
				// indexAxis: "y",

				// cutoutPercentage:80,

				// layout: {
				// 	padding: 30,
				// },

				scales: {
					xAxes: [
						{
							// stacked: true,

							ticks: {
								beginAtZero: true,
								fontFamily: '"Prompt", sans-serif',

								autoSkip: false,
								callback: function (value, index, values) {

									return value.abbr;
								},
							},
							gridLines: { display: false },
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
							},
						},
					],
				},
				tooltips: {
					titleFontFamily: '"Prompt", sans-serif',
					titleFontColor: "#000",
					bodyFontFamily: '"Prompt", sans-serif',
					bodyFontColor: "#000",
					backgroundColor: "#fff",
					borderColor: "#4DA366",
					borderWidth: 1,
					callbacks: {
						label: function (tooltipItem, data) {
							// console.log(tooltipItem,data);
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

				plugins: {
					datalabels: {
						color: "#fff",
						display: false,
						align: "center",
						formatter: function (value) {
							if (value <= 0) return "";
							if (value < 1e3) return value;
							if (value >= 1e3 && value < 1e6) return +(value / 1e3).toFixed(1) + "K";
							if (value >= 1e6 && value < 1e9) return +(value / 1e6).toFixed(1) + "M";
							if (value >= 1e9 && value < 1e12) return +(value / 1e9).toFixed(1) + "B";
							if (value >= 1e12) return +(value / 1e12).toFixed(1) + "T";
						},

						font: {
							size: 10,
							weight: "bold",
							family: '"Prompt", sans-serif',
						},
					},
				},
			},
		};
	},
	async mounted() {
		await this.getClassifyByType();
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
		async getClassifyByType() {
			const app = this;
			return await app.$axios
				.$get(`/api/v1/stats/dashboard/project-type`)
				.then((resp) => {
					app.ChartData.labels = resp.labels

					app.ChartData.datasets[0].data = resp.datasets;
					// app.$refs.verifiedCredit._data._chart.config.type = 'horizontalBar'
					// console.log(app.$refs.verifiedCredit._data._chart);
					// app.$refs.classifyByType._data._chart.data.labels = app._.map(resp.labels,item=>item.abbr)

					app.$refs.classifyByType._data._chart.update();
				})
				.catch((err) => err);
		},
	},
};
</script>

<style></style>
