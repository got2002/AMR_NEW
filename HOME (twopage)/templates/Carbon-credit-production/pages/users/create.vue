<template>
	<div>
		<div class="container mx-auto 2xl:px-96 lg:px-5">
			<div class="flex justify-between items-center pb-2">
				<div class="w-full flex items-center mb-5">
					<span class="inline-flex justify-center items-center w-14 h-14 mr-4 bg-tgo-teal-500 rounded text-white">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
						</svg>
					</span>
					<div>
						<h2 class="text-2xl font-bold">{{ $t("user.create_page.page_title") }}</h2>
						<p class="text-sm text-gray-500 font-medium">{{ $t("user.create_page.subtitle") }} (<span class="text-red-600">*</span>)</p>
					</div>
				</div>
			</div>

			<div class="grid grid-cols-1 md:grid-cols-1 lg:grid-cols-1 xl:grid-cols-1 2xl:grid-cols-1 gap-4 bg-white p-4 shadow-sm rounded">
				<UserCreateForm ref="createForm" :form="form" :isSubmitted="isSubmitted" class="col-span-1" />
				<div class="col-span-1 flex items-center gap-2">
					<input v-model="form.createAccount" type="checkbox" name="add-account" class="w-5 h-5 border-2 rounded-sm" />
					<label>{{ $t("button.create_account") }}</label>
				</div>
				<UserAccountForm v-if="form.createAccount" ref="createForm" :form="form" :isSubmitted="isSubmitted" class="col-span-1"></UserAccountForm>
			</div>

			<div class="flex justify-center gap-4 mt-3">
				<!-- <button class="w-24 py-2 text-center bg-gray-500 rounded shadow-sm text-white hover:bg-gray-600" @click="$router.push(localePath({ name: 'users' }))">
					<span class="text-center">{{ $t("button.back") }}</span>
				</button> -->
				<UIBackButton  @click="$router.push(localePath({ name: 'users' }))">{{ $t("button.back") }}</UIBackButton>
				<button @click="submitForm" class="w-24 gap-2 flex items-center justify-center py-2 text-white bg-tgo-teal-500 hover:bg-tgo-teal-600 hover:text-theme-white rounded shadow-sm">
					<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
						<path stroke-linecap="round" stroke-linejoin="round" d="M10.125 2.25h-4.5c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125v-9M10.125 2.25h.375a9 9 0 019 9v.375M10.125 2.25A3.375 3.375 0 0113.5 5.625v1.5c0 .621.504 1.125 1.125 1.125h1.5a3.375 3.375 0 013.375 3.375M9 15l2.25 2.25L15 12" />
					</svg>

					{{ $t("button.create") }}
				</button>
			</div>
		</div>

		<loadingCarbon v-if="isLoading" />
	</div>
</template>

<script>

	export default {
		name: "CreateUser",
		layout: "DashboardLayout",
		middleware: ["auth"],
		components: {},
		computed: {},
		data() {
			return {
				isLoading: false,
				isData: false,
				isSubmitted: false,
				form: {
					email: null,
					password: null,
					firstname: null,
					lastname: null,
					middlename: "",

					role: null,
					passwordConfirmation: null,
					scopes: [],

					createAccount: false,

					accountName: "",

					accountTypeID: "",
					account_type: -1,
					companyID: null,
				},
			};
		},

		async mounted() {},
		methods: {
			submitForm() {
				this.isSubmitted = true;
				this.$refs.createForm.$v.$touch();
				if (this.$refs.createForm.$v.$invalid) {
					return;
				}

				const app = this;

				app.$swal
					.fire({
						icon: "info",
						iconColor:'#00b0d8',
						iconHtml: `
									<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
										<path stroke-linecap="round" stroke-linejoin="round" d="M19 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zM4 19.235v-.11a6.375 6.375 0 0112.75 0v.109A12.318 12.318 0 0110.374 21c-2.331 0-4.512-.645-6.374-1.766z" />
									</svg>`,
						title: this.$t("sweetalert.user.create.confirm.title"),
						text: this.$t("sweetalert.user.create.confirm.sub_title"),
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
								text: this.$t("saving"),
								allowOutsideClick: false,
								showCloseButton: false,
							});
							app.$swal.showLoading();

							app.$axios
								.$post(`/api/v1/user`, app.form)
								.then((resp) => {
									app.$swal.close();
									app.$swal
										.fire({
											icon: "success",
											iconColor:'#059669',
											confirmButtonColor: "#059669",
											title: this.$t("sweetalert.user.create.success.title"),
											text: this.$t("sweetalert.user.create.success.sub_title"),
											timer: 2000,
											timerProgressBar: true,
										})
										.then(() => {
											app.$router.push(app.localePath({ name: "users" }));
										});
								})
								.catch((err) => {
									app.$swal.close();
									app.$swal.fire({
										icon: "error",
										title: this.$t("sweetalert.user.create.error.title"),
										text: this.$t("sweetalert.user.create.error.sub_title"),
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
	.pulse-animate {
		animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
	}
	@keyframes pulse-animate {
		0%,
		100% {
			opacity: 1;
		}
		50% {
			opacity: 0.5;
		}
	}
</style>
