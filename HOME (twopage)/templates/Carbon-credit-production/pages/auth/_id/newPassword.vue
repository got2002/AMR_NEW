<template>
	<div class="w-full h-full">
		<div class="container mx-auto flex justify-center items-center my-32">
			<div class="w-8/12 bg-white border rounded shadow-sm flex">
				<div class="w-1/2 p-6">
					<div class="py-4 border-b">
						<h1 class="text-3xl font-medium text-green-600">{{ $t("auth.newPassword.title") }}</h1>
						<h1 class="text-sm">{{ $t("auth.newPassword.subtitle") }}</h1>
					</div>

					<div class="grid grid-cols-1 gap-6 py-4">
						<div class="col-span-1">
							<label class="font-thin">{{ $t("auth.new_password") }}</label>
							<div class="relative w-full">
								<svg @click="changeInputType(1)" v-if="inputType1 == 'password' && form.password" class="w-6 h-6 absolute z-10 top-3 right-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
									<path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
									<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
								</svg>
								<svg @click="changeInputType(2)" v-if="inputType1 == 'text' && form.password" class="w-6 h-6 absolute z-10 top-3 right-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
									<path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
								</svg>

								<input v-model="form.password" :type="inputType1" class="w-full p-3 mb-1 border border-gray-200 rounded-md outline-none focus:border-green-600 transition-colors" required />
							</div>
						</div>
						<div class="col-span-1">
							<label class="font-thin">{{ $t("auth.confirm_password") }}</label>
							<div class="relative w-full">
								<svg @click="changeInputType2(1)" v-if="inputType2 == 'password' && form.passwordConfirmation" class="w-6 h-6 absolute z-10 top-3 right-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
									<path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
									<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
								</svg>
								<svg @click="changeInputType2(2)" v-if="inputType2 == 'text' && form.passwordConfirmation" class="w-6 h-6 absolute z-10 top-3 right-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
									<path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
								</svg>

								<input v-model="form.passwordConfirmation" :type="inputType2" class="w-full p-3 mb-1 border border-gray-200 rounded-md outline-none focus:border-green-600 transition-colors" required />
							</div>
						</div>
					</div>
					<div class="w-full flex flex-col items-center gap-4 mt-4">
						<button class="text-center w-full bg-tgo-teal-500 hover:bg-tgo-teal-600 border border-gray-600 rounded-md text-white py-3 font-medium" @click="submitForm()">
							{{ $t("button.confirm") }}
						</button>
						<nuxt-link class="text-gray-500 hover:underline hover:text-green-500" to="/auth/signin">{{ $t("button.back") }}</nuxt-link>
					</div>
				</div>
				<div class="w-1/2 bg-gray-50 p-6 rounded-r">
					<div class="w-full p-4 relative">
						<p class="font-bold text-xl text-center">{{ $t("auth.subtitle2") }}</p>
						<svg class="absolute top-0 right-0" width="27" height="27" viewBox="0 0 27 27" fill="none" xmlns="http://www.w3.org/2000/svg">
							<circle cx="24.4289" cy="2.57143" r="2.57143" fill="#059669" />
							<circle cx="17.1437" cy="2.57143" r="2.57143" fill="#059669" />
							<circle cx="9.85658" cy="2.57143" r="2.57143" fill="#059669" />
							<circle cx="2.57143" cy="2.57143" r="2.57143" fill="#059669" />
							<circle cx="24.4289" cy="9.85719" r="2.57143" fill="#059669" />
							<circle cx="24.4289" cy="17.1428" r="2.57143" fill="#059669" />
							<circle cx="24.4289" cy="24.4286" r="2.57143" fill="#059669" />
							<path d="M19.7151 17.1428C19.7151 18.563 18.5639 19.7143 17.1437 19.7143C15.7235 19.7143 14.5723 18.563 14.5723 17.1428C14.5723 15.7227 15.7235 14.5714 17.1437 14.5714C18.5639 14.5714 19.7151 15.7227 19.7151 17.1428Z" fill="#059669" />
							<circle cx="17.1437" cy="9.85719" r="2.57143" fill="#059669" />
							<circle cx="9.85658" cy="9.85719" r="2.57143" fill="#059669" />
						</svg>
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
import { required, email } from "vuelidate/lib/validators";
export default {
	name: "ForgetPasswordPage",
	layout: "MainLayout",
	data() {
		return {
			inputType1: "password",
			inputType2: "password",
			form: {
				password: "",
				passwordConfirmation: "",
				token:this.$route.params.id
			},
		};
	},
	validations() {
		return {
			form: {
				password: {required},
				passwordConfirmation: {required},
				
			},
		};
	},
	methods: {
		changeInputType(value) {
			switch (value) {
				case 1:
					this.inputType1 = "text";
					break;
				case 2:
					this.inputType1 = "password";
					break;
				default:
					this.inputType1 = "password";
					break;
			}
		},
		changeInputType2(value) {
			switch (value) {
				case 1:
					this.inputType2 = "text";
					break;
				case 2:
					this.inputType2 = "password";
					break;
				default:
					this.inputType2 = "password";
					break;
			}
		},
		submitForm() {
			const app = this
			app.isSubmitted = true;
			// app.updateComponentData();
			app.$v.$touch();

			if (app.$v.$invalid) {
				app.$swal.fire({
					icon: "error",
					title: app.$t("sweetalert.invalid"),
					text: app.$t("sweetalert.complete_information_text"),
				});
				return;
			}

			app.$axios
				.$post("/api/v1/auth/set-new-password", app.form)
				.then((resp) => {
					// console.log(app.form);
					app.$swal
						.fire({
							icon: "success",
							iconColor:'#059669',
							title: app.$t("sweetalert.auth.newPassword.success.title"),
							text: app.$t("sweetalert.auth.newPassword.success.sub_title"),
							confirmButtonColor:'#059669'
						})
						.then(() => {
							app.$router.push(app.localePath({ name: "auth-signin" }));
						});
				})
				.catch((error) => {
					console.log(error);
					app.$swal.fire({
						icon: "error",
						title: app.$t("sweetalert.auth.newPassword.error.title"),
						text: app.$t("sweetalert.auth.newPassword.error.sub_title"),
					});
				});
		},
	},
};
</script>

<style>
</style>