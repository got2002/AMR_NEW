
<script>
import { Pie } from "vue-chartjs";
import ChartJsPluginDataLabels from 'chartjs-plugin-datalabels';
export default {
	extends: Pie,
	props: ["data", "option"],

	mounted() {
		// const app = this;
		
		this.addPlugin(ChartJsPluginDataLabels);
		
		this.renderChart(this.data, this.option);
		
		setTimeout(() => {
			this.$data._chart.update();
		});

		
		
		
		
	
	},
};
</script>

<style>
</style>