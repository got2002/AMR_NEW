<template>
	<div class="w-80 relative">
		<div class="absolute z-50 bottom-3 left-0" :style="LabelPosition()">
			<div class="py-1 px-3 w-auto shadow-sm text-white text-center text-xs" :class="{ 'bg-green-700': color === 'green', 'bg-yellow-700': color === 'yellow' }">{{ start }} - {{ end }}</div>
		</div>
		<div :style="arrowLabel()" class="absolute z-50 bottom-2 w-2 h-2 transform rotate-45 text-white" :class="{ 'bg-green-700': color === 'green', 'bg-yellow-700': color === 'yellow' }"></div>
	</div>
</template>

<script>
	export default {
		props: ["max", "start", "end", "color"],
		methods: {
			blockWidth() {
				const len = this.end - this.start + 1;
				const b = (len / this.max) * 100;
				const c = (320 * b) / 100;

				return c;
			},
			blockStart(a) {
				const b = (a / this.max) * 100;
				const c = (320 * b) / 100;

				return c;
			},
			arrowLabel() {
				const s = this.blockStart(this.start) + this.blockWidth() / 3;

				const strLen = String(`${this.start} - ${this.end}`);
				const labelWidth = strLen.length;

				return `left:${Math.ceil(s) - 8}px`;
				
			},
			LabelPosition() {
				const s = this.blockStart(this.start) + this.blockWidth() / 3;

				const strLen = String(`${this.start} - ${this.end}`);
				const labelWidth = (strLen.length*2) + 24;
				

				if (this.blockStart(this.start) + (strLen.length + 24) >= 320) {
					return `right:-2px`;
				}
				return `left:${Math.ceil(s) - 8 - labelWidth}px`;
				
			},
		},
	};
</script>

<style></style>
