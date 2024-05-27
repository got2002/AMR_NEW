<template>
	<div>
		<div @click="drop = !drop" class="ml-4 mt-2 px-2 py-1 flex items-center justify-between w-full bg-white border rounded shadow-sm cursor-pointer">
			<div class="font-medium py-1 w-full flex items-center gap-2">
				<IconArrowDown class="transform " :class="{'-rotate-90 duration-200':!drop,'rotate-0 duration-200':drop}"/>
				{{ dateLocale(data.transaction_date) }}
			</div>
			<div class="w-full text-gray-500 text-right">{{ data.amount?.toLocaleString() }} (tCO<sub>2</sub>eq)</div>
		</div>
		<div v-if="drop" class="ml-4 px-2 py-1 border border-t-0 border-dashed w-full bg-gray-100">{{ getSerial }}</div>
	</div>
</template>

<script>
export default {
    
	props: ["data", "programID", "project_id", "vintageYear", "authorizedUse", "additionalCertificationCode"],
	data() {
		return {
			drop: false,
		};
	},
    computed: {
		getSerial() {
			// console.log(this.authorizedUse);
			return `TH1-${this.programID}-${this.project_id}-${this.data.day_batch_number}-${this.vintageYear}-${this.data.block_start}-${this.data.block_end}-${this.authorizedUse}-${this.additionalCertificationCode}`;
		},
	},
	methods: {
		dateLocale(date) {
			if (!date) return this.$t("undefined");
			else if (this.$i18n.locale === "th") {
				return this.$dayjs(date).locale("th").format("DD MMM BBBB");
			}
			return this.$dayjs(date).locale("en").format("DD MMM YYYY");
		},
	},
};
</script>

<style>
</style>