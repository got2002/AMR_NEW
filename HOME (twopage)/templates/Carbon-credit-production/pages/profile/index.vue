<template>
	<div class="h-full container mx-auto p-4">
		<ProfileSkeletonLoad v-if="isLoading"/>
		<div v-if="!isLoading" id="profile" class="mx-auto container 2xl:w-6/12 lg:w-8/12 sm:w-full xs:w-full">
			<div class="flex justify-between items-center pb-2">
				<div class="w-full flex items-center">
					<div>
						<h2 class="text-2xl font-bold">{{ $t("profile.title") }}</h2>
					</div>
				</div>
			</div>
			<div class="p-3 bg-white rounded">
				<div class="mb-3">
					<div class="bg-white border-b pb-2">
						<h2 class="font-semibold">{{ $t("profile.personal_info") }}</h2>
					</div>
				</div>
				<div class="grid grid-cols-2 gap-2 mt-3">
					<div>
						<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">{{ $t("profile.firstname") }}</label>
						<div class="w-full px-3 h-11 mb-1 bg-gray-100 rounded-sm flex items-center">
							{{ form.firstname }}
						</div>
						<!-- <div>
							<input v-model="form.firstname" class="w-full px-3 py-2 mb-1 bg-gray-100 border border-gray-300 rounded-sm focus:outline-none focus:border-indigo-500 transition-colors" required />
						</div> -->
						
					</div>

					<div>
						<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">{{ $t("profile.lastname") }}</label>
						<div>
							<div class="w-full px-3 h-11 mb-1 bg-gray-100 rounded-sm flex items-center">
								{{ form.lastname }}
							</div>
							<!-- <div>
								<input v-model="form.lastname" class="w-full px-3 py-2 mb-1 bg-gray-100 border border-gray-300 rounded-sm focus:outline-none focus:border-indigo-500 transition-colors" required />
							</div> -->
							<!-- <p class="text-xs text-red-500" v-if="!$v.form.lastname.required && isSubmitted">{{ $t("form_validation.require.lastname") }}</p>
							<p class="text-xs text-red-500" v-if="!$v.form.lastname.minLength && isSubmitted">{{ $t("form_validation.min_length.lastname") }}</p>
							<p class="text-xs text-red-500" v-if="!$v.form.lastname.containsNotSpecial && isSubmitted">{{ $t("form_validation.pattern.lastname_contain_special") }}</p> -->
							<!-- <span v-if="!$v.formx.uas_owner.address.district.required && isSubmitted" class="text-red-500 text-sm">{{ $t("form.signup.validate.required") }}</span> -->
						</div>
					</div>
					<div>
						<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">{{ $t("profile.organization") }}</label>
						<div class="w-full px-3 h-11 mb-1 bg-gray-100 rounded-sm flex items-center">
							{{ organizationName }}
						</div>
					</div>
					<div>
						<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">{{ $t("profile.role") }}</label>
						<div class="w-full px-3 h-11 mb-1 bg-gray-100 rounded-sm flex items-center">
							{{ roleName }}
						</div>
					</div>
					<div class="col-span-2">
						<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">{{ $t("profile.email") }}</label>
						<!-- <div>
							<input v-model="form.email" placeholder="example@defire.com" type="email" class="w-full px-3 py-2 mb-1 bg-gray-100 border border-gray-300 rounded-sm focus:outline-none focus:border-indigo-500 transition-colors" required />
							
						</div> -->
						<div class="w-full px-3 h-11 mb-1 bg-gray-100 rounded-sm flex items-center">
							{{ form.email }}
						</div>
						<p class="text-xs text-red-500" v-if="!$v.form.email.required && isSubmitted">{{ $t("form_validation.require.email") }}</p>
						<p class="text-xs text-red-500" v-if="!$v.form.email.email && isSubmitted">{{ $t("form_validation.pattern.email") }}</p>
					</div>
					<button @click="$router.push(localePath('/profile/changePassword'))" class="px-3 py-2 bg-blue-400 hover:bg-blue-500 border border-blue-600 text-white">
						{{ $t("button.change_password") }}
					</button>
				</div>

				<div class="bg-white border-b py-2">
					<h2 class="font-semibold">{{ $t("profile.notification_title") }}</h2>
				</div>
				<div class="grid grid-cols-1 gap-2 mt-4">
					<div class="col-span-1 flex items-center gap-2" v-for="(item, idx) in dropdowns.emailTopics" :key="idx">
						<label :for="`noti-${idx}`" class="w-10 h-6 px-0.5 rounded-full border flex items-center relative cursor-pointer transform" :class="{ 'bg-gray-100': !form.emailTopics.includes(item.value), 'bg-tgo-teal-500': form.emailTopics.includes(item.value) }">
							<div class="w-5 h-5 ml-0 rounded-full bg-white shadow-sm duration-100" :class="{ 'ml-0': !form.emailTopics.includes(item.value), 'ml-3.5': form.emailTopics.includes(item.value) }"></div>
						</label>
						<input v-model="form.emailTopics" :value="item.value" :id="`noti-${idx}`" type="checkbox" class="w-4 h-4 border-2 hidden" />
						<label>{{ item[$i18n.locale] }}</label>
					</div>
				</div>
			</div>

			<div class="flex justify-center gap-4 mt-3">
				<button class="w-28 py-2 text-center bg-gray-500 rounded shadow-sm text-white hover:bg-gray-600" @click="$router.push(localePath('/'))">
					<span class="text-center">{{ $t("button.close") }}</span>
				</button>
				<button @click="submitForm" class="w-28 gap-2 flex items-center justify-center py-2 text-white bg-tgo-teal-500 hover:bg-tgo-teal-600 hover:text-theme-white rounded shadow-sm">
					<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
						<path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
					</svg>

					{{ $t("button.save") }}
				</button>
			</div>
		</div>

		
	</div>
