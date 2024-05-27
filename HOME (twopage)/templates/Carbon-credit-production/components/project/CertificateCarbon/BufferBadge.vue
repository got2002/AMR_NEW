<template>
	<div class="text-center px-4 py-1 bg-stone-500 bg-opacity-10 rounded-full text-stone-500 border border-stone-500">{{ bufferCredit?.toLocaleString() }} tCO<sub>2</sub>eq</div>
</template>

<script>
export default {
	props: ["item"],
	computed: {
		bufferCredit() {
			const bufferIssue = this._.chain(this.item.buffers)
				.filter((data) => [1, 3].includes(data.buffer_type))
				.sumBy((data) => data.amount)
				.value();

			// console.log(bufferIssue);
			return bufferIssue ?? 0;
		},
	},
};
</script>

<style>
</style>