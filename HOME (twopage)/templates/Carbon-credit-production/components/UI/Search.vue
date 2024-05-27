<template>
	<div class="relative">
		<div class="absolute z-10 top-2 right-2">
			<IconSearch customClass="w-6 h-6 text-gray-500"/>
		</div>
		<input ref="textinput" :placeholder="placeholder" :value="value" :type="type" @change="$emit('change')" v-on:keyup="$emit('keyup',$event.target.value)" @input="$emit('input', $event.target.value)" class="pl-4 pr-10 py-2 border border-gray-300 w-full rounded outline-none focus:border-green-500 bg-gray-50" />
	</div>
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
		placeholder: {
			type: String,
			default: () => "",
		},
	},
	updated() {
		// console.log(this.disabled);
		this.$refs.textinput.value = this.value;
	},
};
</script>

<style>
</style>