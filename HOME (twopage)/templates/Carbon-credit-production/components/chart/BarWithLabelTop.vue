<script>
	import { Bar } from "vue-chartjs";

	export default {
		extends: Bar,
		props: ["data", "option", "topLabelData"],

		mounted() {
			const app = this;
			const topLabels = {
				id: "topLabels",
				afterDatasetsDraw: function (chart, args, pluginOption) {
					const ctx = chart.ctx;
					const xAxis = chart.scales["x-axis-0"];
					// const img = new Image();

					// const yAxis = chart.scales['y-axis-0']
					// console.log(xAxis.getPixelForValue(0), chart.getDatasetMeta(2).data[0]);
					ctx.font = "bold 14px Prompt";
					function numberFormat(value) {
						if (value < 0) return "";
						if (value === 0) return 0;
						if (value < 1e3) return value;
						if (value >= 1e3 && value < 1e6) return +(value / 1e3).toFixed(1) + "K";
						if (value >= 1e6 && value < 1e9) return +(value / 1e6).toFixed(1) + "M";
						if (value >= 1e9 && value < 1e12) return +(value / 1e9).toFixed(1) + "B";
						if (value >= 1e12) return +(value / 1e12).toFixed(1) + "T";
					}
					const angle = Math.PI / 180;
					if (app.topLabelData.datasets.length > 0) {
						chart.data.labels.forEach((label, i) => {
							const projectAmount = app.topLabelData.datasets[i] ?? 0;
							// console.log(projectAmount);
							// const medium = chart.data.datasets[1].data[i];
							// const small = chart.data.datasets[2].data[i];
							const top = chart.getDatasetMeta(0).data[i]._model.y;
							// const total = large + medium + small;
							// console.log(large,medium,small,'=',sum);
							// img.src = "/images/folder.png";
							// ctx.drawImage(img, xAxis.getPixelForValue(i)-14, top-26,26,26);
							ctx.beginPath();
							ctx.fillStyle = "#00b0d8";
							ctx.arc(xAxis.getPixelForValue(i), top - 20, 15, angle * 0, angle * 360, false);
							ctx.fill();
							ctx.closePath();

							ctx.fillStyle = "#fff";
							ctx.textAlign = "center";
							ctx.fillText(numberFormat(projectAmount), xAxis.getPixelForValue(i), top - 15);

							// if (total > 0) {
							// 	ctx.fillText(100, xAxis.getPixelForValue(i), top - 5);
							// }
						});
					}
				},
			};

			this.addPlugin(topLabels);

			this.renderChart(this.data, this.option);
		},
	};
</script>

<style></style>
