<template>
	<div class="w-full mx-auto rounded-lg bg-white border border-gray-200 text-gray-800 font-light mb-6 mt-6">
		<div class="w-full p-3">
			<form>
				<!-- Email, Phone -->
				<div class="mb-3 border-b pb-4 border-dashed">
					<div class="grid grid-cols-1">
						<div>
							<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">เบอร์โทรศัพท์ <span class="text-red-600">*</span></label>
							<div>
								<input v-model="formx.phoneNumber" class="w-full px-3 py-2 mb-1 border border-gray-200 rounded-md focus:outline-none focus:border-indigo-500 transition-colors" type="email" maxlength="255" required />
								<span v-if="!$v.formx.phoneNumber.required && isSubmitted" class="text-red-500 text-sm">{{ $t("form.signup.validate.required") }}</span>
							</div>
						</div>
					</div>
				</div>
			</form>
		</div>
	</div>
</template>

<script>
import { required } from "vuelidate/lib/validators";
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
		return {
			formx: {
				phoneNumber: { required },
			},
		};
	},
};
</script>