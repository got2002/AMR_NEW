<template>
	<input ref="textinput" :disabled="disabled" :value="value" :type="type" @input="$emit('input', $event.target.value)" :class="customClass" @change="$emit('change')" v-on:keyup="$emit('keyup',$event.target.value)"/>
</template>

<script>
export default {
	props: {
		value: {
			default: () => "",
		},
		type: {
			type: String,
			default: () => "text",
		},
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
		if(this.$refs.textinput) this.$refs.textinput.value = this.value;
		
	},
};
</script>

<style>
</style>