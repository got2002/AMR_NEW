<template>
	<div class="flex flex-col h-full">
		<div class="mb-3">
			<div class="bg-white border-b pb-2">
				<h2 class="font-semibold">{{ $t("user.create_page.form.title") }}</h2>
			</div>
			<div id="user__form" class="grid grid-cols-2 gap-2 mt-3">
				<div>
					<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">{{ $t("user.create_page.form.firstname") }}<span class="text-red-600">*</span></label>
					<div>
						<input v-model="form.firstname" class="w-full px-3 py-2 mb-1 bg-white border border-gray-300 rounded outline-none focus:border-indigo-500 transition-colors" required />
					</div>
					<p class="text-xs text-red-500" v-if="!$v.form.firstname.required && isSubmitted">{{ $t("form_validation.require.firstname") }}</p>
					<p class="text-xs text-red-500" v-if="!$v.form.firstname.containsNotSpecial && isSubmitted">{{ $t("form_validation.pattern.firstname_contain_special") }}</p>
					<p class="text-xs text-red-500" v-if="!$v.form.firstname.minLength && isSubmitted">{{ $t("form_validation.min_length.firstname") }}</p>
				</div>

				<div>
					<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">{{ $t("user.create_page.form.lastname") }}<span class="text-red-600">*</span></label>
					<div>
						<div>
							<input v-model="form.lastname" class="w-full px-3 py-2 mb-1 bg-white border border-gray-300 rounded focus:outline-none focus:border-indigo-500 transition-colors" required />
						</div>
						<p class="text-xs text-red-500" v-if="!$v.form.lastname.required && isSubmitted">{{ $t("form_validation.require.lastname") }}</p>
						<p class="text-xs text-red-500" v-if="!$v.form.lastname.minLength && isSubmitted">{{ $t("form_validation.min_length.lastname") }}</p>
						<p class="text-xs text-red-500" v-if="!$v.form.lastname.containsNotSpecial && isSubmitted">{{ $t("form_validation.pattern.lastname_contain_special") }}</p>

						<!-- <span v-if="!$v.formx.uas_owner.address.district.required && isSubmitted" class="text-red-500 text-sm">{{ $t("form.signup.validate.required") }}</span> -->
					</div>
				</div>
				<div>
					<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">{{ $t("user.create_page.form.account_type") }}<span class="text-red-600">*</span></label>
					<div class="border border-gray-300 rounded">
						<UIDropdownSearch v-model="form.account_type" :options="dropdowns.account_types" valueAttr="value" textAttr="text" :searchable="false"/>
					</div>
					<p class="text-xs text-red-500" v-if="!$v.form.account_type.selectDropdown && isSubmitted">{{ $t("form_validation.require.account_type") }}</p>
				</div>
				<div>
					<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">{{ $t("user.create_page.form.role") }}<span class="text-red-600">*</span></label>
					<!-- <div>
						<select v-model="form.role" class="w-full px-3 py-2 mb-1 bg-white border border-gray-300 rounded focus:outline-none focus:border-indigo-500 transition-colors" required>
							<option disabled :value="-1">{{ $t("user.create_page.form.dropdowns.role.all") }}</option>

							<option v-for="role in dropdowns.role" :key="role.value" :value="role.value">{{ role.text }}</option>
						</select>
					</div> -->
					<div class="border border-gray-300 rounded">
						<UIDropdownSearch v-model="form.role" :options="dropdowns.role" valueAttr="value" textAttr="text" :searchable="false"/>
					</div>
					<p class="text-xs text-red-500" v-if="!$v.form.role.selectDropdown && isSubmitted">{{ $t("form_validation.require.role") }}</p>
				</div>
				<div class="col-span-2" v-if="[1,2].includes(form.account_type)">
					<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">{{ $t("user.create_page.form.organization") }}<span class="text-red-600">*</span></label>
					<div>
						<!-- <select v-model="form.companyID" class="w-full px-3 py-2 mb-1 bg-white border border-gray-300 rounded focus:outline-none focus:border-indigo-500 transition-colors" required>
							<option disabled :value="-1">{{ $t("user.create_page.form.dropdowns.organization.all") }}</option>
							<option v-for="organization in dropdowns.organization" :key="organization.value" :value="organization.value">{{ organization[$i18n.locale] }}</option>
						</select> -->
						<!-- <v-select v-model="form.companyID" :options="dropdowns.organization" :reduce="(item) => item.value" :label="$i18n.locale"></v-select> -->
						<div class="border border-gray-300 rounded">
							<UIDropdownSearch v-model="form.companyID" :options="dropdowns.organization" valueAttr="value" :textAttr="$i18n.locale"/>
						</div>
					</div>
					<p class="text-xs text-red-500" v-if="!$v.form.companyID.required && isSubmitted">{{ $t("form_validation.require.organization") }}</p>
				</div>
				<div class="col-span-2">
					<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">{{ $t("user.create_page.form.email") }}<span class="text-red-600">*</span></label>
					<div>
						<input v-model="form.email" placeholder="example@gmail.com" type="email" class="w-full px-3 py-2 mb-1 bg-white border border-gray-300 rounded focus:outline-none focus:border-indigo-500 transition-colors" required />
						<!-- <span v-if="!$v.formx.uas_owner.address.province.required && isSubmitted" class="text-red-500 text-sm">{{ $t("form.signup.validate.required") }}</span> -->
					</div>
					<p class="text-xs text-red-500" v-if="!$v.form.email.required && isSubmitted">{{ $t("form_validation.require.email") }}</p>
					<p class="text-xs text-red-500" v-if="!$v.form.email.email && isSubmitted">{{ $t("form_validation.pattern.email") }}</p>
				</div>
				<div class="col-span-2">
					<label>{{ $t("user.create_page.form.permission") }}</label>
					<t-select  v-model="form.scopes" multiple :options="dropdowns.userScopes" :closeOnSelect="false" :hideSearchBox="true" valueAttribute="value" :textAttribute="$i18n.locale">
						<template slot="option" slot-scope="{ isSelected, option }">
							<div class="px-3 py-1" :class="{ 'bg-tgo-teal-300': isSelected }">
								<span>{{ option.raw[$i18n.locale] }}</span>
							</div>
						</template>
					</t-select>
				</div>
				<div>
					<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">{{ $t("user.create_page.form.password") }}<span class="text-red-600">*</span></label>
					<!-- <div>
							<input v-model="form.password" type="password" class="w-full px-3 py-2 mb-1 bg-white border border-gray-300 rounded focus:outline-none focus:border-indigo-500 transition-colors" required />
						</div> -->
					<div class="relative">
						<div class="absolute z-10 top-2 right-2 cursor-pointer" @click="showPassword1">
							<svg v-if="typeInput1 == 'password' && form.password" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
								<path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
								<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
							</svg>
							<svg v-else-if="typeInput1 != 'password' && form.password" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
								<path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
							</svg>
						</div>
						<input v-model="form.password" :type="typeInput1" class="w-full px-3 py-2 mb-1 bg-white border border-gray-300 rounded focus:outline-none focus:border-indigo-500 transition-colors" required />

						<!-- <input v-model="form.password" :type="typeInput1" class="w-full px-3 py-2 mb-1 bg-white border border-gray-300 rounded focus:outline-none focus:border-indigo-500 transition-colors" required /> -->
					</div>
					<p class="text-xs text-red-500" v-if="!$v.form.password.required && isSubmitted">{{ $t("form_validation.require.password") }}</p>
					<p class="text-xs text-red-500" v-if="!$v.form.password.minLength && isSubmitted">{{ $t("form_validation.min_length.password") }}</p>
					<p class="text-xs text-red-500" v-if="!$v.form.password.strongPass">{{ $t("form_validation.strong_password") }}</p>
				</div>

				<div>
					<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">{{ $t("user.create_page.form.confirm_password") }}<span class="text-red-600">*</span></label>
					<!-- <div>
							<input v-model="form.passwordConfirmation" type="password" class="w-full px-3 py-2 mb-1 bg-white border border-gray-300 rounded focus:outline-none focus:border-indigo-500 transition-colors" required />
						</div> -->
					<div class="relative">
						<div class="absolute z-10 top-2 right-2 cursor-pointer" @click="showPassword2">
							<svg v-if="typeInput2 == 'password' && form.passwordConfirmation" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
								<path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
								<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
							</svg>
							<svg v-else-if="typeInput2 != 'password' && form.passwordConfirmation" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
								<path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
							</svg>
						</div>
						<input v-model="form.passwordConfirmation" :type="typeInput2" class="w-full px-3 py-2 mb-1 bg-white border border-gray-300 rounded focus:outline-none focus:border-indigo-500 transition-colors" required />

						<!-- <input v-model="form.passwordConfirmation" :type="typeInput2" class="w-full px-3 py-2 mb-1 bg-gray-100 border border-gray-300 rounded focus:outline-none focus:border-indigo-500 transition-colors" required /> -->
					</div>
					<!-- <p class="text-xs text-red-500" v-if="!$v.form.passwordConfirmation.required && isSubmitted">{{$t('form_validation.require.confirm_password')}}</p> -->
					<p class="text-xs text-red-500" v-if="!$v.form.passwordConfirmation.sameAsPassword && isSubmitted">{{ $t("form_validation.same_as.confirm_password") }}</p>
				</div>
			</div>
		</div>
	</div>
