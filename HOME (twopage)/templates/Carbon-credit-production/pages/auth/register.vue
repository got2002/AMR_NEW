<template>
	<div class="w-full h-full xl:my-20 lg:my-10 my-5">
		<div class="flex flex-col justify-center items-center">
			<div class="space-y-4 2xl:w-11/12 w-full">
				<UIStep :step="step" />
				<div class="bg-white border rounded shadow-sm p-4 relative">
					<ManyCircle />
					<AuthAccountType @click="step = 2" v-if="step == 1" :form="form" />
					<AuthPermission @click="step = 3" @cancel="step = 1" v-if="step == 2" :form="form" />

					<AuthGuestForm @click="step = 4" @cancel="step = 1" v-if="step == 3 && form.account_type == 0" :form="form" />
					<AuthFileForm1 @back="step = 3" @cancel="step = 1" @click="step = 5" v-if="step == 4 && form.account_type == 0" :form="form" />

					<AuthJuristicForm @click="step = 4" @cancel="step = 1" v-if="step == 3 && form.account_type == 1" :form="form" />
					<AuthFileForm2 @back="step = 3" @cancel="step = 1" @click="step = 5" v-if="step == 4 && form.account_type == 1" :form="form" />

					<AuthGovernmentForm @click="step = 4" @cancel="step = 1" v-if="step == 3 && form.account_type == 2" :form="form" />
					<AuthFileForm3 @back="step = 3" @cancel="step = 1" @click="step = 5" v-if="step == 4 && form.account_type == 2" :form="form" />

					<AuthGuestReview @back="step = 4" @cancel="step = 1" @click="submitForm" v-if="step == 5 && form.account_type == 0" :form="form" />
					<AuthJuristicReview @back="step = 4" @cancel="step = 1" @click="submitForm" v-if="step == 5 && form.account_type == 1" :form="form" />
					<AuthGovernmentReview @back="step = 4" @cancel="step = 1" @click="submitForm" v-if="step == 5 && form.account_type == 2" :form="form" />
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: "RegisterAccount",
	layout: "MainLayout",

	data() {
		return {
			accept: false,
			step: 1,
			isSubmitted: false,
			loading: false,
			baseUrl: process.env.baseUrl,
			form: {
				account_type: 0,
				consents: {
					for_notification: "",
					for_public_nonsensitive_information: "",
					for_development: "",
				},
				guest: {
					firstname: "",
					lastname: "",
					card_id: "",
					issued_by: "",
					phone_number: "",
					email: "",
					password: "",
					passwordConfirmation: "",
					address: "",
					province: "",
					district: "",
					subdistrict: "",
					postcode: "",
					accountName: "",
					request_permission: [],
					document: "",
				},
				juristic: {
					juristic_name: "",
					firstname: "",
					lastname: "",
					juristic_number: "",
					alien_number: "",
					card_id: "",
					issued_by: "",
					phone_number: "",
					email: "",
					password: "",
					passwordConfirmation: "",
					address: "",
					province: "",
					district: "",
					subdistrict: "",
					postcode: "",
					accountName: "",
					request_permission: [],
					juristic_document: {
						verified: "",
						authorize: "",
						// card_id_owner: "",
						card_id_representative: "",
						// employment_certificate: "",
					},
				},
				government: {
					government_name: "",
					firstname: "",
					lastname: "",

					card_id: "",

					phone_number: "",
					email: "",
					password: "",
					passwordConfirmation: "",
					address: "",
					province: "",
					district: "",
					subdistrict: "",
					postcode: "",
					accountName: "",
					request_permission: [],
					government_document: {
						verified: "",
						authorize: "",
						// card_id_owner: "",
						card_id_representative: "",
					},
				},
			},
		};
	},
	// created(){
	// 	this.$router.go(-1)
	// },
	watch: {
		step: function (val) {
			if (val === 1) this.resetForm();
		},
	},

	methods: {
		resetForm() {
			this.form = {
				account_type: 0,
				consents: {
					for_notification: "",
					for_public_nonsensitive_information: "",
					for_development: "",
				},
				guest: {
					firstname: "",
					lastname: "",
					card_id: "",
					issued_by: "",
					phone_number: "",
					email: "",
					password: "",
					passwordConfirmation: "",
					address: "",
					province: "",
					district: "",
					subdistrict: "",
					postcode: "",
					accountName: "",
					request_permission: [],
					document: "",
				},
				juristic: {
					juristic_name: "",
					firstname: "",
					lastname: "",
					juristic_number: "",
					alien_number: "",
					card_id: "",
					issued_by: "",
					phone_number: "",
					email: "",
					password: "",
					passwordConfirmation: "",
					address: "",
					province: "",
					district: "",
					subdistrict: "",
					postcode: "",
					accountName: "",
					request_permission: [],
					juristic_document: {
						verified: "",
						authorize: "",
						card_id_owner: "",
						card_id_representative: "",
						employment_certificate: "",
					},
				},
				government: {
					government_name: "",
					firstname: "",
					lastname: "",

					card_id: "",

					phone_number: "",
					email: "",
					password: "",
					passwordConfirmation: "",
					address: "",
					province: "",
					district: "",
					subdistrict: "",
					postcode: "",
					accountName: "",
					request_permission: [],
					government_document: {
						verified: "",
						authorize: "",
						card_id_owner: "",
						card_id_representative: "",
					},
				},
			};
		},
		submitForm() {
			this.isSubmitted = true;
			// this.$v.$touch();
			// if (this.$v.$invalid) {
			// 	return;
			// }
			const app = this;
			app.$swal
				.fire({
					icon: "info",
					iconColor: "#00b0d8",
					iconHtml: `
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
  <path stroke-linecap="round" stroke-linejoin="round" d="M12 10.5v6m3-3H9m4.06-7.19l-2.12-2.12a1.5 1.5 0 00-1.061-.44H4.5A2.25 2.25 0 002.25 6v12a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9a2.25 2.25 0 00-2.25-2.25h-5.379a1.5 1.5 0 01-1.06-.44z" />
</svg>

								`,
					title: this.$t("sweetalert.openAccount.confirm.title"),
					text: this.$t("sweetalert.openAccount.confirm.sub_title"),
					showCancelButton: true,

					confirmButtonColor: "#00b0d8",
					confirmButtonText: `${app.$t("button.confirm")}`,
					cancelButtonText: `${app.$t("button.cancel")}`,
					reverseButtons: true,
				})
				.then((result) => {
					if (result.isConfirmed) {
						app.$swal.fire({
							title: this.$t("sweetalert.waiting"),
							text: this.$t("loading"),
							allowOutsideClick: false,
							showCloseButton: false,
						});
						app.$swal.showLoading();

						app.$axios
							.$post(`/api/v1/user/openAccount`, app.form)
							.then((resp) => {
								app.$swal.close();
								// app.form = {
								// 	password: null,
								// 	passwordConfirmation: null,
								// };
								app.$swal
									.fire({
										icon: "success",
										iconColor: "#059669",
										confirmButtonColor: "#059669",
										title: this.$t("sweetalert.openAccount.success.title"),
										text: this.$t("sweetalert.openAccount.success.sub_title"),
									})
									.then(() => {
										app.$router.push(this.localePath({ name: "auth-signin" }));
									});
							})
							.catch((err) => {
								app.$swal.showLoading();
								app.$swal.fire({
									icon: "error",
									iconColor: "#ef4444",
									confirmButtonColor: "#ef4444",
									title: this.$t("sweetalert.openAccount.error.title"),
									text: this.$t("sweetalert.openAccount.error.sub_title"),
								});
								console.log(err);
							});
					}
				});
		},
	},
};
</script>

<style></style>
