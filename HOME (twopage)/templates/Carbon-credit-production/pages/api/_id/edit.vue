<template>
	<section class="">
		<h2 class="mb-10 text-3xl font-bold">{{ $t("api.edit_page.page_title") }}</h2>
		<div class="flex items-start gap-4 p-5 bg-white rounded">
			<ApiSkeletonLoad v-if="isLoading" />
			<ApiForm  v-if="!isLoading" :form="form"></ApiForm>
			<div  v-if="!isLoading" class="w-5/12">
				<div class="bg-theme-black-50 p-6 w-full flex-col gap-3 mt-3 justify-between">
					<div class="text-lg font-bold">{{ $t("api.create_page.manual._0") }}</div>
					<div class="text-sm mt-2 w-full">
						<ul class="list-decimal list-inside">
							<li>{{ $t("api.create_page.manual._1") }}</li>
							<li>{{ $t("api.create_page.manual._2") }}</li>
							<li>{{ $t("api.create_page.manual._3") }}</li>
						</ul>
					</div>
				</div>
				<div class="w-full flex-col gap-3 mt-3 justify-between text-sm">
					<div v-if="form?.appId" class="text-sm font-bold">Access key</div>
					<div v-if="form?.appId" class="p-2 mb-5 col-span-1 flex items-center justify-start bg-tgo-teal-500 px-2 py-1 text-theme-black-50 rounded-full shadow-sm">
						<span class="font-semibold">{{ form.appId }}</span>
					</div>
					<button v-if="form?.appId" @click="reset()" class="text-sm font-bold text-tgo-teal-500 flex">
						{{ $t("button.reset") }} Secret key
						<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 ml-2 mt-1">
							<path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
						</svg>
					</button>
					<div v-if="isReset">
						<div class="text-sm font-bold">Secret key</div>
						<div class="p-2 col-span-1 flex items-center justify-between bg-tgo-teal-500 px-2 py-1 text-theme-black-50 rounded-full shadow-sm">
							<span class="font-semibold">{{ secret_key }}</span>
						</div>
					</div>
					<!-- <div class="relative w-full lg:w-auto ml-auto mt-10 flex justify-end">
						<div class="relative inline-flex flex-wrap items-stretch mb-1">
							<nuxt-link :to="localePath('api')" type="button" class="py-3 px-5 mr-2 mb-2 text-sm font-medium text-theme-black-300 bg-theme-black-50 hover:bg-tgo-teal-500 hover:text-gray-100 focus:z-10">กลับ</nuxt-link>
						</div>
					</div> -->
				</div>
			</div>
		</div>
		<div class="relative w-full lg:w-auto ml-auto my-4 flex justify-center">
			<div class="relative inline-flex flex-wrap items-stretch mb-1 gap-4">
				<nuxt-link :to="localePath('api')" type="button" class="w-20 py-2 text-center bg-gray-500 rounded shadow-sm text-white hover:bg-gray-600">{{ $t("button.close") }}</nuxt-link>
				<button type="button" @click="updateApi()" class="w-20 flex items-center justify-center py-2 text-white bg-yellow-500 hover:bg-yellow-600 hover:text-theme-white rounded shadow-sm">{{ $t("button.save") }}</button>
			</div>
		</div>
		
	</section>
</template>

<script>
	export default {
		name: "DocumentPage",
		layout: "DashboardLayout",
		middleware: ["auth"],
		asyncData({ params }) {
			const id = params.id;
			return { id };
		},
		data() {
			return {
				form: {},
				isLoading: true,
				dropdown: {
					scopes: [],
				},
				isReset: false,
				secret_key: "",
			};
		},
		async mounted() {
			await this.getScope();
			await this.getApi();
		},
		methods: {
			getScope() {
				const app = this;
				this.$axios.$get(`/api/v1/dropdown/app/scopes`).then((resp) => {
					app.dropdown.scopes = resp;
				});
			},
			async getApi() {
				const app = this;
				this.isLoading = true;
				await this.$axios
					.$get(`/api/v1/app/` + this.$route.params.id)
					.then((resp) => {
						// console.log(resp);
						app.form = resp;
						app.isLoading = false;
					})
					.catch((err) => {
						console.log(err);
						app.isLoading = false;
					});
			},
			updateApi() {
				const app = this;
				// console.log(this.form);
				app.$swal
					.fire({
						icon: "info",
						iconColor: "#f59e0b",
						iconHtml: `
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
									<path stroke-linecap="round" stroke-linejoin="round" d="M11.42 15.17L17.25 21A2.652 2.652 0 0021 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 11-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 004.486-6.336l-3.276 3.277a3.004 3.004 0 01-2.25-2.25l3.276-3.276a4.5 4.5 0 00-6.336 4.486c.091 1.076-.071 2.264-.904 2.95l-.102.085m-1.745 1.437L5.909 7.5H4.5L2.25 3.75l1.5-1.5L7.5 4.5v1.409l4.26 4.26m-1.745 1.437l1.745-1.437m6.615 8.206L15.75 15.75M4.867 19.125h.008v.008h-.008v-.008z" />
								</svg>
								`,
						title: this.$t("alert.title.warning"),
						text: this.$t("alert.text.warning.edit"),
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
								.$put(`/api/v1/app/` + this.$route.params.id, app.form)
								.then((resp) => {
									// console.log(resp);
									app.$swal.close();

									// app.form = resp;
									app.$swal
										.fire({
											icon: "success",
											iconColor:'#059669',
											confirmButtonColor: "#059669",
											title: this.$t("alert.title.success.edit"),
											text: this.$t("alert.text.success.edit"),
											timer: 2000,
											timerProgressBar: true,
										})
										.then(() => {
											app.$router.push(app.localePath({ name: "api" }));
										});
								})
								.catch((err) => {
									app.$swal.close();
									app.$swal.fire({
										icon: "error",
										title: this.$t("alert.title.error.edit"),
										text: this.$t("alert.text.error.edit"),
										timer: 2000,
										timerProgressBar: true,
									});

									console.log(err);
								});
						}
					});
			},
			reset() {
				const app = this;

				app.$swal
					.fire({
						icon: "info",
						iconColor: "#f59e0b",
						iconHtml: `
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
									<path stroke-linecap="round" stroke-linejoin="round" d="M15.75 5.25a3 3 0 013 3m3 0a6 6 0 01-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 17.25H8.25v2.25H6v2.25H2.25v-2.818c0-.597.237-1.17.659-1.591l6.499-6.499c.404-.404.527-1 .43-1.563A6 6 0 1121.75 8.25z" />
								</svg>

								`,
						title: this.$t("sweetalert.api.reset.title"),
						text: this.$t("sweetalert.api.reset.sub_title"),
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
								.$post(`/api/v1/app/token/${app.form._id}/reset`)
								.then((resp) => {
									app.$swal.close();
									app.isReset = true;
									// app.form = resp;
									app.secret_key = resp.appSecretKey;
									app.$swal.fire({
										icon: "success",
										iconColor:'#059669',
										title: this.$t("sweetalert.api.reset.success"),
										text: this.$t("sweetalert.api.success.sub_title"),
										confirmButtonColor: "#059669",
										confirmButtonText: app.$t("button.close"),
									});
								})
								.catch((err) => {
									app.$swal.close();

									app.$swal.fire({
										icon: "error",
										title: this.$t("sweetalert.api.reset.error"),
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
