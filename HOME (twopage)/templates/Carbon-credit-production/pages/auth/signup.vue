<template>
	<div class="max-w-7xl mx-auto px-4 sm:px-6">
		<h1 class="text-2xl tracking-tight font-extrabold text-gray-900 sm:text-2xl md:text-4xl">
			<span class="inline">{{ $t("form.signup.title.register_form") }}</span>
		</h1>

		<!-- <div class="mt-2 space-y-2">
			<div class="block bg-gray-200 h-5 w-full"></div>
			<div class="block bg-gray-200 h-5 w-1/2"></div>
		</div> -->

		<p v-show="false" class="mt-3 text-base text-gray-500 sm:mt-5 sm:text-md sm:max-w-xl md:mt-5 md:text-md lg:mx-0">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque quis magna mattis, hendrerit tortor ut, ullamcorper eros.</p>

		<div>
			<!-- Signup Form -->
			<SignupAccountForm :form="form" :isSubmitted="isSubmitted" />

			<!-- <div v-if="errors !== null" class="p-3 w-full mx-auto rounded-lg bg-white border border-red-400 text-gray-800 font-light mb-6 mt-6">
				<ul>
					<li v-for="(error, key) in errors" :key="key" class="text-red-400">- {{ error[0] }}</li>
				</ul>
			</div> -->

			<div class="flex justify-end gap-2">
				<button type="submit" class="inline-flex bg-caat-600 border border-gray-300 text-white hover:bg-caat-700 hover:text-gray-700 rounded-lg leading-tight py-2 px-4" @click="submitForm()">
					<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
						<path stroke-linecap="round" stroke-linejoin="round" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
					</svg>
					{{ $t("button.submit") }}
				</button>
			</div>
		</div>
	</div>
</template>

<script>
import { required, email, minLength, sameAs } from "vuelidate/lib/validators";
export default {
	name: "SignUpPage",
	layout: "AuthLayout",
	middleware: "guest",
	data() {
		return {
			isSubmitted: false,
			steps: 1,
			form: {
				email: "",
				password: "",
				firstname: "",
				lastname: "",
				phoneNumber: "",
				idCardNumber: "",
				idCardExpiredDate: "",
				passwordConfirmation: "",
			},
			errors: null,
		};
	},
	validations() {
		return {
			form: {
				// firstname: { required, containsNotSpecial: (value) => !/[?!$^*]/.test(value) },
				// lastname: { required, containsNotSpecial: (value) => !/[?!$^*]/.test(value) },
				// email: { required, email },
				// password: {
				// 	required,
				// 	minLength: minLength(8), // I assume you'd want something like this too
				// 	containsUppercase: (value) => /[A-Z]/.test(value),
				// 	containsLowercase: (value) => /[a-z]/.test(value),
				// 	containsNumber: (value) => /[0-9]/.test(value),
				// 	containsSpecial: (value) => /[#?!@$%^&*+-]/.test(value),
				// },
				// passwordConfirmation: {
				// 	sameAsPassword: sameAs("password"),
				// },
				// phoneNumber: {
				// 	required,
				// 	phone: (value) => /^(06|08|09)+\d{8}$/.test(value),
				// },
			},
		};
	},
	methods: {
		async submitForm() {
			// this.isSubmitted = true;
			// // this.updateComponentData();
			// this.$v.$touch();
			// // console.log(this.$v.$invalid)
			// if (this.$v.$invalid) {
			// 	return;
			// }
			console.log("[Methods] - Pilot Registration has been uploaded.");

			try {
				await this.$axios
					.$post("/api/v1/auth/web/register", this.form)
					.then((e) => {
						console.log(e);
            this.$auth.strategy.token.set(e.data.token)
						this.$toast.success(this.$t("text.yourAccountHasBeenCreate"));
						// this.$router.push("/auth/signin");
						this.$router.push(this.localePath({ name: "auth-signin" }));
            
						// this.$swal.fire(this.$t('word.done'), this.$t('text.yourAccountHasBeenCreate'), 'success')

						// try {
						//   this.$auth.loginWith('laravelJWT', { data: this.form })
						//   this.$toast.success('Logged In!')
						//   window.location.replace("/");
						// } catch (err) {
						//   console.log(err)
						// }

						setTimeout(this.$toast.clear, 3000);
					})
					.catch((error) => {
						if (error.response) {
							console.log(error.response);
							this.errors = error.response.data.errors;
							this.$toast.error(`${this.$t("text.cantCreateAnAccount")}`);
							setTimeout(this.$toast.clear, 3000);
						}
					});
			} catch (e) {
				this.$toast.error(this.$t("text.somethingWentWrong"));
				setTimeout(this.$toast.clear, 3000);
			}
		},
	},
};
</script>

<style>
/*
  module.exports = {
      plugins: [require('@tailwindcss/forms'),]
  };
  */
.form-radio {
	-webkit-appearance: none;
	-moz-appearance: none;
	appearance: none;
	-webkit-print-color-adjust: exact;
	color-adjust: exact;
	display: inline-block;
	vertical-align: middle;
	background-origin: border-box;
	-webkit-user-select: none;
	-moz-user-select: none;
	-ms-user-select: none;
	user-select: none;
	flex-shrink: 0;
	border-radius: 100%;
	border-width: 2px;
}

.form-radio:checked {
	background-image: url("data:image/svg+xml,%3csvg viewBox='0 0 16 16' fill='white' xmlns='http://www.w3.org/2000/svg'%3e%3ccircle cx='8' cy='8' r='3'/%3e%3c/svg%3e");
	border-color: transparent;
	background-color: currentColor;
	background-size: 100% 100%;
	background-position: center;
	background-repeat: no-repeat;
}

@media not print {
	.form-radio::-ms-check {
		border-width: 1px;
		color: transparent;
		background: inherit;
		border-color: inherit;
		border-radius: inherit;
	}
}

.form-radio:focus {
	outline: none;
}

.form-select {
	background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23a0aec0'%3e%3cpath d='M15.3 9.3a1 1 0 0 1 1.4 1.4l-4 4a1 1 0 0 1-1.4 0l-4-4a1 1 0 0 1 1.4-1.4l3.3 3.29 3.3-3.3z'/%3e%3c/svg%3e");
	-webkit-appearance: none;
	-moz-appearance: none;
	appearance: none;
	-webkit-print-color-adjust: exact;
	color-adjust: exact;
	background-repeat: no-repeat;
	padding-top: 0.5rem;
	padding-right: 2.5rem;
	padding-bottom: 0.5rem;
	padding-left: 0.75rem;
	font-size: 1rem;
	line-height: 1.5;
	background-position: right 0.5rem center;
	background-size: 1.5em 1.5em;
}

.form-select::-ms-expand {
	color: #a0aec0;
	border: none;
}

@media not print {
	.form-select::-ms-expand {
		display: none;
	}
}

@media print and (-ms-high-contrast: active), print and (-ms-high-contrast: none) {
	.form-select {
		padding-right: 0.75rem;
	}
}
</style>
