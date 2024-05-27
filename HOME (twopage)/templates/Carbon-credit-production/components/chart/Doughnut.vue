
<script>
import { Doughnut } from "vue-chartjs";
import ChartJsPluginDataLabels from "chartjs-plugin-datalabels";

export default {
	extends: Doughnut,
	props: ["data", "option"],

	mounted() {
		// const plugins = function (chart) {

		// 	// chart.chart.width = window.innerWidth + 10000
		// 	// chart.scales['x-axis-0'].min = "อ่างทอง"
		// 	console.log(chart);
		// 	chart.update()

		// };
		const app = this;
		const plugin = function (chart) {
			const width = chart.chart.width;
			const height = chart.chart.height;

			const ctx = chart.chart.ctx;
			ctx.restore();

			ctx.font = "bold 25px Prompt";
			ctx.textBaseline = "middle";
			const text = Number(chart.data.datasets[0].data.reduce((sum, n) => sum + n)).toLocaleString();
			const textX = Math.round((width - ctx.measureText(text).width) / 2);
			const textY = height / 1.95;
			ctx.fillStyle = "#0C3156";
			ctx.lineWidth = 3;
			ctx.fillText(text, textX, textY);
			ctx.save();
		};
		this.addPlugin(ChartJsPluginDataLabels);
		this.addPlugin({
			id: "my-chart",
			beforeDraw: plugin,
		});
		// this.addPlugin({
		// 	id: "my-chart",
		// 	afterDraw: this.drawLabelsLine,
		// });

		this.renderChart(this.data, this.option);

		// setTimeout(() => {
		// 	this.$data._chart.update();
		// });
		// console.log(this.$data._chart.canvas);
	},
	methods: {
		drawLabelsLine(context) {
			const chart = context.chart;
			const {
				ctx,
				chartArea: { top, bottom, left, right },
			} = chart;
			const width = right - left;
			const height = bottom - top;

			// console.log(top, bottom, left, right, width, height);
			chart.data.datasets.forEach((dataset, i) => {
				chart.getDatasetMeta(i).data.forEach((datapoint, index) => {
					// console.log(dataset);
					const { x, y } = datapoint.tooltipPosition();
					// ctx.fillStyle = dataset.backgroundColor[index]
					// ctx.fillRect(x,y,10,10)
					const halfWidth = width / 2;
					const halfHeight = height / 2;
					function getRandomInt(min, max) {
						return Math.floor(Math.random() * (max - min)) + min; // The maximum is exclusive and the minimum is inclusive
					}

					const xLine = x >= halfWidth ? x + 20 : x - 20;
					// console.log(xLine);

					const yLine = y >= halfHeight ? y + 35 : y - 35;
					const extraLine = x >= halfWidth ? 10 : -10;

					// line
					ctx.beginPath();
					ctx.moveTo(x, y);
					ctx.lineTo(xLine, yLine);
					ctx.lineTo(xLine + extraLine, yLine);
					ctx.strokeStyle = dataset.backgroundColor[index];
					ctx.stroke();

					// text value
					const textWidth = ctx.measureText(chart.data.labels[index]).width;
					ctx.font = "14px Prompt";

					// control position
					const textPosition = x >= halfWidth ? "left" : "right";
					const plusFivePx = x >= halfWidth ? 5 : -5;
					ctx.textAlign = textPosition;
					ctx.textBaseline = "middle";
					ctx.fillStyle = dataset.backgroundColor[index];
					// ctx.fillRect(xLine + extraLine + plusFivePx,yLine-10,-textWidth,20)
					let textValue = "";
					const value = chart.data.datasets[0].data[index];
					if (value < 1e3) textValue = value;
					if (value >= 1e3 && value < 1e6) textValue = +(value / 1e3).toFixed(1) + "K";
					if (value >= 1e6 && value < 1e9) textValue = +(value / 1e6).toFixed(1) + "M";
					if (value >= 1e9 && value < 1e12) textValue = +(value / 1e9).toFixed(1) + "B";
					if (value >= 1e12) textValue = +(value / 1e12).toFixed(1) + "T";
					// ctx.fillStyle = 'white';

					ctx.fillText(textValue, xLine + extraLine + plusFivePx, yLine);
				});
			});
		},
	},
};
</script>

<style>
</style>