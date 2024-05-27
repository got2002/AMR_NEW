<template>
	<div class="w-full mx-auto rounded-lg bg-white border border-gray-200 text-gray-800 font-light mb-6 mt-6">
		<div class="w-full p-3">
			<!-- Email, Phone -->
			<div class="mb-3">
				<div class="grid grid-cols-1 md:grid-cols-2 gap-2">
					<div>
						<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">{{ $t("form.signup.label.password") }} <span class="text-red-600">*</span></label>
						<div>
							<input v-model="formx.password" class="w-full px-3 py-2 mb-1 border border-gray-200 rounded-md focus:outline-none focus:border-indigo-500 transition-colors" type="password" maxlength="255" />
							<span v-if="!$v.formx.password.required && isSubmitted" class="text-red-500 text-sm">{{ $t("form.signup.validate.required") }}</span>
						</div>
					</div>
					<div>
						<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">{{ $t("form.signup.label.passwordConfirmation") }}</label>
						<div>
							<input v-model="formx.passwordConfirmation" type="password" minlength="8" maxlength="255" class="w-full px-3 py-2 mb-1 border border-gray-200 rounded-md focus:outline-none focus:border-indigo-500 transition-colors" />
							<span v-if="!$v.formx.passwordConfirmation.sameAsPassword && isSubmitted" class="text-red-500 text-sm">{{ $t("form.signup.validate.password_Confirm_title") }}</span>
						</div>
					</div>
				</div>
				<div class="flex justify-end gap-2 mt-2">
					<button class="inline-flex bg-caat-600 border border-gray-300 text-white hover:bg-caat-700 hover:text-gray-700 rounded-lg leading-tight py-2 px-4" @click="submitForm3()">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
						</svg>
						{{ $t("button.submit") }}
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { required, sameAs } from "vuelidate/lib/validators";
export default {
	props: {
		form: {
			type: Object,
			required: true,
		},
	},
	data() {
		return {
			formx: this.form,
			isSubmitted: false,
		};
	},
	validations() {
		return {
			formx: {
				password: {
					required,
				},
				passwordConfirmation: {
					sameAsPassword: sameAs("password"),
				},
			},
		};
	},
	methods: {
		submitForm3() {
			this.isSubmitted = true;
			// this.updateComponentData();
			this.$v.$touch();
			console.log(this.$v.$invalid);
			if (this.$v.$invalid) {
				return;
			}
			this.$axios
				.$post("/api/v1/auth/set-new-password", this.formx)
				.then((resp) => {
					this.$toast.success(this.$t("text.PasswordChangeSuccessfully"));
					setTimeout(this.$toast.clear, 3000);
					// this.$router.push("/auth/signin");
					this.$router.push(this.localePath({ name: "auth-signin" }));
				})
				.catch((error) => {
					console.log(error);
					if (error.response) {
						console.log(error.response);
						this.errors = error.response.data.errors;
						this.$toast.error(`${this.$t("text.somethingWentWrong")}`);
						setTimeout(this.$toast.clear, 3000);
					}
				});
		},
	},
};
</script>
