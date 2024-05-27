<template>
	<div class="flex justify-center relative">
		<div class="w-80 bg-gray-200 border border-black shadow-sm flex items-center justify-center h-4 relative px-1">
			<div class="absolute z-10 w-full flex items-center justify-center divide-x divide-gray-400">
				<div class="w-1 h-3.5" v-for="i in 80" :key="i"></div>
			</div>
			<HomeBlockProgress @showLabel="showMain_f" @closeLabel="closeMain_f" :totalBlock="data.total_blocks" :max="data.last_block_number" :start="data.block_start" :end="data.block_end"></HomeBlockProgress>
			<HomeBlockAllocateProgress v-if="data.allocated_block_start > 0" @showLabel="showAllocate_f" @closeLabel="closeAllocate_f" :max="data.last_block_number" :start="data.allocated_block_start" :end="data.allocated_block_end"></HomeBlockAllocateProgress>
			<HomeBlockLabel v-if="showMain" color="green" :totalBlock="data.total_blocks" :max="data.last_block_number" :start="data.block_start" :end="data.block_end"></HomeBlockLabel>
			<HomeBlockLabel v-if="showAllocate" color="yellow" :totalBlock="data.total_blocks" :max="data.last_block_number" :start="data.allocated_block_start" :end="data.allocated_block_end"></HomeBlockLabel>
		</div>
	</div>
</template>

<script>
	export default {
		props: ["data", "show"],
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
