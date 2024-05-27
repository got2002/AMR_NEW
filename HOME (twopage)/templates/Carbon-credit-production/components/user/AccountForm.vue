<template>
	<div class="flex flex-col h-full">
		<div class="mb-3">
			<div class="bg-white border-b pb-2">
				<h2 class="font-semibold">{{ $t("account.create_page.form.title") }}</h2>
			</div>
			<div id="account__form" class="grid grid-cols-1 gap-2 mt-3">
				<div>
					<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">{{ $t("account.create_page.form.name") }}<span class="text-red-600">*</span></label>
					<div>
						<input v-model="form.accountName" class="w-full px-3 py-2 mb-1 bg-white border border-gray-300 rounded outline-none focus:border-indigo-500 transition-colors " required />
					</div>
					<p class="text-xs text-red-500" v-if="!$v.form.accountName.required && isSubmitted">{{ $t("form_validation.require.Accountname") }}</p>
					<p class="text-xs text-red-500" v-if="!$v.form.accountName.containsNotSpecial && isSubmitted">{{ $t("form_validation.pattern.Accountname") }}</p>
					<p class="text-xs text-red-500" v-if="!$v.form.accountName.minLength && isSubmitted">{{ $t("form_validation.min_length.Accountname") }}</p>
				</div>
				
				<div>
					<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">{{ $t("account.create_page.form.accountTypes") }}<span class="text-red-600">*</span></label>
					<!-- <div>
						
						<v-select :options="dropdowns.transaction_types" :reduce="(text) => text.value" label="text" v-model="form.accountTypeID" />
					</div> -->
					<div class="border border-gray-300 rounded">
						<UIDropdownSearch v-model="form.accountTypeID" :options="dropdowns.transaction_types" valueAttr="value" textAttr="text" :searchable="false"/>
					</div>
					<p class="text-xs text-red-500" v-if="!$v.form.accountTypeID.selectDropdown && isSubmitted">{{ $t("form_validation.require.accountTypes") }}</p>
				</div>
			</div>
		</div>
	</div>
</template>
<script>
	import { required, sameAs, minLength, email } from "vuelidate/lib/validators";
	export default {
		props: ["form", "isSubmitted"],
		name: "Accountform",
		middleware: ["auth"],
		components: {},
		computed: {},
		data() {
			return {
				preview_list: [],
				preview_idCardFrontImage: null,
				preview_faceIdImage: null,
				dropdowns: {
					email: [],
					account_types: [],
					userScopes: [],
					transaction_types: [],
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
					accountName: { required, containsNotSpecial: (value) => !/[?!$^*]/.test(value), minLength: minLength(2) },
					accountTypeID: {
						selectDropdown: (accountTypeID) => accountTypeID !== null,
					},
					transactionTypeID: {
						selectDropdown: (transactionTypeID) => transactionTypeID !== null,
					},
					userEmail: {
						selectDropdown: (userEmail) => userEmail !== null,
					},
				},
			};
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
			await this.getAccountTypes();
			await this.getTransactionTypes();
			// await this.getEmail();
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
			async getAccountTypes() {
				const app = this;

				await this.$axios
					.$get(`/api/v1/dropdown/account-types`)
					.then((resp) => {
						// console.log(resp);
						app.dropdowns.account_types = resp;
					})
					.catch((err) => {
						console.log(err);
					});
			},
			async getTransactionTypes() {
				this.dropdowns.transaction_types = await this.$axios
					.$get(`/api/v1/dropdown/account-transaction-types`)
					.then((resp) => resp)
					.catch((err) => {
						console.log(err);
					});
			},
			async getEmail() {
				const app = this;

				await this.$axios
					.$get(`/api/v1/dropdown/email`)
					.then((resp) => {
						// console.log(resp);
						app.dropdowns.email = resp;
					})
					.catch((err) => {
						console.log(err);
					});
			},
		},
	};
</script>

<style scoped>
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
	#account__form .vs__dropdown-toggle {
		-webkit-appearance: none;
		-moz-appearance: none;
		appearance: none;
		background: #fff;
	
		border: 1px solid rgba(60, 60, 60, 0.26) !important;
	
		border-radius: 4px !important;
		
		display: flex;
		align-items: center;
		padding: 6px 4px 6px 4px !important;
		white-space: normal;
	}
</style>
