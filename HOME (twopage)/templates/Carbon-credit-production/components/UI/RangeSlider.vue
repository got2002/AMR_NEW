<template>
	<div class="w-full bg-gray-100 rounded-md flex items-center gap-2">
		<div class="w-48">
			<UINumberInput @change="setMinValue(Number($event))" :value="minValue" :min="0" :max="maxValue" customClass="px-4 py-3 text-center text-xs bg-white outline-none border border-gray-200 rounded-l w-full" />
		</div>
		<div class="w-full relative">
			<!-- <div class="absolute z-50 -top-4 bg-green-500 text-white px-2 py-1 text-xs rounded text-center" :style="`left:${labelPos}%`">
				<div class="relative">
					{{ minValue }}฿ - {{ maxValue }}฿
					<div class="absolute z-10 -bottom-2 left-1/2 w-2 h-2 bg-green-500 transform rotate-45"></div>
				</div>
			</div> -->
			<div class="slider">
				<div class="progress" :style="`left:${minRangePos}%;right:${maxRangePos}%`"></div>
			</div>

			<div class="range-input">
				<input @input="setMinValue($event.target.value)" type="range" ref="range-min" :min="0" :max="max" :value="minValue" />
				<input @input="setMaxValue($event.target.value)" type="range" ref="range-max" :min="min" :max="max" :value="maxValue" />
			</div>
		</div>
		<div class="w-48">
			<UINumberInput @change="setMaxValue(Number($event))" :value="maxValue" :min="0" :max="maxValue" customClass="px-4 py-3 text-center text-xs bg-white outline-none border border-gray-200 rounded-r w-full" />
		</div>
	</div>
</template>

<script>
export default {
	props: {
		min: {
			type: Number,
			default: () => 0,
		},
		max: {
			type: Number,
			default: () => 1000000,
		},
		minRangeValue: {
			type: Number,
			// default: () => 0,
		},
		maxRangeValue: {
			type: Number,
			// default: () => 1000000,
		},
	},

	data() {
		return {
			minValue: 0,
			maxValue: 0,

			minRangePos: 0,
			maxRangePos: 0,
		};
	},

	// watch: {
	// 	minRangeValue() {
	// 		this.setMinValue(this.minValue);
	// 	},
	// 	maxRangeValue() {
	// 		this.setMaxValue(this.maxValue);
	// 	},
	// 	min() {
	// 		this.setMinValue(this.minValue);
	// 	},
	// 	max() {
	// 		this.setMaxValue(this.maxValue);
	// 	},
	// },
	
	mounted() {
		this.setValue();
		
		this.setMinValue(this.minValue);
		this.setMaxValue(this.maxValue);
	},
	methods: {
		setValue() {
			this.minValue = this.min;
			this.maxValue = this.max;
		},
		setMinValue(value) {
			if (value === undefined || value >= this.maxValue) {
				this.$refs["range-min"].value = this.minValue;
				if (value === undefined) {
					this.minValue = 0;
				}
			} else {
				this.minValue = Math.min(parseInt(value), parseInt(this.maxValue) - 1);

				const percent = ((this.minValue - this.min) / (this.max - this.min)) * 100;

				this.minRangePos = percent;
				this.$emit("setMin", value);
			}
		},
		setMaxValue(value) {
			if (value === undefined || value <= this.minValue) {
				this.$refs["range-max"].value = this.maxValue;
				if (value === undefined) {
					this.maxValue = 0;
				}
			} else {
				this.maxValue = Math.max(parseInt(value), parseInt(this.minValue) + 1);

				var percent = ((this.maxValue - this.min) / (this.max - this.min)) * 100;

				this.maxRangePos = 100 - percent;
				if (this.maxRangePos <= 0) this.maxRangePos = 0;
				this.$emit("setMax", value);
			}
		},
	},
};
</script>

<style>
.slider {
	height: 5px;
	border-radius: 5px;
	background: #ddd;
	position: relative;
}
.slider .progress {
	height: 5px;
	left: 25%;
	right: 25%;
	border-radius: 5px;
	position: absolute;
	background: #10b981;
}
.range-input {
	position: relative;
}
.range-input input {
	position: absolute;
	top: -5px;
	height: 5px;
	width: 100%;
	background: none;
	-webkit-appearance: none;
	pointer-events: none;
}
input[type="range"]::-webkit-slider-thumb {
	height: 20px;
	width: 20px;
	border-radius: 50%;
	border: 1px solid #ddd;
	pointer-events: auto;
	-webkit-appearance: none;
	background: #fff;
	cursor: ew-resize;
}

input[type="range"]::-moz-range-thumb {
	height: 20px;
	width: 20px;
	border-radius: 50%;
	border: 1px solid #ddd;
	pointer-events: auto;
	-moz-appearance: none;
	background: #fff;
	cursor: ew-resize;
}
input[type="number"]::-webkit-inner-spin-button {
	appearance: none;
}
</style>