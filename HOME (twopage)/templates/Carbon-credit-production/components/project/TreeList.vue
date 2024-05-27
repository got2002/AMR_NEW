<template>
	<div class="w-full">
		<div @click="expand = !expand" class="hover:bg-gray-200 py-2 px-2 cursor-pointer flex items-center gap-2" :class="{ 'bg-gray-100': expand }">
			<div class="transform" :class="{ 'rotate-0 duration-200': expand, '-rotate-90 duration-200': !expand }">
				<IconArrowDown />
			</div>

			<div class="flex items-center justify-between text-sm gap-2 w-full">
				<div>
					<span>{{ $t("project.create_page.vintage_year") }}</span>
					<span>{{ dateVintage(item.year) }} </span>
				</div>

				<div class="text-sm text-gray-500 text-left">{{ $t("unit.total") }} {{ sumTotal?.toLocaleString() }} tCO<sub>2</sub>eq</div>
			</div>
		</div>
		<div v-if="expand" class="w-full pl-6 py-4 space-y-2">
			<template v-for="(data, i) in item.data">
				<ProjectCertifiedCarbonAccordionInfo :key="i + 'parent'" :item="data" :vintageYear="item.year" :programID="programID" :project_id="project_id" :authorizedUse="authorizedUse" :additionalCertificationCode="additionalCertificationCode" :projectStandard="projectStandard" :projectTypeByExtens="projectTypeByExtens"/>
				<div :key="i + 'child'" v-if="data.cancellation.length > 0">
					<ProjectCertifiedCarbonAccordionChildInfo :vintageYear="item.year" :programID="programID" :project_id="project_id" :authorizedUse="authorizedUse" :additionalCertificationCode="additionalCertificationCode" @reload="$emit('reload')" :item="data" />

					<!-- <template v-for="(data2, idx) in data.cancellation"> -->
					<!-- <div class="absolute z-10 top-0 -left-8 border-l-2 border-b-2 h-6 w-6"></div>
							<div v-if="idx+1 !== data.cancellation.length" class="absolute z-10 top-6 -left-8 border-l-2 h-full w-6"></div> -->

					<!-- </template> -->
				</div>
			</template>
		</div>
	</div>
</template>

<script>
export default {
	props: ["item", "programID", "project_id", "authorizedUse", "additionalCertificationCode","projectStandard","projectTypeByExtens"],
	data: () => {
		return {
			expand: false,
		};
	},

	computed: {
		sumTotal() {
			const total = this._.sumBy(this.item.data, (item) => item.amount+item.buffer_amount??0);
			return total;
		},
	},
	methods: {
		dateVintage(year) {
			if (this.$i18n.locale === "th") return Number(year) + 543;
			else return year;
		},
	},
};
</script>

<style>
</style>