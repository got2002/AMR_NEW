<template>
	<div class="h-full w-full p-4 space-y-4">
		<ChartLine ref="yearly" :data="ChartData" :option="ChartOptions" :height="500"></ChartLine>
	
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
					borderColor: "#00b0d8",
					borderWidth: 1,
					callbacks: {
						label: function (tooltipItem, data) {
							// console.log(tooltipItem,data);
							// var label = data.datasets[tooltipItem.datasetIndex].label || "";

							// if (label) {
							// 	label += ": ";
							// }
							// label += tooltipItem.yLabel.toLocaleString()
							return tooltipItem.yLabel.toLocaleString();
						},
					},
					// display:false
				},
				legend: {
					display: false,
				},
				// plugins: {
				// 	datalabels: {
				// 		color: "#fff",
				// 		display: true,
				// 		align: "center",
				// 		formatter: function (value) {
				// 			if (value > 0) {
				// 				return `${value}`;
				// 			} else {
				// 				return "";
				// 			}
				// 		},

				// 		font: {
				// 			size: 10,
				// 			weight: "bold",
				// 			family: '"Prompt", sans-serif',
				// 		},
				// 	},
				// },
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
								padding: 10,
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
						label: this.$t('dashboard.chart.data_label'),
						borderColor: "#00b0d8",
						// backgroundColor: this.getBackgroundGradient,
						fill: false,
						lineTension:0,

						data: [],
					},
				],
			},
		};
	},
	mounted() {
		// this.createXlabels();
		// const elem = document.getElementById("verified-carbon-credit");

		// setTimeout(() => {
		// 	console.log(elem.offsetHeight);
		// 	this.$refs.yearly._data._chart.height = elem.offsetHeight
		// 	this.$refs.yearly._data._chart.update();
		// }, 500);
		this.getVerificatedCreditStat();
	},
	methods: {
		createXlabels() {
			let startDate = this.$moment("2011");
			const endDate = this.$moment();
			let labels = [];
			while (startDate <= endDate) {
				labels.push(startDate.format("YYYY"));
				startDate = startDate.add(1, "years");
			}

			this.ChartData.labels = labels;
			this.$refs.yearly._data._chart.update();
		},
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
				gradient.addColorStop(0, "#4DA366");
				gradient.addColorStop(1, "#00b0d8");
				// gradient.addColorStop(1, "#a7c4e1");
			}

			return gradient;
		},
		async getVerificatedCreditStat() {
			const app = this;
			return await app.$axios
				.$get(`/api/v1/stats/statistics/credits-classified-years`)
				.then((resp) => {
					app.ChartData.labels = resp.labels;
					app.ChartData.datasets[0].data = resp.datasets;
					// console.log(app.$refs.verifiedCredit._data._chart);
					// app.$refs.verifiedCredit._data._chart.config.type = 'horizontalBar'
					app.$refs.yearly._data._chart.update();
				})
				.catch((err) => err);
		},
	},
};
</script>

<style>
</style>