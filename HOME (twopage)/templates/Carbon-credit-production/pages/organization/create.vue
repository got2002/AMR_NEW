<template>
	<section class="pt-2 pb-4 lg:px-20 px-4 w-full">
		<div class="2xl:w-6/12 lg:w-11/12 w-full container mx-auto">
			<h2 class="text-3xl font-bold mb-4">{{ $t("organization.create.page_title") }}</h2>
			<OrganizationFormData ref="createForm" :form="form" :edit="true" :submitted="submitted"></OrganizationFormData>
			<div class="mt-4 flex items-center justify-between">
				<UIBackButton padding="px-4 py-3" @click="$router.push(localePath('/organization'))">{{ $t("button.back") }}</UIBackButton>
				<!-- <nuxt-link class="w-40 text-center border border-gray-500 py-3 bg-gray-300 hover:bg-gray-400 rounded shadow-sm" :to="localePath('/organization')">{{ $t("button.back") }}</nuxt-link> -->
				<button @click="AddOrganization" class="w-40 py-3 rounded bg-tgo-teal-500 hover:bg-tgo-teal-600 text-center text-white shadow-sm border border-tgo-teal-600">{{ $t("button.add") }}</button>
			</div>
		</div>
	</section>
</template>

<script>
export default {
	name: "CreateOrganizationPage",
	layout: "DashboardLayout",
	middleware: ["auth"],
	data() {
		return {
			form: {
				companyName: "",
				companyNameEn: "",
				fieldOfIndustry: "",
				fieldOfIndustryCustom: "",
				address: "",
				addressEn: "",
				province: "",
				district: "",
				subDistrict: "",
				postCode: null,
				phone: "",
				companyLogo: "",
				road: "",
				website: "",
				landArray: "",
				fax: "",
				village: "",
				organization_type: null,
			},
			submitted: false,
		};
	},

	methods: {
		AddOrganization() {
			const app = this;
			app.submitted = true;
			this.$refs.createForm.$v.$touch();

			if (this.$refs.createForm.$v.$invalid) {
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
					iconColor: "#00b0d8",
					iconHtml: `
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
									<path stroke-linecap="round" stroke-linejoin="round" d="M12 21v-8.25M15.75 21v-8.25M8.25 21v-8.25M3 9l9-6 9 6m-1.5 12V10.332A48.36 48.36 0 0012 9.75c-2.551 0-5.056.2-7.5.582V21M3 21h18M12 6.75h.008v.008H12V6.75z" />
								</svg>`,
					title: this.$t("alert.title.warning"),
					text: this.$t("alert.text.warning.default"),
					showCancelButton: true,

					confirmButtonColor: "#00b0d8",
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
							.$post(`/api/v1/organization`, app.form)
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
										app.$router.push(app.localePath("/organization"));
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
