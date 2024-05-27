<template>
	<div class="absolute z-20" :style="`left:${blockStart()}px`">
		<div @mouseenter="show1" @mouseleave="close" :class="{ 'bg-green-600 hover:bg-green-700': color === 'green', 'bg-yellow-600 hover:bg-yellow-700': color === 'yellow' }" class="h-3 bg-opacity-90 cursor-pointer" :style="`width:${blockWidth()}px;`"></div>
	</div>
</template>

<script>
	export default {
		props: ["bfirst", "blast", "bstart", "bend", "total", "color"],
		computed: {},

		methods: {
			blockWidth() {
				const last = this.blast - this.bfirst + 1;
				const blockEnd = this.bend - this.bfirst + 1;
				const blockStart = this.bstart - this.bfirst;
				const width = ((blockEnd-blockStart) / last) * 100;
				const toPixel = (320 * width) / 100;
				if (toPixel > 0 && toPixel < 1) return toPixel;
				else if (Math.floor(toPixel) === 0) return this.total;
				else return Math.floor(toPixel);
			},
			blockStart() {
				const last = this.blast - this.bfirst + 1;
				const blockStart = this.bstart - this.bfirst;
				const width = (blockStart / last) * 100;
				const toPixel = (320 * width) / 100;
				return Math.floor(toPixel);
			},
			show1() {
				this.$emit("showLabel");
			},
			close() {
				this.$emit("closeLabel");
			},
		},
	};
</script>

<style></style>
