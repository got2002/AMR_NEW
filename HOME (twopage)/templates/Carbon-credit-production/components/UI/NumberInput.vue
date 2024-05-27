<template>
	<input ref="textinput" :disabled="disabled" :value="value" type="number" :min="min" :max="max" :step="step" @input="$emit('input', $event.target.value)" :class="customClass" @change="$emit('change',$event.target.value)"/>
</template>

<script>
export default {
	props: {
		value: {
			default: () => "",
		},
		
		min: Number,
		max: Number,
		step: String,
		customClass: {
			type: String,
			default: () => "px-2 py-2 border border-gray-300 w-full rounded outline-none focus:border-green-500 bg-gray-50",
		},
		disabled:{
			type: Boolean,
			default: () => false,
		}
	},
	updated() {
		// console.log(this.disabled);
		this.$refs.textinput.value = this.value;
	},
};
</script>

<style>
</style>