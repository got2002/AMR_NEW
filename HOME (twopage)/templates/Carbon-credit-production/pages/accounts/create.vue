<template>
	<div>
		<div class="container mx-auto 2xl:px-96 lg:px-40 px-10">
			<div class="flex justify-between items-center pb-2">
				<div class="w-full flex items-center mb-5">
					<span class="inline-flex justify-center items-center w-14 h-14 mr-4 bg-tgo-teal-500 rounded text-white">
						<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
							<path stroke-linecap="round" stroke-linejoin="round" d="M21 12a2.25 2.25 0 00-2.25-2.25H15a3 3 0 11-6 0H5.25A2.25 2.25 0 003 12m18 0v6a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 18v-6m18 0V9M3 12V9m18 0a2.25 2.25 0 00-2.25-2.25H5.25A2.25 2.25 0 003 9m18 0V6a2.25 2.25 0 00-2.25-2.25H5.25A2.25 2.25 0 003 6v3" />
						</svg>
					</span>
					<div>
						<h2 class="text-2xl font-bold">{{ $t("account.create_page.page_title") }}</h2>
						<p class="text-sm text-gray-500 font-medium">{{ $t("account.create_page.subtitle") }} (<span class="text-red-600">*</span>)</p>
					</div>
				</div>
			</div>

			<div class="grid grid-cols-1 md:grid-cols-1 lg:grid-cols-1 xl:grid-cols-1 2xl:grid-cols-1 gap-4">
				<div class="w-full bg-white shadow rounded">
					<AccountCreateForm ref="createForm" :form="form" :isSubmitted="isSubmitted" class="flex flex-col p-3 w-full" />
				</div>
			</div>

			<div class="flex justify-center gap-4 mt-3">
				<!-- <button class="w-20 py-2 text-center bg-gray-500 rounded shadow-sm text-white hover:bg-gray-600" @click="$router.push(localePath({ name: 'accounts' }))">
					<span class="text-center">{{ $t("button.back") }}</span>
				</button> -->
				<UIBackButton @click="$router.push(localePath({ name: 'accounts' }))">{{ $t("button.back") }}</UIBackButton>
				<button @click="submitForm" class="w-20 flex items-center justify-center py-2 text-white bg-tgo-teal-500 hover:bg-tgo-teal-600 hover:text-theme-white rounded shadow-sm">
					<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
						<path stroke-linecap="round" stroke-linejoin="round" d="M10.125 2.25h-4.5c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125v-9M10.125 2.25h.375a9 9 0 019 9v.375M10.125 2.25A3.375 3.375 0 0113.5 5.625v1.5c0 .621.504 1.125 1.125 1.125h1.5a3.375 3.375 0 013.375 3.375M9 15l2.25 2.25L15 12" />
					</svg>

					{{ $t("button.save") }}
				</button>
			</div>
		</div>

		<loadingCarbon v-if="isLoading" />
	</div>
</template>

<script>
	export default {
		name: "CreateAccount",
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
					userEmail: null,
					accountName: null,
					accountTypeID: null,
					transactionTypeID: null,
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
						iconColor: "#00b0d8",
						iconHtml: `
									<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
  <path stroke-linecap="round" stroke-linejoin="round" d="M21 12a2.25 2.25 0 00-2.25-2.25H15a3 3 0 11-6 0H5.25A2.25 2.25 0 003 12m18 0v6a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 18v-6m18 0V9M3 12V9m18 0a2.25 2.25 0 00-2.25-2.25H5.25A2.25 2.25 0 003 9m18 0V6a2.25 2.25 0 00-2.25-2.25H5.25A2.25 2.25 0 003 6v3" />
</svg>
`,

						title: this.$t("alert.title.warning"),
						text: this.$t("alert.text.warning.create"),
						showCancelButton: true,
						reverseButtons: true,

						confirmButtonColor: "#00b0d8",
						confirmButtonText: `${app.$t("button.confirm")}`,
						cancelButtonText: `${app.$t("button.cancel")}`,
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
								.$post(`/api/v1/account`, app.form)
								.then((resp) => {
									// console.log(resp);
									app.$swal.close();

									// app.form = resp;
									app.$swal
										.fire({
											icon: "success",
											iconColor:'#059669',
											confirmButtonColor: "#059669",
											title: this.$t("alert.title.success.create"),
											timer: 2000,
											timerProgressBar: true,
										})
										.then(() => {
											app.$router.push(app.localePath({ name: "accounts" }));
										});
								})
								.catch((err) => {
									app.$swal.close();
									app.$swal.fire({
										icon: "error",
										title: this.$t("alert.title.error.create"),
									});

									console.log(err);
								});
						}
					});
			},
		},
	};
</script>

<style scoped></style>
