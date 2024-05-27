<template>
	<div class="w-full pt-4">
		<div class="">
			<p class="text-green-600 text-lg">{{ $t("openAccount.form.title") }}</p>
			<p class="text-sm">{{ $t("openAccount.form.guest.subtitle") }}</p>
		</div>
		<div class="border-t my-4"></div>

		<div class="grid grid-cols-4 gap-4">
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.firstname')" :required="true" />
				<UITextInput v-model="form.guest.firstname" />
				<UIErrorMsg v-if="!$v.form.guest.firstname.required && isSubmitted">{{ $t("openAccount.validate.firstname") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.guest.firstname.containsNotSpecial && isSubmitted">{{ $t("openAccount.validate.containsNotSpecial") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.guest.firstname.minLength && isSubmitted">{{ $t("openAccount.validate.minLength2") }}</UIErrorMsg>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.lastname')" :required="true" />
				<UITextInput v-model="form.guest.lastname" />
				<UIErrorMsg v-if="!$v.form.guest.lastname.required && isSubmitted">{{ $t("openAccount.validate.lastname") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.guest.lastname.containsNotSpecial && isSubmitted">{{ $t("openAccount.validate.containsNotSpecial") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.guest.lastname.minLength && isSubmitted">{{ $t("openAccount.validate.minLength2") }}</UIErrorMsg>
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.card_id')" :required="true" />

				<UITextInput v-model="form.guest.card_id" />
				<UIErrorMsg v-if="!$v.form.guest.card_id.required && isSubmitted">{{ $t("openAccount.validate.id_card") }}</UIErrorMsg>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.issued_by')" :required="false" />
				<UITextInput v-model="form.guest.issued_by" />
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.phone_number')" :required="true" />
				<UITextInput v-model="form.guest.phone_number" @keyup="maskPhone" />
				<UIErrorMsg v-if="!$v.form.guest.email.required && isSubmitted">{{ $t("openAccount.validate.phone_number") }}</UIErrorMsg>
			</div>

			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.address')" :required="true" />
				<UITextInput v-model="form.guest.address" />
				<UIErrorMsg v-if="!$v.form.guest.address.required && isSubmitted">{{ $t("openAccount.validate.address") }}</UIErrorMsg>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.province')" :required="true" />
				<UIDropdown :option="dropdowns.provinces" v-model="form.guest.province" />
				<UIErrorMsg v-if="!$v.form.guest.province.required && isSubmitted">{{ $t("openAccount.validate.province") }}</UIErrorMsg>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.district')" :required="true" />
				<UIDropdown :option="dropdowns.district" v-model="form.guest.district" />
				<UIErrorMsg v-if="!$v.form.guest.district.required && isSubmitted">{{ $t("openAccount.validate.district") }}</UIErrorMsg>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.subdistrict')" :required="true" />
				<UIDropdown :option="dropdowns.subdistrict" v-model="form.guest.subdistrict" />
				<UIErrorMsg v-if="!$v.form.guest.subdistrict.required && isSubmitted">{{ $t("openAccount.validate.subdistrict") }}</UIErrorMsg>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.postcode')" :required="true" />
				<UITextInput v-model="form.guest.postcode" />
				<UIErrorMsg v-if="!$v.form.guest.postcode.required && isSubmitted">{{ $t("openAccount.validate.postcode") }}</UIErrorMsg>
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.email')" :required="true" />
				<UITextInput v-model="form.guest.email" />
				<UIErrorMsg v-if="!$v.form.guest.email.required && isSubmitted">{{ $t("openAccount.validate.email") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.guest.email.email && isSubmitted">{{ $t("openAccount.validate.emailValidate") }}</UIErrorMsg>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.password')" :required="true" />
				<UIPasswordInput v-model="form.guest.password" />
				<UIErrorMsg v-if="!$v.form.guest.password.required && isSubmitted">{{ $t("openAccount.validate.password") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.guest.password.minLength && isSubmitted">{{ $t("openAccount.validate.minLength8") }}</UIErrorMsg>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.passwordConfirmation')" :required="true" />
				<UIPasswordInput v-model="form.guest.passwordConfirmation" />

				<UIErrorMsg v-if="!$v.form.guest.passwordConfirmation.sameAsPassword && isSubmitted">{{ $t("openAccount.validate.passwordConfirmation") }}</UIErrorMsg>
			</div>
			<div class="col-span-4"></div>
			<div class="col-span-4 border-t"></div>
			<div class="col-span-4"></div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.accountName')" :required="true" />
				<UITextInput v-model="form.guest.accountName" />
				<UIErrorMsg v-if="!$v.form.guest.accountName.required && isSubmitted">{{ $t("openAccount.validate.accountName") }}</UIErrorMsg>
				<!-- <UIErrorMsg v-if="!$v.form.guest.accountName.containsNotSpecial && isSubmitted">{{ $t("openAccount.validate.containsNotSpecial") }}</UIErrorMsg> -->
				<UIErrorMsg v-if="!$v.form.guest.accountName.minLength && isSubmitted">{{ $t("openAccount.validate.minLength2") }}</UIErrorMsg>
			</div>

			<div class="col-span-2 space-y-3">
				<UILabel :text="$t('openAccount.form.request_permission.title')" :required="true" />
				<AuthRequestPermission :form="form.guest" />

				<UIErrorMsg v-if="!$v.form.guest.request_permission.morethan1 && isSubmitted">{{ $t("openAccount.validate.requestPermission") }}</UIErrorMsg>
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
			dropdowns: {
				provinces: [],
				district: [],
				subdistrict: [],
			},
			idOption: "idcard",
			isSubmitted: false,
		};
	},
	watch: {
		"form.guest.province"(value) {
			console.log(value);
			if (value) {
				this.getDistrict();
			}
		},
		"form.guest.district"(value) {
			if (value) {
				this.getSubdistrict();
			}
		},
	},
	validations() {
		return {
			form: {
				guest: {
					accountName: { required, minLength: minLength(2) },
					firstname: { required, containsNotSpecial: (value) => !/[?!$^*]/.test(value), minLength: minLength(2) },
					lastname: { required, containsNotSpecial: (value) => !/[?!$^*]/.test(value), minLength: minLength(2) },
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
						morethan1: () => this.form.guest.request_permission.length > 0,
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

			this.form.guest.phone_number = phonenumber;
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
			this.form.guest.district = "";
			this.form.guest.subdistrict = "";
			this.dropdowns.district = await this.$axios
				.$get(`/api/v1/dropdown/district?province=${this.form.guest.province}`)
				.then((resp) => resp)
				.catch((err) => {
					console.log(err);
				});
		},
		async getSubdistrict() {
			const app = this;
			this.form.guest.subdistrict = "";
			this.dropdowns.subdistrict = await this.$axios
				.$get(`/api/v1/dropdown/subdistrict?province=${this.form.guest.province}&district=${this.form.guest.district}`)
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