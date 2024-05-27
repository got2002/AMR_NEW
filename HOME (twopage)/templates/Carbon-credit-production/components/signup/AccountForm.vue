<template>
	<div class="w-full mx-auto rounded-lg bg-white border border-gray-200 text-gray-800 font-light mb-6 mt-6">
		<div class="w-full p-3">
			<form>
				<!-- Firstname, Middlename, Lastname -->
				<div class="mb-3">
					<div class="grid grid-cols-1 md:grid-cols-2 gap-2">
						<div>
							<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">{{ $t("form.signup.label.firstname") }} <span class="text-red-600">*</span></label>
							<div>
								<input v-model="formx.firstname" class="w-full px-3 py-2 mb-1 border border-gray-200 rounded-md focus:outline-none focus:border-indigo-500 transition-colors" type="text" maxlength="255" required />
								<span v-if="!$v.formx.firstname.required && isSubmitted" class="text-red-500 text-sm">{{ $t("form.signup.validate.required") }}</span>
								<span v-else-if="!$v.formx.firstname.containsNotSpecial && isSubmittedx" class="text-red-500 text-sm">{{ $t("form.signup.validate.firstname_title") }}</span>
							</div>
						</div>
						<div>
							<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">{{ $t("form.signup.label.lastname") }} <span class="text-red-600">*</span></label>
							<div>
								<input v-model="formx.lastname" class="w-full px-3 py-2 mb-1 border border-gray-200 rounded-md focus:outline-none focus:border-indigo-500 transition-colors" type="text" maxlength="255" required />
								<span v-if="!$v.formx.lastname.required && isSubmitted" class="text-red-500 text-sm">{{ $t("form.signup.validate.required") }}</span>
								<span v-else-if="!$v.formx.lastname.containsNotSpecial && isSubmittedx" class="text-red-500 text-sm">{{ $t("form.signup.validate.firstname_title") }}</span>
							</div>
						</div>
					</div>
				</div>

				<!-- Email, Phone -->
				<div class="mb-3 border-b pb-4 border-dashed">
					<div class="grid grid-cols-1 md:grid-cols-2 gap-2">
						<div>
							<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">{{ $t("form.signup.label.email") }} <span class="text-red-600">*</span></label>
							<div>
								<input v-model="formx.email" class="w-full px-3 py-2 mb-1 border border-gray-200 rounded-md focus:outline-none focus:border-indigo-500 transition-colors" type="email" maxlength="255" required />
								<span v-if="!$v.formx.email.required && isSubmitted" class="text-red-500 text-sm">{{ $t("form.signup.validate.required") }}</span>
								<span v-else-if="!$v.formx.email.email && isSubmittedx" class="text-red-500 text-sm">{{ $t("form.signup.validate.email_title") }}</span>
							</div>
						</div>
						<div>
							<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">{{ $t("form.signup.label.phone") }} <span class="text-red-600">*</span></label>
							<div>
								<input v-model="formx.phoneNumber" class="w-full px-3 py-2 mb-1 border border-gray-200 rounded-md focus:outline-none focus:border-indigo-500 transition-colors" type="text" maxlength="20" oninput="this.value = this.value.replace(/[^0-9+]/g, '').replace(/(\..*)\./g, '$1');" required />
								<span v-if="!$v.formx.phoneNumber.required && isSubmitted" class="text-red-500 text-sm">{{ $t("form.signup.validate.required") }}</span>
								<span v-else-if="!$v.formx.phoneNumber.phone && isSubmittedx" class="text-red-500 text-sm">{{ $t("form.signup.validate.phoneNumber_title") }}</span>
							</div>
						</div>
					</div>
					<div class="mb-3">
						<div class="grid grid-cols-1 md:grid-cols-2 gap-2">
							<div>
								<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">เลขบัตรประชาชน<span class="text-red-600">*</span></label>
								<div>
									<input v-model="formx.idCardNumber" class="w-full px-3 py-2 mb-1 border border-gray-200 rounded-md focus:outline-none focus:border-indigo-500 transition-colors" type="text" maxlength="255" required />
									<span v-if="!$v.formx.idCardNumber.required && isSubmitted" class="text-red-500 text-sm">{{ $t("form.signup.validate.required") }}</span>
									<!-- <span v-else-if="!$v.formx.idCardNumber.citizen && isSubmittedx" class="text-red-500 text-sm">เลขบัตรประชาชนไม่ถูกต้อง</span> -->
								</div>
							</div>
							<div>
								<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">วันหมดอายุบัตร<span class="text-red-500 text-sm">ตลอดชีพไม่ต้องกรอก</span></label>
								<div>
									<div>
										<date-picker value-type="format" format="YYYY-MM-DD" v-model="formx.idCardExpiredDate" class="w-full px-3 py-1 mb-1 border border-gray-200 rounded-md focus:outline-none focus:border-indigo-500 transition-colors"></date-picker>
										<span v-if="!$v.formx.idCardExpiredDate.required && isSubmitted" class="text-red-500 text-sm">{{ $t("form.signup.validate.required") }}</span>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>

				<!-- Email, Phone -->
				<div class="mb-3">
					<div class="grid grid-cols-1 md:grid-cols-2 gap-2">
						<div>
							<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">{{ $t("form.signup.label.password") }} <span class="text-red-600">*</span></label>
							<div>
								<input v-model="formx.password" class="w-full px-3 py-2 mb-1 border border-gray-200 rounded-md focus:outline-none focus:border-indigo-500 transition-colors" type="password" maxlength="255" />
								<span v-if="!$v.formx.password.required && isSubmitted" class="text-red-500 text-sm">{{ $t("form.signup.validate.required") }}</span>
								<span v-else-if="(!$v.formx.password.containsUppercase || !$v.formx.password.containsLowercase || !$v.formx.password.containsNumber || !$v.formx.password.containsSpecial) && isSubmittedx" class="text-red-500 text-sm">{{ $t("form.signup.validate.password_title") }}</span>
							</div>
						</div>
						<div>
							<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">{{ $t("form.signup.label.passwordConfirmation") }}</label>
							<div>
								<!-- <input
                  v-model="formx.passwordConfirmation"
                  class="w-full px-3 py-2 mb-1 border border-gray-200 rounded-md focus:outline-none focus:border-indigo-500 transition-colors"
                  type="text"
                  maxlength="255"
                /> -->
								<input v-model="formx.passwordConfirmation" type="password" minlength="8" maxlength="255" class="w-full px-3 py-2 mb-1 border border-gray-200 rounded-md focus:outline-none focus:border-indigo-500 transition-colors" />
								<span v-if="!$v.formx.passwordConfirmation.sameAsPassword && isSubmittedx" class="text-red-500 text-sm">{{ $t("form.signup.validate.password_Confirm_title") }}</span>
							</div>
						</div>
					</div>
				</div>
			</form>
		</div>
	</div>
