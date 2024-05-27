<template>
	<div class="w-80 relative">
		<div class="absolute z-50 bottom-3 left-0" :style="LabelPosition()">
			<div class="py-1 px-3 w-auto shadow-sm text-white text-center rounded-sm" :class="{ 'bg-green-700': color === 'green', 'bg-yellow-700': color === 'yellow' }">{{ bstart.toLocaleString() }} - {{ bend.toLocaleString() }}</div>
		</div>
		<div :style="arrowLabel()" class="absolute z-50 bottom-2 w-2 h-2 transform rotate-45 text-white" :class="{ 'bg-green-700': color === 'green', 'bg-yellow-700': color === 'yellow' }"></div>
	</div>
</template>

<script>
	export default {
		props: ["bfirst", "blast", "bstart", "bend", "total", "color"],
		methods: {
			blockWidth() {
				const start = this.bstart - this.bfirst;
				const end = this.bend - this.bfirst;
				const last = this.blast - this.bfirst;
				const len = end - start + 1;
				const b = (len / last) * 100;
				const c = (320 * b) / 100;

				return c;
			},
			blockStart(a) {
				const last = this.blast - this.bfirst + 1;

				const b = (a / last) * 100;
				const c = (320 * b) / 100;

				return c;
			},
			arrowLabel() {
				const start = this.bstart - this.bfirst;
				
				const arrowPosition = this.blockStart(start) + this.blockWidth() / 2;

				return `left:${Math.ceil(arrowPosition) - 8}px`;
			},
			LabelPosition() {
				const start = this.bstart - this.bfirst;

				const s = this.blockStart(start) + this.blockWidth() / 2;

				const strLen = String(`${this.bstart.toLocaleString()} - ${this.bend.toLocaleString()}`);
				const labelWidth = strLen.length * 2 + 24;

				if (this.blockStart(start) + (strLen.length + 24) >= 320) {
					return `right:-2px`;
				}
				return `left:${Math.ceil(s) - 8 - labelWidth}px`;
			},
		},
	};
</script>

<style></style>
