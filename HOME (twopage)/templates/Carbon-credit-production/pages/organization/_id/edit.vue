<template>
	<section class="pt-2 pb-4 lg:px-20 px-4 w-full">
		<div class="2xl:w-6/12 lg:w-11/12 w-full container mx-auto">
			<h2 class="text-3xl font-bold mb-4">{{ $t("organization.create.page_title") }}</h2>
			<OrganizationFormDataEdit v-if="!loading" ref="editForm" :form="form" :edit="true" :submitted="submitted"></OrganizationFormDataEdit>
			<OrganizationSkeletonLoad v-else />
			<div class="mt-4 flex items-center justify-between">
				<UIBackButton padding="px-4 py-3" @click="$router.push(localePath('/organization'))">{{ $t("button.back") }}</UIBackButton>
				<!-- <nuxt-link class="w-40 text-center py-3 bg-gray-300 hover:bg-gray-400 rounded shadow-sm" :to="localePath('/organization')">{{ $t("button.back") }}</nuxt-link> -->
				<button @click="AddOrganization" class="w-40 py-3 rounded bg-yellow-500 hover:bg-yellow-600 text-center text-white shadow-sm">{{ $t("button.edit") }}</button>
			</div>
		</div>
	</section>
</template>

<script>
export default {
	name: "EditOrganizationPage",
	layout: "DashboardLayout",
	middleware: ["auth"],
	data() {
		return {
			loading: true,
			form: {
				// companyName: "",
				// companyNameEn: "",
				// fieldOfIndustry: "",
				// fieldOfIndustryCustom: "",
				// address: "",
				// addressEn: "",
				// province: "",
				// district: "",
				// subDistrict: "",
				// postCode: null,
				// phone: "",
				// companyLogo: "",
				// road: "",
				// website: "",
				// landArray: "",
				// fax: "",
				// village: "",
			},
			submitted: false,
		};
	},
	mounted() {
		this.getOrganizationInfo();
	},

	methods: {
		async getOrganizationInfo() {
			this.loading = true;
			this.form = await this.$axios
				.$get(`/api/v1/organization/${this.$route.params.id}`)
				.then((resp) => resp)
				.catch((err) => console.log(err));
			this.loading = false;
		},
		AddOrganization() {
			const app = this;
			app.submitted = true;

			this.$refs.editForm.$v.$touch();

			if (this.$refs.editForm.$v.$invalid) {
				this.$swal.fire({
					icon: "error",
					title: this.$t("sweetalert.invalid"),
					text: this.$t("sweetalert.complete_information"),
				});
				return;
			}
			this.$swal
				.fire({
					icon: "info",
					iconColor: "#f59e0b",
					iconHtml: `
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
									<path stroke-linecap="round" stroke-linejoin="round" d="M11.42 15.17L17.25 21A2.652 2.652 0 0021 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 11-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 004.486-6.336l-3.276 3.277a3.004 3.004 0 01-2.25-2.25l3.276-3.276a4.5 4.5 0 00-6.336 4.486c.091 1.076-.071 2.264-.904 2.95l-.102.085m-1.745 1.437L5.909 7.5H4.5L2.25 3.75l1.5-1.5L7.5 4.5v1.409l4.26 4.26m-1.745 1.437l1.745-1.437m6.615 8.206L15.75 15.75M4.867 19.125h.008v.008h-.008v-.008z" />
								</svg>
								`,
					title: this.$t("alert.title.warning"),
					text: this.$t("alert.text.warning.default"),
					showCancelButton: true,

					confirmButtonColor: "#f59e0b",
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
							.$put(`/api/v1/organization/${app.$route.params.id}`, app.form)
							.then((resp) => {
								// console.log(resp);

								// app.form = resp;
								app.$swal.close();
								app.$swal
									.fire({
										icon: "success",
										iconColor: "#059669",
										confirmButtonColor: "#059669",
										title: this.$t("alert.title.success.default"),
										timer: 2000,
										timerProgressBar: true,
									})
									.then(() => {
										app.getOrganizationInfo();
									});
							})
							.catch((err) => {
								app.$swal.close();
								app.$swal.fire({
									icon: "error",
									title: this.$t("alert.title.error.default"),
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
