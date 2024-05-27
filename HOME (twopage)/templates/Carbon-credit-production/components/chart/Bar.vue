<script>
import { Bar } from "vue-chartjs";
import ChartJsPluginDataLabels from "chartjs-plugin-datalabels";


export default {
	extends: Bar,
	props: ["data", "option"],

	mounted() {
		// const plugins = function (chart) {

		// 	// chart.chart.width = window.innerWidth + 10000
		// 	// chart.scales['x-axis-0'].min = "อ่างทอง"
		// 	console.log(chart);
		// 	chart.update()

		// };
		// const app = this;
		// const topLabels = {
		// 	id: "topLabels",
		// 	afterDatasetsDraw: function (chart, args, pluginOption) {
		// 		// console.log(chart);
		// 		const ctx = chart.ctx;
		// 		const xAxis = chart.scales["x-axis-0"];
		// 		// const yAxis = chart.scales['y-axis-0']
		// 		// console.log(xAxis.getPixelForValue(0), chart.getDatasetMeta(2).data[0]);
		// 		ctx.font = "bold 14px Prompt";
		// 		ctx.fillStyle = "#0C3156";
		// 		ctx.textAlign = "center";
		// 		chart.data.labels.forEach((label, i) => {
		// 			const large = chart.data.datasets[0].data[i];
		// 			const medium = chart.data.datasets[1].data[i];
		// 			const small = chart.data.datasets[2].data[i];
		// 			const top = chart.getDatasetMeta(2).data[i]._model.y;
		// 			const total = large + medium + small;
		// 			// console.log(large,medium,small,'=',sum);
		// 			if (total > 0) {
		// 				ctx.fillText(total, xAxis.getPixelForValue(i), top - 5);
		// 			}
		// 		});
		// 	},
		// };
		// this.addPlugin(ChartJsPluginDataLabels);
		// this.addPlugin(topLabels);
		// this.addPlugin({
		// 	id:'horizontal-chart',
		// 	afterDraw:function(context){
		// 		context.chart.config.type = 'horizontalBar'
		// 		context.chart.update()
		// 	}
		// });

		this.renderChart(this.data, this.option);

	
	},
};
</script>

<style>
</style>