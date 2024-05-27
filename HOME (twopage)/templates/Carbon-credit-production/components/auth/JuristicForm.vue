<template>
	<div class="w-full pt-4">
		<div class="">
			<p class="text-green-600 text-lg">{{ $t("openAccount.form.title") }}</p>
			<p class="text-sm">{{ $t("openAccount.form.juristic.subtitle") }}</p>
		</div>
		<div class="border-t my-4"></div>

		<div class="grid grid-cols-4 gap-4">
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.juristic.name')" :required="true" />
				<UITextInput v-model="form.juristic.juristic_name" />
				<UIErrorMsg v-if="!$v.form.juristic.juristic_name.required && isSubmitted">{{ $t("openAccount.validate.juristic.name") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.juristic.juristic_name.containsNotSpecial && isSubmitted">{{ $t("openAccount.validate.containsNotSpecial") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.juristic.juristic_name.minLength && isSubmitted">{{ $t("openAccount.validate.minLength2") }}</UIErrorMsg>
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.phone_number')" :required="true" />
				<UITextInput v-model="form.juristic.phone_number" @keyup="maskPhone"/>
				<UIErrorMsg v-if="!$v.form.juristic.phone_number.required && isSubmitted">{{ $t("openAccount.validate.phone_number") }}</UIErrorMsg>
			</div>
			<div class="col-span-4">
				<UILabel :text="$t('openAccount.form.juristic.address')" :required="true" />
				<UITextInput v-model="form.juristic.address" />
				<UIErrorMsg v-if="!$v.form.juristic.address.required && isSubmitted">{{ $t("openAccount.validate.juristic.office_address") }}</UIErrorMsg>
			</div>

			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.province')" :required="true" />
				<UIDropdown :option="dropdowns.provinces" v-model="form.juristic.province" />
				<UIErrorMsg v-if="!$v.form.juristic.province.required && isSubmitted">{{ $t("openAccount.validate.province") }}</UIErrorMsg>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.district')" :required="true" />
				<UIDropdown :option="dropdowns.district" v-model="form.juristic.district" />
				<UIErrorMsg v-if="!$v.form.juristic.district.required && isSubmitted">{{ $t("openAccount.validate.district") }}</UIErrorMsg>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.subdistrict')" :required="true" />
				<UIDropdown :option="dropdowns.subdistrict" v-model="form.juristic.subdistrict" />
				<UIErrorMsg v-if="!$v.form.juristic.subdistrict.required && isSubmitted">{{ $t("openAccount.validate.subdistrict") }}</UIErrorMsg>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.postcode')" :required="true" />
				<UITextInput v-model="form.juristic.postcode" />
				<UIErrorMsg v-if="!$v.form.juristic.postcode.required && isSubmitted">{{ $t("openAccount.validate.postcode") }}</UIErrorMsg>
			</div>

			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.juristic.number')" :required="false" />
				<UITextInput v-model="form.juristic.juristic_number" />
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.juristic.alien_id')" :required="false" />
				<UITextInput v-model="form.juristic.alien_number" />

				<UILabel class="text-gray-500" :text="$t('openAccount.form.juristic.alien_id_description')" :required="false" />
			</div>

			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.email')" :required="true" />
				<UITextInput v-model="form.juristic.email" />
				<UIErrorMsg v-if="!$v.form.juristic.email.required && isSubmitted">{{ $t("openAccount.validate.email") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.juristic.email.email && isSubmitted">{{ $t("openAccount.validate.emailValidate") }}</UIErrorMsg>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.password')" :required="true" />
				<UIPasswordInput v-model="form.juristic.password" />
				<UIErrorMsg v-if="!$v.form.juristic.password.required && isSubmitted">{{ $t("openAccount.validate.password") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.juristic.password.minLength && isSubmitted">{{ $t("openAccount.validate.minLength8") }}</UIErrorMsg>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.passwordConfirmation')" :required="true" />
				<UIPasswordInput v-model="form.juristic.passwordConfirmation" />
				<UIErrorMsg v-if="!$v.form.juristic.passwordConfirmation.sameAsPassword && isSubmitted">{{ $t("openAccount.validate.passwordConfirmation") }}</UIErrorMsg>
			</div>
			<div class="col-span-4"></div>
			<div class="col-span-4 border-t"></div>
			<div class="col-span-4"></div>

			<div class="col-span-4">
				<p class="text-base underline">{{ $t("openAccount.form.juristic.grantee_info.title") }}</p>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.firstname')" :required="true" />
				<UITextInput v-model="form.juristic.firstname" />
				<UIErrorMsg v-if="!$v.form.juristic.firstname.required && isSubmitted">{{ $t("openAccount.validate.firstname") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.juristic.firstname.containsNotSpecial && isSubmitted">{{ $t("openAccount.validate.containsNotSpecial") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.juristic.firstname.minLength && isSubmitted">{{ $t("openAccount.validate.minLength2") }}</UIErrorMsg>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.lastname')" :required="true" />
				<UITextInput v-model="form.juristic.lastname" />
				<UIErrorMsg v-if="!$v.form.juristic.lastname.required && isSubmitted">{{ $t("openAccount.validate.lastname") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.juristic.lastname.containsNotSpecial && isSubmitted">{{ $t("openAccount.validate.containsNotSpecial") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.juristic.lastname.minLength && isSubmitted">{{ $t("openAccount.validate.minLength2") }}</UIErrorMsg>
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.card_id')" :required="true" />
				<UITextInput v-model="form.juristic.card_id" />
				<UIErrorMsg v-if="!$v.form.juristic.card_id.required && isSubmitted">{{ $t("openAccount.validate.id_card") }}</UIErrorMsg>
			</div>

			<div class="col-span-4"></div>
			<div class="col-span-4 border-t"></div>
			<div class="col-span-4"></div>
			<div class="col-span-4">
				<p class="text-base underline">{{ $t("openAccount.form.juristic.account_detail.title") }}</p>
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.accountName')" :required="true" />
				<UITextInput v-model="form.juristic.accountName" />
				<UIErrorMsg v-if="!$v.form.juristic.accountName.required && isSubmitted">{{ $t("openAccount.validate.accountName") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.juristic.accountName.minLength && isSubmitted">{{ $t("openAccount.validate.minLength2") }}</UIErrorMsg>
			</div>

			<div class="col-span-2 space-y-3">
				<UILabel :text="$t('openAccount.form.request_permission.title')" :required="true" />
				<AuthRequestPermission :form="form.juristic" />
				<UIErrorMsg v-if="!$v.form.juristic.request_permission.morethan1 && isSubmitted">{{ $t("openAccount.validate.requestPermission") }}</UIErrorMsg>
			</div>

			<div class="col-span-4 my-4"></div>
			<div class="col-span-4 flex flex-col items-center text-sm gap-5">
				<button @click="next_step" class="w-80 bg-tgo-teal-500 border shadow-md rounded text-center py-2 text-white">{{ $t("button.next") }}</button>
				<button @click="$emit('cancel')" class="">{{ $t("button.cancel") }}</button>
			</div>
			<div class="col-span-4"></div>
		</div>
	</div>
</template>

<script>
import { required, sameAs, minLength, email } from "vuelidate/lib/validators";

export default {
	props: ["form"],
	data() {
		return {
			dropzoneOptions: {
				url: process.env.baseUrl + "/api/v1/form/upload",
				disablePreviews: true,
				previewsContainer: false,
				parallelUploads: 10,
				maxFiles: 10,
				acceptedFiles: "image/png,image/jpeg,application/pdf",
			},
			dropdowns: {
				provinces: [],
				district: [],
				subdistrict: [],
			},
			isSubmitted: false,
		};
	},
	watch: {
		"form.juristic.province"(value) {
			if (value) {
				this.getDistrict();
			}
		},
		"form.juristic.district"(value) {
			if (value) {
				this.getSubdistrict();
			}
		},
	},
	validations() {
		return {
			form: {
				juristic: {
					accountName: { required, minLength: minLength(2) },
					firstname: { required, containsNotSpecial: (value) => !/[?!$^*]/.test(value), minLength: minLength(2) },
					lastname: { required, containsNotSpecial: (value) => !/[?!$^*]/.test(value), minLength: minLength(2) },
					juristic_name: { required, containsNotSpecial: (value) => !/[?!$^*]/.test(value), minLength: minLength(2) },
					card_id: { required },
					password: {
						required,
						minLength: minLength(8),
					},
					passwordConfirmation: {
						sameAsPassword: sameAs("password"),
					},
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

					request_permission: {
						morethan1: () => this.form.juristic.request_permission.length > 0,
					},
				},
			},
		};
	},
	async mounted() {
		await this.getProvince();
	},
	methods: {
		maskPhone(value) {
			let phonenumber = value;

			if (value.length === 4) {
				phonenumber = value.slice(0, 3) + "-" + value.slice(3 + Math.abs(0));
			}
			if (value.length > 11) {
				phonenumber = value.slice(0, 11);
			}

			this.form.juristic.phone_number = phonenumber;
		},
		next_step() {
			this.isSubmitted = true;
			this.$v.$touch();
			if (this.$v.$invalid) {
				this.$swal.fire({
					icon: "error",
					iconColor: "#ef4444",
					confirmButtonColor: "#ef4444",
					title: this.$t("sweetalert.complete_information"),
					text: this.$t("sweetalert.complete_information_text"),
				});

				return 0;
			}
			this.$emit("click");
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
			this.form.juristic.district = "";
			this.form.juristic.subdistrict = "";
			this.dropdowns.district = await this.$axios
				.$get(`/api/v1/dropdown/district?province=${this.form.juristic.province}`)
				.then((resp) => resp)
				.catch((err) => {
					console.log(err);
				});
		},
		async getSubdistrict() {
			const app = this;
			this.form.juristic.subdistrict = "";
			this.dropdowns.subdistrict = await this.$axios
				.$get(`/api/v1/dropdown/subdistrict?province=${this.form.juristic.province}&district=${this.form.juristic.district}`)
				.then((resp) => resp)
				.catch((err) => {
					console.log(err);
				});
		},
	},
};
</script>

<style>
</style>