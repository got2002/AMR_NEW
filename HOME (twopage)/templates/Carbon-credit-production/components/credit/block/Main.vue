<template>
	<td class="">
		<div class="flex justify-center">
			<div class="w-80 bg-gray-200 border border-black shadow-sm flex items-center justify-center h-4 relative px-1">
				<div class="absolute z-10 w-full flex items-center justify-center divide-x divide-gray-400">
					<div class="w-1 h-3.5" v-for="i in 80" :key="i"></div>
				</div>
				<CreditBlockProgress 
				@showLabel="showMain_f" 
				@closeLabel="closeMain_f" 
				:blast="data.last_block_number" 
				:bfirst="data.first_block_number" 
				:bstart="data.block_start" 
				:bend="data.block_end" 
				:total="data.total_blocks"
				color="green"/>


				<CreditBlockProgress 
				v-if="data.allocated_block_start > 0" 
				@showLabel="showAllocate_f" 
				@closeLabel="closeAllocate_f" 
				:blast="data.last_block_number" 
				:bfirst="data.first_block_number" 
				:bstart="data.allocated_block_start" 
				:bend="data.allocated_block_end" 
				:total="data.total_blocks"
				color="yellow"/>
				
				<CreditBlockLabel v-if="showMain" color="green" :blast="data.last_block_number" :bfirst="data.first_block_number" :bstart="data.block_start" :bend="data.block_end"></CreditBlockLabel>
				<CreditBlockLabel v-if="showAllocate" color="yellow" :blast="data.last_block_number" :bfirst="data.first_block_number" :bstart="data.allocated_block_start" :bend="data.allocated_block_end" :total="data.total_blocks"></CreditBlockLabel>
			</div>
		</div>
	</td>
</template>

<script>
	export default {
		props: ["data"],
		data() {
			return {
				showAllocate: false,
				showMain: false,
			};
		},
		methods: {
			showAllocate_f() {
				// this.$emit("showLabel");
				this.showAllocate = true;
			},
			closeAllocate_f() {
				// this.$emit("closeLabel");
				this.showAllocate = false;
			},
			showMain_f() {
				// this.$emit("showLabel");
				this.showMain = true;
			},
			closeMain_f() {
				// this.$emit("closeLabel");
				this.showMain = false;
			},
		},
	};
</script>

<style></style>
