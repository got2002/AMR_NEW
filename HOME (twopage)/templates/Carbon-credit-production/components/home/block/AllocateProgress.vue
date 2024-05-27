<template>
	<div class="max-w-full absolute z-20" :style="`left:${blockStart()}px`">
		<div @mouseenter="show1" @mouseleave="close" class="h-3 bg-yellow-600 bg-opacity-90 cursor-pointer hover:bg-yellow-700" :style="`width:${blockWidth()}px;`"></div>
	</div>
</template>

<script>
	export default {
		props: ["max", "start", "end"],
		computed: {},

		methods: {
			blockWidth() {
				const len = this.end - this.start + 1;
				const b = (len / this.max) * 100;
				const c = (320 * b) / 100;

				if (Math.floor(c) === 0) return 1
				else return Math.floor(c);
			},
			blockStart() {
				const b = (this.start / this.max) * 100;
				const c = (320 * b) / 100;

				return Math.floor(c);
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
