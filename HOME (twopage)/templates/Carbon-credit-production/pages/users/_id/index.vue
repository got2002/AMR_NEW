<template>
	<div class="w-full h-full">
		<div class="mx-auto container 2xl:w-11/12 lg:9/12 w-full">
			<div class="text-xl font-bold flex items-center justify-between mb-4">
				<div>
					<p>{{ $t("user.view.approve_page_title") }}</p>
					<p v-if="form.account_type == 0" class="text-green-500 text-sm">{{ $t("openAccount.form.guest.subtitle") }}</p>
					<p v-if="form.account_type == 1" class="text-green-500 text-sm">{{ $t("openAccount.form.juristic.subtitle") }}</p>
					<p v-if="form.account_type == 2" class="text-green-500 text-sm">{{ $t("openAccount.form.government.subtitle") }}</p>
				</div>

				<button @click="$router.push(localePath(`/users`))" class="w-40 text-center rounded shadow-sm py-2 border border-gray-400 bg-gray-300 hover:bg-gray-400 text-sm">{{ $t("button.back") }}</button>
			</div>

			<div class="bg-white shadow-sm rounded p-4">
				<!-- <UserApproveForm :form="form" :edit="false" :loading="isLoading"></UserApproveForm> -->
				<UserGuestAccount :form="form" v-if="form.account_type == 0" />
				<UserJuristicAccount :form="form" v-if="form.account_type == 1" />
				<UserGovernmentAccount :form="form" v-if="form.account_type == 2" />

				<UserSkeletonLoad v-if="isLoading" />
			</div>
			<div class="my-4 flex items-center justify-center sticky bottom-4">
				<div class="w-1/2 flex divide-x bg-white rounded-full shadow-lg border border-gray-400">
					<button @click="approve(1)" class="w-1/2 flex gap-1 text-center justify-center rounded-l-full py-2 hover:bg-green-600 hover:text-white text-sm">
						<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
							<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
						</svg>
						{{ $t("button.approve") }}
					</button>
					<button @click="approve(2)" class="w-1/2 flex gap-1 text-center justify-center rounded-r-full py-2 hover:bg-red-600 hover:text-white text-sm">
						<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
							<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
						</svg>
						{{ $t("button.reject") }}
					</button>
				</div>
			</div>
		</div>

		<!-- <loadingCarbon v-if="isLoading"></loadingCarbon> -->
	</div>
</template>

<script>
export default {
	name: "EditUser",
	layout: "DashboardLayout",
	middleware: ["auth"],
	computed: {},
	asyncData({ params }) {
		const id = params.id;
		return { id };
	},
	data() {
		return {
			isLoading: true,
			isData: false,
			form: {},
			id: null,
			edit: false,
			dropdowns: {
				role: [],
				organization: [],
				userScopes: [],
			},
		};
	},

	async mounted() {
		await this.getData();
		// if(this.form.verificationStatus !== 0){

		// 	this.$router.push(this.localePath(`/users/${this.$route.params.id}/edit`))
		// }
	},
	methods: {
		async getData() {
			this.isLoading = true;
			await this.$axios
				.$get(`/api/v1/user/${this.$route.params.id}/account`)
				.then((resp) => {
					// console.log(resp);
					this.form = resp;

					this.isLoading = false;
				})
				.catch((err) => {
					console.log(err);
					this.isLoading = false;
				});
		},
		statusText(status) {
			switch (status) {
				case 0:
					if (this.$i18n.locale === "th") return "รอยืนยัน";
					else return "pending";
				case 1:
					if (this.$i18n.locale === "th") return "ยืนยันแล้ว";
					else return "approve";
				case 2:
					if (this.$i18n.locale === "th") return "ปฏิเสธ";
					else return "Rejected";

				default:
					break;
			}
		},

		fullname(data) {
			return data.firstname + " " + data.lastname;
		},
		role(role) {
			switch (role) {
				case 0:
					return "User";
				case 1:
					return "Moderator";
				case 99:
					return "Admin";
				default:
					return "N/A";
			}
		},
		dateLocale(date) {
			if (this.$i18n.locale === "th") {
				return this.$dayjs(date).locale("th").format("DD MMM BBBB");
			}
			return this.$dayjs(date).locale("en").format("DD MMM YYYY");
			// return this.$dayjs(date).locale("en").format("DD MMM YYYY");
		},
		datetime(date) {
			if (this.$i18n.locale === "th") {
				return this.$dayjs(date).locale("th").format("DD MMM BBBB (HH:mm)");
			}
			return this.$dayjs(date).locale("en").format("DD MMM YYYY (HH:mm)");
		},

		approve(approveValue) {
			const app = this;
			this.$swal
				.fire({
					icon: "info",
					iconColor: approveValue === 1 ? "#10b981" : "#ef4444",
					iconHtml:
						approveValue === 1
							? `
									<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
										<path stroke-linecap="round" stroke-linejoin="round" d="M10.125 2.25h-4.5c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125v-9M10.125 2.25h.375a9 9 0 019 9v.375M10.125 2.25A3.375 3.375 0 0113.5 5.625v1.5c0 .621.504 1.125 1.125 1.125h1.5a3.375 3.375 0 013.375 3.375M9 15l2.25 2.25L15 12" />
									</svg>
									`
							: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
										<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m6.75 12H9m1.5-12H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
									</svg>
									`,
					title: this.$t("alert.title.warning"),
					// text: this.$t("alert.text.warning.default"),
					showCancelButton: true,

					confirmButtonColor: approveValue === 1 ? "#10b981" : "#ef4444",
					confirmButtonText: this.$t("button.confirm"),
					cancelButtonText: this.$t("button.cancel"),
					reverseButtons: true,

					input: "text",
					inputLabel: approveValue === 1 ? app.$t("sweetalert.account.input.label1") : app.$t("sweetalert.account.input.label2"),

					inputPlaceholder: app.$t("sweetalert.account.input.placeholder"),
					inputValidator: (value) => {
						if (!value && approveValue === 2) {
							return app.$t("sweetalert.account.input.error_msg");
						}
					},
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
							.$post(`/api/v1/user/${app.form._id}/approval`, {
								status: approveValue,
								remark: result.value,
							})
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
										if (approveValue === 1) app.$router.push(app.localePath(`/users/${app.form._id}/info`));
										else app.$router.push(app.localePath(`/users`));
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

<style scoped>
.vs__dropdown-toggle {
	-webkit-appearance: none;
	-moz-appearance: none;
	appearance: none;
	background: #fff;
	background: var(--vs-search-input-bg);
	border: 2px solid #eeee !important;
	border: var(--vs-border-width) var(--vs-border-style) var(--vs-border-color);
	border-radius: 4px;
	display: flex;
	padding: 6px;
	white-space: normal;
}
</style>