</template>

<script>
import { required, email, minLength, sameAs } from "vuelidate/lib/validators";
export default {
	props: {
		isSubmitted: {
			type: Boolean,
			required: true,
		},
		form: {
			type: Object,
			required: true,
		},
	},
	data() {
		return {
			formx: this.form,
			isSubmittedx: this.isSubmitted,
		};
	},
	watch: {
		isSubmitted(newValue) {
			this.isSubmittedx = newValue;
			// console.log(this.isSubmittedx)
		},
	},
	validations() {
		// let phone = (value) => /^(06|08|09)+\d{8}$/.test(value)
		return {
			formx: {
				firstname: {
					required,
					containsNotSpecial: (value) => !/[?!$^*]/.test(value),
				},
				lastname: {
					required,
					containsNotSpecial: (value) => !/[?!$^*]/.test(value),
				},
				email: { required, email },
				password: {
					required,
					minLength: minLength(8), // I assume you'd want something like this too
					containsUppercase: (value) => /[A-Z]/.test(value),
					containsLowercase: (value) => /[a-z]/.test(value),
					containsNumber: (value) => /[0-9]/.test(value),
					containsSpecial: (value) => /[#?!@$%^&*+-]/.test(value),
				},
				passwordConfirmation: {
					sameAsPassword: sameAs("password"),
				},
				phoneNumber: {
					required,
					phone: (value) => /^(06|08|09)+\d{8}$/.test(value),
				},
				idCardNumber: {
					required,
					citizen: this.checkcitizen,
				},
				idCardExpiredDate: {
					required,
				},
			},
		};
	},
	method: {
		checkcitizen() {
      console.log(this.formx.idCardNumber)
			const words = this.formx.idCardNumber.split("");
			let idx = 0;
			let sum = 0;
			let checkDigit = 0;
			for (let i = 13; i > 1; i--) {
				sum += parseInt(words[idx]) * i;
				idx++;
			}
			sum = (sum % 11) % 10;
			checkDigit = (11 - sum) % 10;
			if (checkDigit !== parseInt(words[words.length - 1])) {
				return false;
			} else {
				return true;
			}
		},
	},
  mounted(){
    
  }
};
</script>
