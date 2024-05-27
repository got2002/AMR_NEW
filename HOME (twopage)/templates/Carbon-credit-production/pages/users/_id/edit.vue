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
				<div>
					<!-- <button @click="$router.push(localePath(`/users`))" class="w-40 text-center rounded shadow-sm py-2 border border-gray-400 bg-gray-300 hover:bg-gray-400 text-sm">{{ $t("button.back") }}</button> -->
					<UIBackButton @click="$router.push(localePath(`/users`))" padding="py-2 px-4" class="text-sm">{{ $t("button.back") }}</UIBackButton>
					<button @click="updateUser" class="w-40 text-center rounded shadow-sm py-2 border border-yellow-600 bg-yellow-500 hover:bg-yellow-600 text-sm text-white">{{ $t("button.save") }}</button>
				</div>
			</div>

			<div class="grid grid-cols-10">
				<div @click="step = 1" :class="{ 'bg-white rounded-tr-xl drop-shadow-md': step == 1, 'bg-tgo-teal-100': step != 1 }" class="col-span-2 py-4 text-center cursor-pointer">{{ $t("general_information") }}</div>
				<div @click="step = 2" :class="{ 'bg-white rounded-t-xl': step == 2, 'bg-tgo-teal-100 ': step != 2 }" class="col-span-2 py-4 text-center cursor-pointer">{{ $t("consents") }}</div>
				<div @click="step = 3" :class="{ 'bg-white rounded-t-xl': step == 3, 'bg-tgo-teal-100 ': step != 3 }" class="col-span-2 py-4 text-center cursor-pointer">{{ $t("user.change_password_tab") }}</div>
			</div>

			<div class="bg-white shadow-sm rounded-b p-4" v-if="step == 1">
				<!-- <UserApproveForm :form="form" :edit="false" :loading="isLoading"></UserApproveForm> -->
				<UserGuestAccountEdit ref="guest" :form="form" :isSubmitted="isSubmitted" v-if="form.account_type == 0" />
				<UserJuristicAccountEdit ref="juristic" :form="form" :isSubmitted="isSubmitted" v-if="form.account_type == 1" />
				<UserGovernmentAccountEdit ref="government" :form="form" :isSubmitted="isSubmitted" v-if="form.account_type == 2" />

				<div class="w-full" v-if="!isLoading">
					<UILabel :text="$t('user.create_page.form.permission')" />
					<t-select v-model="form.scopes" multiple :closeOnSelect="false" :options="dropdowns.userScopes" :hideSearchBox="true" valueAttribute="value" :textAttribute="$i18n.locale">
						<template slot="option" slot-scope="{ isSelected, option }">
							<div class="px-3 py-1" :class="{ 'bg-tgo-teal-300': isSelected }">
								<span>{{ option.raw[$i18n.locale] }}</span>
							</div>
						</template>
					</t-select>
				</div>
				<UserSkeletonLoad v-if="isLoading" />
			</div>
			<div class="bg-white shadow-sm rounded-b p-4" v-else-if="step === 2">
				<UserConsents :form="form" />

				<UserSkeletonLoad v-if="isLoading" />
			</div>
			<div class="bg-white shadow-sm rounded-b p-4" v-else-if="step === 3">
				<UserChangePasswordForm :userForm="form" />

				<UserSkeletonLoad v-if="isLoading" />
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
			step: 1,
			isSubmitted: false,
			invalidForm: false,
		};
	},

	async mounted() {
		await this.getUserScopes();

		await this.getData();

		// if(this.form.verificationStatus !== 0){

		// 	this.$router.push(this.localePath(`/users/${this.$route.params.id}/edit`))
		// }
	},
	methods: {
		async getData() {
			this.isLoading = true;
			await this.$axios
				.$get(`/api/v1/user/${this.$route.params.id}/account_edit`)
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
		async getUserScopes() {
			const app = this;

			await this.$axios
				.$get(`/api/v1/dropdown/user/scopes`)
				.then((resp) => {
					// console.log(resp);
					app.dropdowns.userScopes = resp;
				})
				.catch((err) => {
					console.log(err);
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

		updateUser() {
			const app = this;
			this.isSubmitted = true;
			this.invalidForm = false;
			if(this.form.account_type === 0) this.invalidForm = this.$refs.guest?.validateForm();
			else if(this.form.account_type === 1) this.invalidForm = this.$refs.juristic?.validateForm();
			else if(this.form.account_type === 2) this.invalidForm = this.$refs.government?.validateForm();

			if(this.invalidForm) {
				return
			}

			this.$swal
				.fire({
					icon: "info",
					iconColor: "#f59e0b",
					iconHtml: `
									<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
										<path stroke-linecap="round" stroke-linejoin="round" d="M11.42 15.17L17.25 21A2.652 2.652 0 0021 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 11-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 004.486-6.336l-3.276 3.277a3.004 3.004 0 01-2.25-2.25l3.276-3.276a4.5 4.5 0 00-6.336 4.486c.091 1.076-.071 2.264-.904 2.95l-.102.085m-1.745 1.437L5.909 7.5H4.5L2.25 3.75l1.5-1.5L7.5 4.5v1.409l4.26 4.26m-1.745 1.437l1.745-1.437m6.615 8.206L15.75 15.75M4.867 19.125h.008v.008h-.008v-.008z" />
									</svg>`,
					title: this.$t("sweetalert.user.edit.confirm.title"),
					text: this.$t("sweetalert.user.edit.confirm.sub_title"),
					showCancelButton: true,

					confirmButtonColor: "#f59e0b",
					confirmButtonText: `${app.$t("button.confirm")}`,
					cancelButtonText: `${app.$t("button.cancel")}`,
					reverseButtons: true,
				})
				.then((result) => {
					if (result.isConfirmed) {
						app.$swal.fire({
							title: app.$t("sweetalert.waiting"),
							text: app.$t("saving"),
							allowOutsideClick: false,
							showCloseButton: false,
						});
						app.$swal.showLoading();
						// app.form.verificationStatus = app.edit_approval.value;
						app.$axios
							.$put(`/api/v1/user/${app.$route.params.id}/information`, app.form)
							.then((resp) => {
								// console.log(resp);
								// app.form = resp;
								app.$swal.close();
								app.$swal
									.fire({
										icon: "success",
										iconColor: "#059669",
										confirmButtonColor: "#059669",
										title: app.$t("sweetalert.user.edit.success.title"),
										text: app.$t("sweetalert.user.edit.success.sub_title"),
										timer: 2000,
										timerProgressBar: true,
									})
									.then(() => {
										app.$router.push(app.localePath({ name: "users-id-info",params:{id:app.$route.params.id} }));
									});
							})
							.catch((err) => {
								app.$swal.close();
								app.$swal.fire({
									icon: "error",
									title: app.$t("sweetalert.user.edit.error.title"),
									text: app.$t("sweetalert.user.edit.error.sub_title"),
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
