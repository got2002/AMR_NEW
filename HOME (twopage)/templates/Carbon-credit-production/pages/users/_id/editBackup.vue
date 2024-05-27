<template>
	<div class="w-full h-full">
		<div class="flex flex-col items-center justify-center">
			<div class="text-xl font-bold 2xl:w-5/12 lg:w-7/12 w-8/12 text-left mb-4">{{ $t("user.view.page_title") }}</div>
			<div class="border-b px-4 py-2 2xl:w-5/12 lg:w-7/12 w-8/12 bg-gray-50 rounded-t flex items-center justify-between shadow-sm">
				<span class="text-lg">#{{ form.userId }}</span>
				<span
					class="px-3 py-1 rounded"
					:class="{
						'bg-yellow-100 bg-opacity-40 border border-yellow-500 text-yellow-500': form.verificationStatus === 0,
						'bg-green-100 bg-opacity-40 border border-green-500 text-green-500': form.verificationStatus === 1,
					}"
					>{{ statusText(form.verificationStatus) }}</span
				>
			</div>
			<div class="2xl:w-5/12 lg:w-7/12 w-8/12 bg-white shadow-sm rounded-b p-4">
				<UserForm :form="form" :edit="true" :loading="isLoading"></UserForm>
			</div>
			<div class="2xl:w-5/12 lg:w-7/12 w-8/12 mt-4 flex items-center justify-between">
				<button @click="$router.push(localePath('/users'))" class="w-40 text-center rounded shadow-sm py-2 bg-gray-300 hover:bg-gray-400 text-sm">{{$t('button.back')}}</button>
				
				<button @click="updateUser"  class="w-40 text-center rounded shadow-sm py-2 bg-yellow-500 hover:bg-yellow-600 text-sm">{{$t('button.save')}}</button>
			</div>
		</div>

		<!-- <loadingCarbon v-if="isLoading"></loadingCarbon> -->
	</div>
</template>

<script>
	import { required, sameAs, minLength, email } from "vuelidate/lib/validators";

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
				edit_approval: {
					text: null,
					value: 0,
				},
				dropdowns: {
					role: [],
					organization: [],
					userScopes: [],
				},
				isSubmitted: false,
			};
		},
		validations() {
			return {
				form: {
					firstname: { required, containsNotSpecial: (value) => !/[?!$^*]/.test(value), minLength: minLength(2) },
					lastname: { required, containsNotSpecial: (value) => !/[?!$^*]/.test(value), minLength: minLength(2) },

					email: {
						required,
						email,
					},
				},
			};
		},
		async mounted() {
			await this.getRole();
			await this.getOrganization();
			await this.getUserScopes();
			await this.getData();
		},
		methods: {
			async getData() {
				const app = this;
				this.isLoading = true;
				await this.$axios
					.$get(`/api/v1/user/` + this.$route.params.id)
					.then((resp) => {
						// console.log(resp);
						app.form = resp;
						app.edit_approval = app._.clone(resp.verificationStatus);
						app.isData = true;
						app.isLoading = false;
					})
					.catch((err) => {
						console.log(err);
						app.isLoading = false;
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

					default:
						break;
				}
			},
			async getRole() {
				const app = this;
				await this.$axios
					.$get(`/api/v1/dropdown/roles`)
					.then((resp) => {
						// console.log(resp);
						app.dropdowns.role = resp;
					})
					.catch((err) => {
						console.log(err);
					});
			},
			async getOrganization() {
				const app = this;

				await this.$axios
					.$get(`/api/v1/dropdown/organization`)
					.then((resp) => {
						// console.log(resp);
						app.dropdowns.organization = resp;
					})
					.catch((err) => {
						console.log(err);
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
			updateUser() {
				const app = this;
				this.isSubmitted = true;
				this.$v.$touch();
				if (this.$v.$invalid) {
					return;
				}

				this.$swal
					.fire({
						icon:'info',
						iconColor:'#f59e0b',
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
						reverseButtons:true,
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
								.$put(`/api/v1/user/${app.$route.params.id}`, app.form)
								.then((resp) => {
									// console.log(resp);
									// app.form = resp;
									app.$swal.close();
									app.$swal.fire({
										icon: "success",
										iconColor:'#059669',
										confirmButtonColor: "#059669",
										title: app.$t("sweetalert.user.edit.success.title"),
										text: app.$t("sweetalert.user.edit.success.sub_title"),
										timer: 2000,
										timerProgressBar: true,
									}).then(()=>{
										app.$router.push(app.localePath({ name: "users"}));
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
			userRole(role) {
				switch (role) {
					case 0:
						return this.$t('user.role.user');
					case 1:
						return this.$t('user.role.registrar');;
					case 99:
						return this.$t('user.role.admin');;
					default:
						return "N/A";
				}
			},
			dateLocale(date) {
				if (this.$i18n.locale === "th") {
					return this.$dayjs(date).locale("th").format("DD MMM BBBB");
				}
				return this.$dayjs(date).locale("en").format("DD MMM YYYY");
			},
			datetime(date) {
				if (this.$i18n.locale === "th") {
					return this.$dayjs(date).locale("th").format("DD MMM BBBB (HH:mm)");
				}
				return this.$dayjs(date).locale("en").format("DD MMM YYYY (HH:mm)");
			},
			verification(value) {
				if (this.edit_approval.value === 1 && value === 1) {
					this.edit_approval.value = 0;
				} else if (this.edit_approval.value === 2 && value === 2) {
					this.edit_approval.value = 0;
				}
			},
		},

		metaInfo() {
			return { title: this.$t("home") };
		},
	};
</script>

<style></style>
