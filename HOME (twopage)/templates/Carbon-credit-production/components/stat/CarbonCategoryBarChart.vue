<template>
	<div class="h-full w-full p-4" id="verified-carbon-credit">
		<!-- <div class="grid grid-cols-1 gap-2">
			<div class="col-span-1 flex gap-2" v-for="(label,i) in ChartData.labels" :key="i">
				<p class="w-4 h-4 " :style="`background-color:${ChartData.datasets[0].backgroundColor[i]}`"></p>
				<span class="text-xs">{{ label }}</span>
			</div>
		</div> -->
		<div class="w-full">
			<ChartBar ref="verifiedCredit" :data="ChartData" :option="ChartOptions" type="horizontalBar" :height="500"></ChartBar>
		</div>
		<!-- <div class="flex flex-wrap gap-2 bg-gray-200 p-2 mt-4">
			<div class="w-auto px-2 py-1 flex gap-2" v-for="(label,i) in chartLabel" :key="i">
				<p class="text-xs font-bold">({{i+1}})</p>
				<span class="text-xs">{{ ccmgm(label) }}</span>
			</div>
		</div> -->
	</div>
</template>

<script>
export default {
	data() {
		return {
			chartLabel:[],
			ChartData: {
				labels: [],
				datasets: [
					{
						label: this.$t("dashboard.chart.data_label"),
						backgroundColor: "#00b0d8",
						// backgroundColor: ["#66bcae", "#4db1a1", "#33a693", "#199b86", "#009078", "#00826c", "#007360", "#006554", "#005648"],
						data: [1, 2],
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
									return value.abbr
								},
							},
							gridLines: { display: false },
						},
					],
					yAxes: [
						{
							// stacked: true,
							scaleLabel: {
								display: true,
								fontFamily: '"Prompt", sans-serif',
								fontSize: 10,
								labelString: this.$t("statistics.chart.labels.carbon_credits_classified_by_project_type") + " CCMGM ",
							},
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
					borderColor: "#c9da2a",
					borderWidth: 1,
					callbacks: {
						label: function (tooltipItem, data) {
							// console.log(tooltipItem,data);
							var label = data.datasets[tooltipItem.datasetIndex].label || "";

							if (label) {
								label += ": ";
							}
							label += tooltipItem.yLabel.toLocaleString() + " tCO2eq"
							return label
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
		await this.getVerificatedCreditStat();
	},
	methods: {
		ccmgm(data) {
				if (this.$i18n.locale === "th") {
					return data;
				} else {
					switch (data) {
						case "พลังงานหมุนเวียนหรือพลังงานที่ใช้ทดแทนเชื้อเพลิงฟอสซิล":
							return "Renewable energy or fossil fuel replacement";
						case "การเพิ่มประสิทธิภาพการผลิตไฟฟ้าและการผลิตความร้อน":
							return "Improvement of the efficiency of electricity and heat generation";
						case "การใช้ระบบขนส่งสาธารณะ":
							return "Use of public transportation system";
						case "การใช้ยานพาหนะไฟฟ้า":
							return "Use of electric vehicle";
						case "การเพิ่มประสิทธิภาพเครื่องยนต์":
							return "Improvement of the efficiency of engine";
						case "การเพิ่มประสิทธิภาพการใช้พลังงานในอาคารและโรงงาน และในครัวเรือน":
							return "Improvement of the efficiency of energy consumption in building and factory and in household";
						case "การปรับเปลี่ยนสารทำความเย็นธรรมชาติ":
							return "Use of natural refrigerant";
						case "การใช้วัสดุทดแทนปูนเม็ด":
							return "Use of clinker substitute";
						case "การจัดการขยะมูลฝอย":
							return "Solid waste management";
						case "การจัดการน้ำเสียชุมชน":
							return "Domestic wastewater management";
						case "การนำก๊าซมีเทนกลับมาใช้ประโยชน์":
							return "Methane recovery and utilization";
						case "การจัดการน้ำเสียอุตสาหกรรม":
							return "Industrial wastewater management";
						case "การลด ดูดซับ และกักเก็บก๊าซเรือนกระจกจากภาคป่าไม้และการเกษตร":
							return "Reduction, absorption and removal of greenhouse gases from the forestry and agriculture sectors";
						case "การดักจับ กักเก็บ และ/หรือใช้ประโยชน์จากก๊าซเรือนกระจก":
							return "Capture, storage, and/or utilization of greenhouse gas";
						default:
							return "Other project specified by the Board of Directors of TGO";
					}
				}
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
		async getVerificatedCreditStat() {
			const app = this;
			return await app.$axios
				.$get(`/api/v1/stats/statistics/project-type`)
				.then((resp) => {
					app.ChartData.labels = app._.clone(resp.labels);
					app.chartLabel = app._.clone(resp.labels);
					app.ChartData.datasets[0].data = resp.datasets;
					// app.$refs.verifiedCredit._data._chart.data.labels = app._.map(resp.labels,item=>app.ccmgm(item))
					// app.$refs.verifiedCredit._data._chart.config.type = 'horizontalBar'
					// console.log(app.$refs.verifiedCredit._data._chart);

					app.$refs.verifiedCredit._data._chart.update();
				})
				.catch((err) => err);
		},
	},
};
</script>

<style>
</style>