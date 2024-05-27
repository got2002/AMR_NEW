<template>
	<div class="w-full pt-4">
		<!-- <div class="">
			<p class="text-green-600 text-lg">{{ $t("openAccount.form.title") }}</p>
			<p class="text-sm">{{ $t("openAccount.form.subtitle") }}</p>
			
		</div>
		<div class="border-t my-4"></div> -->

		<div class="grid grid-cols-4 gap-4">
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.account_type.title')" :required="true" />
				<UIDropdown v-model.number="form.account_type" :option="dropdowns.account_types" />
				<UIErrorMsg v-if="!$v.form.account_type.required && isSubmitted">{{ $t("openAccount.validate.account_type") }}</UIErrorMsg>
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('user.table.header.role')" :required="true" />
				<UIDropdown v-model.number="form.role" :option="dropdowns.roles" />
				<UIErrorMsg v-if="!$v.form.role.required && isSubmitted">{{ $t("openAccount.validate.role") }}</UIErrorMsg>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.firstname')" :required="true" />
				<UITextInput v-model="form.firstname" />
				<UIErrorMsg v-if="!$v.form.firstname.required && isSubmitted">{{ $t("openAccount.validate.firstname") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.firstname.containsNotSpecial && isSubmitted">{{ $t("openAccount.validate.containsNotSpecial") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.firstname.minLength && isSubmitted">{{ $t("openAccount.validate.minLength2") }}</UIErrorMsg>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.lastname')" :required="true" />
				<UITextInput v-model="form.lastname" />
				<UIErrorMsg v-if="!$v.form.lastname.required && isSubmitted">{{ $t("openAccount.validate.lastname") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.lastname.containsNotSpecial && isSubmitted">{{ $t("openAccount.validate.containsNotSpecial") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.lastname.minLength && isSubmitted">{{ $t("openAccount.validate.minLength2") }}</UIErrorMsg>
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.card_id')" :required="true" />

				<UITextInput v-model="form.card_id" />
				<UIErrorMsg v-if="!$v.form.card_id.required && isSubmitted">{{ $t("openAccount.validate.id_card") }}</UIErrorMsg>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.issued_by')" :required="false" />
				<UITextInput v-model="form.issued_by" />
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.phone_number')" :required="true" />
				<UITextInput v-model="form.phone_number" />
				<UIErrorMsg v-if="!$v.form.email.required && isSubmitted">{{ $t("openAccount.validate.phone_number") }}</UIErrorMsg>
			</div>

			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.address')" :required="true" />
				<UITextInput v-model="form.address" />
				<UIErrorMsg v-if="!$v.form.address.required && isSubmitted">{{ $t("openAccount.validate.address") }}</UIErrorMsg>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.province')" :required="true" />
				<UIDropdown :option="dropdowns.provinces" v-model="form.province" />
				<UIErrorMsg v-if="!$v.form.province.required && isSubmitted">{{ $t("openAccount.validate.province") }}</UIErrorMsg>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.district')" :required="true" />
				<UIDropdown :option="dropdowns.district" v-model="form.district" />
				<UIErrorMsg v-if="!$v.form.district.required && isSubmitted">{{ $t("openAccount.validate.district") }}</UIErrorMsg>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.subdistrict')" :required="true" />
				<UIDropdown :option="dropdowns.subdistrict" v-model="form.subdistrict" />
				<UIErrorMsg v-if="!$v.form.subdistrict.required && isSubmitted">{{ $t("openAccount.validate.subdistrict") }}</UIErrorMsg>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.postcode')" :required="true" />
				<UITextInput v-model="form.postcode" />
				<UIErrorMsg v-if="!$v.form.postcode.required && isSubmitted">{{ $t("openAccount.validate.postcode") }}</UIErrorMsg>
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.email')" :required="true" />
				<UITextInput v-model="form.email" />
				<UIErrorMsg v-if="!$v.form.email.required && isSubmitted">{{ $t("openAccount.validate.email") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.email.email && isSubmitted">{{ $t("openAccount.validate.emailValidate") }}</UIErrorMsg>
			</div>
			<div class="col-span-4">
				<UILabel :text="$t('openAccount.form.document.card_id')" :required="true"></UILabel>
				<UIFileUpload id="guest-upload" @upload="uploadImage" :filename="form.document?.name"></UIFileUpload>
				<UIErrorMsg v-if="!$v.form.document.required && isSubmitted">{{ $t("openAccount.validate.document") }}</UIErrorMsg>
			</div>
			
			<div class="col-span-4"></div>
			
		</div>
	</div>
</template>

<script>
import { required, sameAs, minLength, email } from "vuelidate/lib/validators";
import UploadImage from "../../static/mixins/upload-image";
export default {
	props: ["form",'isSubmitted'],
	mixins: [UploadImage],
	data() {
		return {
			dropdowns: {
				roles: [
					{  value: 0, text: this.$t("user.role.user") },
					{  value: 1, text: this.$t("user.role.registrar") },
					{ value: 99, text: this.$t("user.role.admin") },
				],
				provinces: [],
				district: [],
				subdistrict: [],
				account_types: [
					{text: this.$t("openAccount.account_type.option.guest"), value: 0},
					{text: this.$t("openAccount.account_type.option.juristic"), value: 1},
					{text: this.$t("openAccount.account_type.option.government"), value: 2},
				]
			},
			pdfModal: false,
			pdfURL: "",
		};
	},
	watch: {
		"form.province"(value) {
			if (value) {
				this.getDistrict();
			}
		},
		"form.district"(value) {
			if (value) {
				this.getSubdistrict();
			}
		},
	},
	validations() {
		return {
			form: {
				account_type: { required },
				role: { required },
				// accountName: { required, containsNotSpecial: (value) => !/[?!$^*]/.test(value), minLength: minLength(2) },
				firstname: { required, containsNotSpecial: (value) => !/[?!$^*]/.test(value), minLength: minLength(2) },
				lastname: { required, containsNotSpecial: (value) => !/[?!$^*]/.test(value), minLength: minLength(2) },
				card_id: { required },
				
				email: {
					required,
					email,
				},

				phone_number: { required },

				address: { required },
				province: { required },
				district: { required },
				subdistrict: { required },
				postcode: { required },
				document: { required },

				// request_permission: {
				// 	morethan1: () => this.form.request_permission.length > 0,
				// },
			},
		};
	},
	async mounted() {
		await this.getProvince();
		await this.getDistrict();
		await this.getSubdistrict();
		this.form.companyID = null;
		// await this.getUserScopes()
	},
	methods: {
		scopeValue(value) {
			const scope = this._.find(this.dropdowns.userScopes, (item) => item.value === value);
			// console.log(scope);
			return scope?.text;
		},
		openPDF(src) {
			// console.log(this.document);
			this.pdfURL = process.env.baseUrl + src;
			this.pdfModal = true;
		},
		async getProvince() {
			const app = this;
			this.dropdowns.provinces = await this.$axios
				.$get(`/api/v1/dropdown/provinces`)
				.then((resp) => resp)
				.catch((err) => {
					console.log(err);
				});
		},
		async getDistrict() {
			const app = this;
			// console.log("province");

			this.dropdowns.district = await this.$axios
				.$get(`/api/v1/dropdown/district?province=${this.form.province}`)
				.then((resp) => resp)
				.catch((err) => {
					console.log(err);
				});
		},
		async getSubdistrict() {
			const app = this;

			this.dropdowns.subdistrict = await this.$axios
				.$get(`/api/v1/dropdown/subdistrict?province=${this.form.province}&district=${this.form.district}`)
				.then((resp) => resp)
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
		validateForm() {
			// this.isSubmitted = true;
			this.$v.$touch();
			return this.$v.$invalid;
		},
		async uploadImage(input) {
			// console.log(input.target.files[0]);
			if (input.target.files[0]) {
				const formData = new FormData();
				const fileItem = input.target.files[0];
				// console.log(fileItem);
				formData.append("file", fileItem);
				const resp = await this.uploadImages(formData);
				// console.log(resp);
				this.form.document = resp;
			}
		},
	},
};
</script>

<style>
</style>