</template>
<script>
	import { required, sameAs, minLength, email, requiredIf } from "vuelidate/lib/validators";
	export default {
		props: ["form", "isSubmitted"],
		name: "Userform",
		middleware: ["auth"],
		components: {},
		computed: {},
		data() {
			return {
				preview_list: [],
				preview_idCardFrontImage: null,
				preview_faceIdImage: null,
				dropdowns: {
					role: [],
					organization: [],
					userScopes: [],
					account_types: [
						{ value: 0, text: this.$t("openAccount.account_type.option.guest") },
						{ value: 1, text: this.$t("openAccount.account_type.option.juristic") },
						{ value: 2, text: this.$t("openAccount.account_type.option.government") },
					]
				},
				isData: false,
				url: null,
				url2: null,
				checkFarmbook: true,
				typeInput1: "password",
				typeInput2: "password",
			};
		},
		validations() {
			return {
				form: {
					firstname: { required, containsNotSpecial: (value) => !/[?!$^*]/.test(value), minLength: minLength(2) },
					lastname: { required, containsNotSpecial: (value) => !/[?!$^*]/.test(value), minLength: minLength(2) },
					password: {
						required,
						minLength: minLength(8),
						strongPass: (value) => /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]/.test(value),
					},
					passwordConfirmation: {
						sameAsPassword: sameAs("password"),
					},

					role: {
						selectDropdown: (role) => role !== -1,
					},
					account_type: {
						selectDropdown: (val) => val !== -1,
					},
					email: {
						required,
						email,
					},
					companyID: {
						required: requiredIf((form) => {
							return [1,2].includes(form.account_type)
						}),
					},
				},
			};
		},
		watch: {
			"form.account_type"(val) {
				this.form.companyID = null;
				this.$v.$touch();
			}
		},
		// watch: {
		// 	async "form.province"() {
		// 		this.form.district = null;
		// 		this.form.subDistrict = null;
		// 		await this.getDistrict();
		// 	},
		// 	async "form.district"() {
		// 		this.form.subDistrict = null;
		// 		await this.getSubDistrict();
		// 	},
		// 	isSubmitted(newValue) {
		// 		this.isSubmittedx = newValue;
		// 	},
		// },
		async mounted() {
			await this.getRole();
			await this.getOrganization();
			await this.getUserScopes();
		},
		methods: {
			showPassword1() {
				if (this.typeInput1 === "password") {
					this.typeInput1 = "text";
				} else {
					this.typeInput1 = "password";
				}
			},
			showPassword2() {
				if (this.typeInput2 === "password") {
					this.typeInput2 = "text";
				} else {
					this.typeInput2 = "password";
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
	.vs__clear {
		display: none !important;
	}
	.mx-input {
		border: none !important;
		box-shadow: none !important;
		height: 32px !important;
		background-color: transparent !important;
	}
	.mx-datepicker {
		width: 100% !important;
	}
	input::-ms-reveal,
	input::-ms-clear {
		display: none;
	}

	#user__form .v-select .vs__dropdown-toggle {
		-webkit-appearance: none;
		-moz-appearance: none;
		appearance: none;
		background: #fff;

		border: 1px solid rgba(60, 60, 60, 0.26) !important;

		border-radius: 4px !important;

		display: flex;
		align-items: center;
		padding: 6px 12px 6px 12px !important;
		white-space: normal;
	}
</style>
