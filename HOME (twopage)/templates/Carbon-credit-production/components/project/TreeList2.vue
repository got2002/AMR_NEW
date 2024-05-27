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
				<ProjectCertifiedCarbonAccordion @deleteIssueCredit="deleteIssueCredit(data._id)" :vintageYear="item.year" :programID="programID" :project_id="project_id" :authorizedUse="authorizedUse" :additionalCertificationCode="additionalCertificationCode" :projectStandard="projectStandard" :projectTypeByExtens="projectTypeByExtens" @reload="$emit('reload')" :key="i + 'parent'" :item="data" />
				<!-- <div class="pl-8 space-y-2" :key="i + 'child'">
					<template v-for="(data2, idx) in data.cancellation">
						<div :key="idx" class="relative">
							<div class="absolute z-10 top-0 -left-8 border-l-2 border-b-2 h-6 w-6"></div>
							<div v-if="idx+1 !== data.cancellation.length" class="absolute z-10 top-6 -left-8 border-l-2 h-full w-6"></div>
							<ProjectCertifiedCarbonAccordionChildInfo :vintageYear="item.year" :programID="programID" :project_id="project_id" :authorizedUse="authorizedUse" :additionalCertificationCode="additionalCertificationCode" @reload="$emit('reload')" :item="data2" />
						</div>
					</template>
				</div> -->
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
		deleteIssueCredit(id) {
			const app = this;
			this.$swal
				.fire({
					icon: "info",
					iconColor: "#ef4444",
					iconHtml: `
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
									<path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
								</svg>
								`,
					title: this.$t("alert.title.warning_delete"),
					text: this.$t("alert.text.warning.delete"),
					showCancelButton: true,

					confirmButtonColor: "#ef4444",
					confirmButtonText: this.$t("button.confirm"),
					cancelButtonText: this.$t("button.cancel"),
					reverseButtons: true,
				})
				.then((result) => {
					if (result.isConfirmed) {
						app.$swal.fire({
							title: this.$t("sweetalert.waiting"),
							text: this.$t("saving"),
							allowOutsideClick: false,
							showCloseButton: false,
						});
						app.$swal.showLoading();
						app.$axios
							.$delete(`/api/v1/project/vintage/${id}`)
							.then((resp) => {
								app.$swal.close();
								app.$swal
									.fire({
										icon: "success",
										iconColor: "#059669",
										title: this.$t("alert.title.success.delete"),
										confirmButtonColor: "#059669",
									})
									.then(() => {
										// app.$router.push(app.localePath({ name: "project-id-edit", params: { id: app.$route.params.id } }));
										// location.reload()
										app.$emit("reload");
									});
							})
							.catch((err) => {
								app.$swal.close();
								app.$swal.fire({
									icon: "error",
									title: this.$t("alert.title.error.delete"),
								});
								console.log(err);
							});
					}
				});
		},
	},
};
</script>

<style>
</style>