</template>

<script>
import { required, sameAs, minLength, email } from "vuelidate/lib/validators";

export default {
	name: "Profile",
	layout: "ProfileLayout",
	middleware: ["auth"],
	data() {
		return {
			isLoading: true,
			formcredit: {
				accountName: null,
			},
			select: {
				arr: [-1, -1],
				toggle: false,
			},
			isData: false,
			create: false,
			edit: false,
			isSubmitted: false,
			form: {
				email: null,

				firstname: null,
				lastname: null,
				middlename: "",

				role: -1,

				organization: -1,
				scopes: [],
				notifications: [],
				emailTopics: [],
				companyID: null,
			},
			dropdowns: {
				role: [],
				organization: [],
				userScopes: [],
				emailTopics: [],
			},
			Transaction: [],
		};
	},
	computed: {
		organizationName() {
			if(this.dropdowns.organization.length === 0) return "-";
			if(this.form.companyID){
				const org = this.dropdowns.organization.find((e) => e.value === this.form.companyID)
				return org[this.$i18n.locale];
			}else{
				return "-"
			}
		},
		roleName() {
			if(this.dropdowns.role.length === 0) return "-";
			if(this.form.role !== undefined || this.form.role !== null){
				const org = this.dropdowns.role.find((e) => e.value === this.form.role)
				return org.text;
			}else{
				return "-"
			}
		},
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
		await this.getEmailTopics();
		await this.getProfile();
		this.loading = false;

		// await this.getCredit();
	},
	methods: {
		mapRole(role) {
			const findd = this._.find(this.dropdowns.role, (item) => item.value === role);
			if (findd) return findd.text;
			return "-";
		},
		mapOrganization(id) {
			const findd = this._.find(this.dropdowns.organization, (item) => item.value === id);
			if (findd) return findd.text;
			return "-";
		},

		getEmailTopics() {
			const app = this;
			app.loading = true;

			this.$axios.$get(`/api/v1/dropdown/email-topics`).then((resp) => {
				app.dropdowns.emailTopics = resp;

				app.loading = false;
			});
		},
		cancle() {
			this.edit = !this.edit;
			this.getProfile();
		},

		submitForm() {
			this.isSubmitted = true;
			this.$v.$touch();
			if (this.$v.$invalid) {
				return;
			}

			const app = this;

			app.$swal
				.fire({
					icon: "info",
					iconColor: "#00b0d8",
					iconHtml: `
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
  <path stroke-linecap="round" stroke-linejoin="round" d="M11.42 15.17L17.25 21A2.652 2.652 0 0021 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 11-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 004.486-6.336l-3.276 3.277a3.004 3.004 0 01-2.25-2.25l3.276-3.276a4.5 4.5 0 00-6.336 4.486c.091 1.076-.071 2.264-.904 2.95l-.102.085m-1.745 1.437L5.909 7.5H4.5L2.25 3.75l1.5-1.5L7.5 4.5v1.409l4.26 4.26m-1.745 1.437l1.745-1.437m6.615 8.206L15.75 15.75M4.867 19.125h.008v.008h-.008v-.008z" />
</svg>




								`,
					title: this.$t("sweetalert.user.edit.confirm.title"),
					text: this.$t("sweetalert.user.edit.confirm.sub_title"),
					showCancelButton: true,

					confirmButtonColor: "#00b0d8",
					confirmButtonText: app.$t("button.confirm"),
					cancelButtonText: app.$t("button.cancel"),
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

						app.$axios
							.$put(`/api/v1/auth/update`, app.form)
							.then((resp) => {
								app.$swal.close();

								app.$swal.fire({
									icon: "success",
									iconColor: "#059669",
									confirmButtonColor: "#059669",
									title: app.$t("sweetalert.user.edit.success.title"),
									text: app.$t("sweetalert.user.edit.success.sub_title"),
									timer: 2000,
									timerProgressBar: true,
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
		async getProfile() {
			const app = this;
			this.isLoading = true;
			await this.$axios
				.$get(`/api/v1/auth/me`)
				.then((resp) => {
					app.form = resp;
					app.isLoading = false;
				})
				.catch((err) => {
					console.log(err);
					app.isLoading = false;
				});
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
	},
};
</script>

<style>
#profile .v-select .vs__dropdown-toggle {
	-webkit-appearance: none;
	-moz-appearance: none;
	appearance: none;
	background: #fff;

	border: 1px solid #e8e8e8 !important;

	border-radius: 0px !important;

	display: flex;
	align-items: center;
	padding: 6px 1px 6px 1px !important;
	white-space: normal;
}
</style>
