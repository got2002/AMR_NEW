<template>
    <div class="text-center px-4 py-1 bg-tgo-teal-500 bg-opacity-10 rounded-full text-tgo-teal-500 border border-tgo-teal-500">{{ IssuedCredit?.toLocaleString() }} tCO<sub>2</sub>eq</div>
</template>

<script>
export default {
    props:['item'],
    computed:{
        IssuedCredit() {
			const bufferIssue = this._.chain(this.item.buffers)
				.filter((data) => data.buffer_type === 2)
				.sumBy((data) => data.amount)
				.value();

			// console.log(bufferIssue);
			return this.item.amount + bufferIssue ?? 0;
		},
    }
}
</script>

<style>

</style>