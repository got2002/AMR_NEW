<template>
	<div class="w-full h-full">
		<div class="container mx-0 md:mx-auto flex justify-center items-center my-2 md:my-32">
			<div class="w-auto md:w-8/12 bg-white border rounded shadow-sm flex flex-col md:flex-row">
				<div class="w-full md:w-1/2 p-6">
					<div class="py-4 border-b">
						<h1 class="text-3xl font-medium text-green-600">{{ $t("auth.title") }}</h1>
						<h1 class="text-sm">{{ $t("auth.subtitle") }}</h1>
					</div>

					<form @submit.prevent="submitForm()" class="grid grid-cols-1 gap-6 py-4">
						<div class="col-span-1">
							<label class="font-thin">{{ $t("auth.email") }}</label>
							<input v-model="form.email" type="text" class="w-full p-3 mb-1 border border-gray-200 rounded-md outline-none focus:border-green-600 transition-colors" required />
						</div>
						<div class="col-span-1">
							<label class="font-thin">{{ $t("auth.password") }}</label>
							<div class="relative w-full">
								<svg @click="changeInputType(1)" v-if="inputType == 'password' && form.password" class="w-6 h-6 absolute z-10 top-3 right-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
									<path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
									<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
								</svg>
								<svg @click="changeInputType(2)" v-if="inputType == 'text' && form.password" class="w-6 h-6 absolute z-10 top-3 right-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
									<path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
								</svg>

								<input v-model="form.password" :type="inputType" class="w-full p-3 mb-1 border border-gray-200 rounded-md outline-none focus:border-green-600 transition-colors" required />
							</div>
						</div>
						<div class="col-sapn-1 text-right">
							<nuxt-link class="text-gray-500 hover:underline hover:text-green-500" to="/auth/forgotPassword">
								<span>{{ $t("button.forgotPassword") }}</span>
							</nuxt-link>
						</div>
					</form>
					<div class="w-full flex flex-col items-center gap-4 mt-4">
						<button @click="submitForm()" class="text-center w-full bg-tgo-teal-500 hover:bg-tgo-teal-600 border border-gray-600 rounded-md text-white py-3 font-medium" >
							{{ $t("button.login") }}
						</button>
						<!-- <nuxt-link class="text-gray-500 hover:underline hover:text-green-500" to="/auth/register">{{ $t("topnav.open_new_account") }}</nuxt-link> -->
					</div>
				</div>
				<div class="w-full md:w-1/2 bg-gray-50 p-6 rounded-r">
					<div class="w-full p-4 relative">
						<p class="font-bold text-xl text-center">{{ $t("auth.subtitle2") }}</p>
						<ManyCircle />
					</div>

					<div class="w-full mt-4">
						<AuthTHLogo v-if="$i18n.locale === 'th'"></AuthTHLogo>
						<AuthENLogo v-else></AuthENLogo>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { required } from "vuelidate/lib/validators";

export default {
	name: "SignInPage",
	layout: "MainLayout",
	middleware: "guest",
	data() {
		return {
			isSubmitted: false,
			inputType: "password",
			twofac: false,
			steps: 1,
			form: {
				email: "",
				password: "",
			},
			otp_class: "otp_input",
			otp_timeout: 600,
			otp_countdown: setInterval(() => {}),
			pin: "",
		};
	},

	validations() {
		return {
			form: {
				email: {
					required,
				},
				password: {
					required,
				},
			},
		};
	},
	mounted() {
		// this.$swal("dd",'','success')
	},

	methods: {
		async submitForm() {
			this.isSubmitted = true;
			this.$v.$touch();
			if (this.$v.$invalid) {
				return;
			}
			this.$swal.fire({
				title: this.$t("sweetalert.waiting"),
				text: this.$t("loading"),
				allowOutsideClick: false,
				showCloseButton: false,
			});
			this.$swal.showLoading();
			console.log("[Metstration has been uploaded.");

			try {
				await this.$auth.loginWith("local", { data: this.form });

				this.$toast.success(this.$t("toast.login.success"));
				setTimeout(this.$toast.clear, 3000);
				this.$swal.close();
				this.redirectByRole(this.$auth.user);
				// this.$router.push(this.localePath("/"));
				// this.$router.push("/dashbroad/landManagement");
			} catch (e) {
				console.log("Error Response", e);
				this.$toast.error(e.response.data.errors[0]);
				setTimeout(this.$toast.clear, 3000);
				this.$swal.close();
			}
			// return true
		},
		redirectByRole(user) {
			// console.log(role);
			switch (user.role) {
				case 0:
					console.log(/(showroom)/.test(document.referrer));
					if (/(showroom)/.test(document.referrer)) {
						console.log(this.localePath(document.referrer));
						this.$router.go(-1)
					}
					else{
						if (user.accountID == null) this.$router.push(this.localePath("/"));
						else this.$router.push(this.localePath({ name: "home-credit" }));
					}

					break;

				default:
					console.log(/(showroom)/.test(document.referrer));

					if (/(showroom)/.test(document.referrer)) {
						console.log(this.localePath(document.referrer));
						this.$router.go(-1)
					}else{
						this.$router.push(this.localePath({ name: "dashboard" }));
					}
					
					break;
			}
		},
		changeInputType(value) {
			switch (value) {
				case 1:
					this.inputType = "text";
					break;
				case 2:
					this.inputType = "password";
					break;
				default:
					this.inputType = "password";
					break;
			}
		},
	},
};
</script>

<style>
.otp-input {
	width: 40px;
	height: 40px;
	padding: 5px;
	margin: 0 10px;
	font-size: 20px;
	border-radius: 4px;
	border: 1px solid rgba(0, 0, 0, 0.3);
	text-align: center;
}
.otp-input::-webkit-inner-spin-button,
.otp-input::-webkit-outer-spin-button {
	-webkit-appearance: none;
	margin: 0;
}
.a {
	color: red;
}
</style>
