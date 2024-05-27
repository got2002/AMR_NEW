<template>
	<section class="">
		<h2 class="mb-5 text-3xl font-bold">{{ $t("api.create_page.page_title") }}</h2>
		<div class="flex items-start gap-4 p-5 bg-white shadow-sm">
			<ApiForm :form="form"></ApiForm>
			<div class="w-5/12">
				<div class="bg-theme-black-50 p-6 w-full flex-col gap-3 mt-3 justify-between">
					<div class="text-lg font-bold">{{ $t("api.create_page.manual._0") }}</div>
					<div class="text-sm mt-2">
						<ul class="list-decimal list-inside">
							<li>{{ $t("api.create_page.manual._1") }}</li>
							<li>{{ $t("api.create_page.manual._2") }}</li>
							<li>{{ $t("api.create_page.manual._3") }}</li>
						</ul>
					</div>
				</div>
			</div>
		</div>
		<div class="relative w-full lg:w-auto ml-auto my-4 flex justify-center">
			<div class="relative inline-flex flex-wrap items-stretch mb-1 gap-4">
				<nuxt-link :to="localePath('api')" type="button" class="w-20 py-2 text-center bg-gray-500 rounded shadow-sm text-white hover:bg-gray-600">{{ $t("button.close") }}</nuxt-link>
				<button type="button" @click="createApi()" class="w-20 flex items-center justify-center py-2 text-white bg-tgo-teal-500 hover:bg-tgo-teal-600 rounded shadow-sm">{{ $t("button.create") }}</button>
			</div>
		</div>
	</section>
</template>

<script>
	export default {
		name: "DocumentPage",
		layout: "DashboardLayout",
		middleware: ["auth"],
		data() {
			return {
				form: {
					name: "",
					description: "",
					email: "",
					fullName: "",
					scopes: [],
					accountNumber: "",
				},

				created: false,
				access_key: "",
				secret_key: "",
			};
		},
		async mounted() {},
		methods: {
			createApi() {
				const app = this;
				console.log(this.form);
				app.$swal
					.fire({
						icon: "info",
						iconColor: "#00b0d8",
						iconHtml: `
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
									<path stroke-linecap="round" stroke-linejoin="round" d="M15.75 5.25a3 3 0 013 3m3 0a6 6 0 01-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 17.25H8.25v2.25H6v2.25H2.25v-2.818c0-.597.237-1.17.659-1.591l6.499-6.499c.404-.404.527-1 .43-1.563A6 6 0 1121.75 8.25z" />
								</svg>


								`,
						title: this.$t("sweetalert.api.create.title"),
						text: this.$t("sweetalert.api.create.sub_title"),
						showCancelButton: true,

						confirmButtonColor: "#00b0d8",
						confirmButtonText: this.$t("button.create"),
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
								.$post(`/api/v1/app`, app.form)
								.then((resp) => {
									// console.log(resp);
									app.$swal.close();

									app.$swal
										.fire({
											icon: "success",
											iconColor:'#059669',
											confirmButtonColor: "#059669",
											title: app.$t("sweetalert.api.success.title"),

											html: `<div class="">
													<p>${app.$t("sweetalert.api.success.sub_title")}</p>
													<div>
														<label class="font-bold text-sm">Access Key</label>
														<p class="text-xs p-2 bg-gray-50 border">${resp.appId}</p>
													</div>
													<div>
														<label class="font-bold text-sm">Secret Key</label>
														<p class="text-xs p-2 bg-gray-50 border">${resp.appSecretKey}</p>
													</div>
											
													</div>`,
											
											confirmButtonText: app.$t("button.close"),
											width: "33em",
										})
										.then(() => {
											app.$router.push(app.localePath(`/api`));
										});
								})
								.catch((err) => {
									app.$swal.close();
									app.$swal.fire({
										icon: "error",
										title: this.$t("sweetalert.api.error.title"),
										text: this.$t("sweetalert.api.error.sub_title"),
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
