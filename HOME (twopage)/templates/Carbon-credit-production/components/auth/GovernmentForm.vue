<template>
	<div class="w-full pt-4">
		<div class="">
			<p class="text-green-600 text-lg">{{$t('openAccount.form.title')}}</p>
			<p class="text-sm">{{$t('openAccount.form.government.subtitle')}}</p>
		</div>
		<div class="border-t my-4"></div>

		<div class="grid grid-cols-4 gap-4">
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.government.name')" :required="true" />
				<UITextInput v-model="form.government.government_name" />
				<UIErrorMsg v-if="!$v.form.government.government_name.required && isSubmitted">{{ $t("openAccount.validate.government.name") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.government.government_name.containsNotSpecial && isSubmitted">{{ $t("openAccount.validate.containsNotSpecial") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.government.government_name.minLength && isSubmitted">{{ $t("openAccount.validate.minLength2") }}</UIErrorMsg>
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.phone_number')" :required="true" />
				<UITextInput v-model="form.government.phone_number" @keyup="maskPhone"/>
				<UIErrorMsg v-if="!$v.form.government.phone_number.required && isSubmitted">{{ $t("openAccount.validate.phone_number") }}</UIErrorMsg>

			</div>
			<div class="col-span-4">
				<UILabel :text="$t('openAccount.form.government.address')" :required="true" />
				<UITextInput v-model="form.government.address" />
				<UIErrorMsg v-if="!$v.form.government.address.required && isSubmitted">{{ $t("openAccount.validate.government.office_address") }}</UIErrorMsg>
			</div>

			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.province')" :required="true" />
				<UIDropdown v-model="form.government.province" :option="dropdowns.provinces"  />
				<UIErrorMsg v-if="!$v.form.government.province.required && isSubmitted">{{ $t("openAccount.validate.province") }}</UIErrorMsg>
			
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.district')" :required="true" />
				<UIDropdown v-model="form.government.district" :option="dropdowns.district" />
				<UIErrorMsg v-if="!$v.form.government.district.required && isSubmitted">{{ $t("openAccount.validate.district") }}</UIErrorMsg>

			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.subdistrict')" :required="true" />
				<UIDropdown v-model="form.government.subdistrict" :option="dropdowns.subdistrict"  />
				<UIErrorMsg v-if="!$v.form.government.subdistrict.required && isSubmitted">{{ $t("openAccount.validate.subdistrict") }}</UIErrorMsg>

			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.postcode')" :required="true" />
				<UITextInput v-model="form.government.postcode" />
				<UIErrorMsg v-if="!$v.form.government.postcode.required && isSubmitted">{{ $t("openAccount.validate.postcode") }}</UIErrorMsg>

			</div>

			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.email')" :required="true" />
				<UITextInput v-model="form.government.email" />
				<UIErrorMsg v-if="!$v.form.government.email.required && isSubmitted">{{ $t("openAccount.validate.email") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.government.email.email && isSubmitted">{{ $t("openAccount.validate.containsNotSpecial") }}</UIErrorMsg>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.password')" :required="true" />
				<UIPasswordInput v-model="form.government.password" />
				<UIErrorMsg v-if="!$v.form.government.password.required && isSubmitted">{{ $t("openAccount.validate.password") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.government.password.minLength && isSubmitted">{{ $t("openAccount.validate.minLength8") }}</UIErrorMsg>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.passwordConfirmation')" :required="true" />
				<UIPasswordInput v-model="form.government.passwordConfirmation" />
				<UIErrorMsg v-if="!$v.form.government.passwordConfirmation.sameAsPassword && isSubmitted">{{ $t("openAccount.validate.passwordConfirmation") }}</UIErrorMsg>
			</div>
			<div class="col-span-4"></div>
			<div class="col-span-4 border-t"></div>
			<div class="col-span-4"></div>

			<div class="col-span-4">
				<p class="text-base underline">{{ $t("openAccount.form.juristic.grantee_info.title") }}</p>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.firstname')" :required="true" />
				<UITextInput v-model="form.government.firstname" />
				<UIErrorMsg v-if="!$v.form.government.firstname.required && isSubmitted">{{ $t("openAccount.validate.firstname") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.government.firstname.containsNotSpecial && isSubmitted">{{ $t("openAccount.validate.containsNotSpecial") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.government.firstname.minLength && isSubmitted">{{ $t("openAccount.validate.minLength2") }}</UIErrorMsg>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.lastname')" :required="true" />
				<UITextInput v-model="form.government.lastname" />
				<UIErrorMsg v-if="!$v.form.government.lastname.required && isSubmitted">{{ $t("openAccount.validate.lastname") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.government.lastname.containsNotSpecial && isSubmitted">{{ $t("openAccount.validate.containsNotSpecial") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.government.lastname.minLength && isSubmitted">{{ $t("openAccount.validate.minLength2") }}</UIErrorMsg>
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.card_id')" :required="true"/>
				<UITextInput v-model="form.government.card_id" />
				<UIErrorMsg v-if="!$v.form.government.card_id.required && isSubmitted">{{ $t("openAccount.validate.id_card") }}</UIErrorMsg>
			</div>

			<div class="col-span-4"></div>
			<div class="col-span-4 border-t"></div>
			<div class="col-span-4"></div>
			<div class="col-span-4">
				<p class="text-base underline">{{ $t("openAccount.form.juristic.account_detail.title") }}</p>
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.accountName')" :required="true" />
				<UITextInput v-model="form.government.accountName" />
				<UIErrorMsg v-if="!$v.form.government.card_id.required && isSubmitted">{{ $t("openAccount.validate.accountName") }}</UIErrorMsg>
			</div>

			<div class="col-span-2 space-y-3">
				<UILabel :text="$t('openAccount.form.request_permission.title')" :required="true" />
				<AuthRequestPermission :form="form.government"/>
				<UIErrorMsg v-if="!$v.form.government.request_permission.morethan1 && isSubmitted">{{ $t("openAccount.validate.requestPermission") }}</UIErrorMsg>
			</div>

			<div class="col-span-4 my-4"></div>
			<div class="col-span-4 flex flex-col items-center text-sm gap-5">
				<button @click="next_step" class="w-80 bg-tgo-teal-500 border shadow-md rounded text-center py-2 text-white">{{ $t("button.next") }}</button>
				<button @click="$emit('cancel')">{{ $t("button.cancel") }}</button>
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
			idOption: "idcard",
			isSubmitted:false
		};
	},
	watch: {
		"form.government.province"(value) {
			if (value) {
				this.getDistrict();
			}
		},
		"form.government.district"(value) {
			if (value) {
				this.getSubdistrict();
			}
		},
	},
	validations() {
		return {
			form: {
				government: {
					accountName: { required, minLength: minLength(2) },
					firstname: { required, containsNotSpecial: (value) => !/[?!$^*]/.test(value), minLength: minLength(2) },
					lastname: { required, containsNotSpecial: (value) => !/[?!$^*]/.test(value), minLength: minLength(2) },

					government_name: { required, containsNotSpecial: (value) => !/[?!$^*]/.test(value), minLength: minLength(2) },

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
					request_permission: {
						morethan1: () => this.form.government.request_permission.length > 0,
					},
					card_id: { required },
					phone_number: { required },

					address: { required },
					province: { required },
					district: { required },
					subdistrict: { required },
					postcode: { required },
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

			this.form.government.phone_number = phonenumber;
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
			this.$emit('click')
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
			this.form.government.district = "";
			this.form.government.subdistrict = "";
			this.dropdowns.district = await this.$axios
				.$get(`/api/v1/dropdown/district?province=${this.form.government.province}`)
				.then((resp) => resp)
				.catch((err) => {
					console.log(err);
				});
		},
		async getSubdistrict() {
			const app = this;
			this.form.government.subdistrict = "";
			this.dropdowns.subdistrict = await this.$axios
				.$get(`/api/v1/dropdown/subdistrict?province=${this.form.government.province}&district=${this.form.government.district}`)
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