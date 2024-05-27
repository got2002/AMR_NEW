<template>
	<div class="w-full relative">
		<!-- <div v-if="loading" class="bg-black bg-opacity-25 absolute z-10 top-0 left-0 w-full h-full flex items-center justify-center">
			<p class="text-white">{{ $t("loading") }}</p>
		</div> -->
		<div class="flex items-center justify-between">
			<span class="font-semibold text-theme-black-300">{{ $t("statistics.chart.title.transfer_chart") }} </span>
			<div class="flex gap-2">
				<select @change="setDate()" v-model="dateunit" class="border rounded px-2 py-0.5 text-center text-base">
					<option value="daily">{{ $t("statistics.chart.filter.daily") }}</option>
					<option value="monthly">{{ $t("statistics.chart.filter.monthly") }}</option>
					<option value="yearly">{{ $t("statistics.chart.filter.yearly") }}</option>
				</select>
				<div class="w-72">
					<DatePicker @change="getData()" range-separator=" - " v-model="dateFilter" :type="dateType" :placeholder="$t('project.view_page.start_date') + ' - ' + $t('project.view_page.end_date')" :lang="$i18n.locale" range :formatter="thaiformatter" value-type="date" input-class="border rounded px-2 text-center py-1 text-base w-full"></DatePicker>
				</div>
			</div>
		</div>
		<div class="py-4 overflow-x-auto">
			<ChartBar ref="transfer" :data="ChartData" :option="ChartOptions" type="transfer" :height="300"></ChartBar>
		</div>
		<ChartLoading v-if="loading"></ChartLoading>
	</div>
</template>

<script>
	import thaiformatter from "../../mixins/thaiformatter";
	export default {
		mixins: [thaiformatter],
		data() {
			return {
				dateunit: "daily",
				dateFilter: [],
				loading: false,
				dateType: "date",
				ChartData: {
					labels: [],
					datasets: [
						{
							label: "Deposit",
							backgroundColor: "#00b0d8",

							data: [],
							// borderRadius:30
						},
						{
							label: "Cancellation",
							backgroundColor: "#c9da2a",

							data: [],
							// borderRadius:30
						},
						{
							label: "Voluntary",
							backgroundColor: "#00d8",

							data: [],
							// borderRadius:30
						},
						{
							label: "Market ",
							backgroundColor: "#124450d8",

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
									// callback: function (value, index, values) {
									// 	return `(${index + 1})`;
									// },
								},
								gridLines: { display: true },
							},
						],
						yAxes: [
							{
								// stacked: true,
								// scaleLabel: {
								// 	display: true,
								// 	fontFamily: '"Prompt", sans-serif',
								// 	fontSize: 10,
								// 	labelString: this.$t("statistics.chart.labels.carbon_credits_classified_by_project_type") + " CCMGM ",
								// },
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
									min: 0,
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
								// console.log(tooltipItem,data);
								let label = data.datasets[tooltipItem.datasetIndex].label || "";

								if (label) {
									label += ": ";
								}
								label += tooltipItem.yLabel.toLocaleString();
								return label;
							},
						},
					},

					legend: {
						display: true,
						position: "bottom",
						labels:{
							boxWidth:14,
							padding:30,
							fontFamily: '"Prompt", sans-serif',
							fontStyle:'bold',
							fontSize:14
						}
					},
					title: {
						display: false,
					},

					// plugins: {
					// 	datalabels: {
					// 		color: "#fff",
					// 		display: false,
					// 		align: "center",
					// 		formatter: function (value) {
					// 			if (value <= 0) return "";
					// 			if (value < 1e3) return value;
					// 			if (value >= 1e3 && value < 1e6) return +(value / 1e3).toFixed(1) + "K";
					// 			if (value >= 1e6 && value < 1e9) return +(value / 1e6).toFixed(1) + "M";
					// 			if (value >= 1e9 && value < 1e12) return +(value / 1e9).toFixed(1) + "B";
					// 			if (value >= 1e12) return +(value / 1e12).toFixed(1) + "T";
					// 		},

					// 		font: {
					// 			size: 10,
					// 			weight: "bold",
					// 			family: '"Prompt", sans-serif',
					// 		},
					// 	},
					// },
				},
			};
		},
		mounted() {
			// this.setDate();
			this.getData();
		},
		methods: {
			setDate() {
				this.dateFilter = [];
				this.getData();
			},
			async getData() {
				const app = this;
				app.loading = true;
				if (this.dateunit === "daily" && (this.dateFilter.length === 0 || this.dateFilter.includes(null))) {
					this.dateFilter = [this.$dayjs().subtract(6, "day").toDate(), this.$dayjs().toDate()];
					this.dateType = "date";
				} else if (this.dateunit === "monthly" && (this.dateFilter.length === 0 || this.dateFilter.includes(null))) {
					this.dateFilter = [this.$dayjs().startOf("year").toDate(), this.$dayjs().endOf("year").toDate()];
					this.dateType = "month";
				} else if (this.dateunit === "yearly" && (this.dateFilter.length === 0 || this.dateFilter.includes(null))) {
					this.dateFilter = [this.$dayjs().subtract(4, "year").toDate(), this.$dayjs().toDate()];
					this.dateType = "year";
				}
				const startDate = app.$dayjs(this.dateFilter[0]).format("YYYY-MM-DD");
				const endDate = app.$dayjs(this.dateFilter[1]).format("YYYY-MM-DD");
				await app.$axios.$get(`/api/v1/stats/statistics/transaction-amount?dateunit=${this.dateunit}&start_date=${startDate}&end_date=${endDate}`).then((resp) => {
					if (app.dateunit === "monthly") {
						// console.log("Monthly");
						app.ChartData.labels = app._.map(resp.label, (l) => {
							return app.$dayjs(l).locale(app.$i18n.locale).format("MMMM");
						});
					} else if (app.dateunit === "yearly") {
						app.ChartData.labels = app._.map(resp.label, (l) => {
							if (app.$i18n.locale === "th") return app.$dayjs(l).locale(app.$i18n.locale).format("BBBB");
							else return app.$dayjs(l).locale(app.$i18n.locale).format("YYYY");
						});
					} else {
						app.ChartData.labels = app._.map(resp.label, (l) => {
							if (app.$i18n.locale === "th") return app.$dayjs(l).locale(app.$i18n.locale).format("DD MMM BBBB");
							else return app.$dayjs(l).locale(app.$i18n.locale).format("DD MMM YYYY");
						});
					}

					const bgColor = ["#00b0d8", "#E90064", "#7286D3", "#03C988", "#F2CD5C"];
					app.ChartData.datasets = app._.map(resp.data, (item, i) => {
						let temp = {
							label: item.typeId[app.$i18n.locale],
							backgroundColor: bgColor[i],

							data: item.amounts,
							// borderRadius:30
						};
						return temp;
					});
				});
				app.loading = false;

				app.$refs.transfer._data._chart.update();
			},
		},
	};
</script>

<style>
	/* option:disabled{
	background-color: rgb(202, 202, 202);
	color: rgb(238, 238, 238);
	cursor: not-allowed;
} */
</style>
