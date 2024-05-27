<template>
	<div class="h-screen">
		<div class="container mx-auto 2xl:w-4/12 lg:w-6/12 md:w-6/12 sm:w-11/12 xs:w-11/12">
			<div class="flex justify-center items-center pb-2">
				<div>
					<h2 class="text-2xl font-bold">{{ $t("profile.change_password_title") }}</h2>
				</div>
			</div>
			<div class="p-4 bg-white shadow-sm">
				<div>
					<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">{{ $t("profile.new_password") }} <span class="text-red-600">*</span></label>
					<div class="relative">
						<div class="absolute z-10 top-2 right-2 cursor-pointer" @click="showPassword1">
							<svg v-if="typeInput1 == 'password' && form.password" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
								<path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
								<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
							</svg>
							<svg v-else-if="typeInput1 != 'password' && form.password" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
								<path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
							</svg>
						</div>
						<input v-model="form.password" :type="typeInput1" class="w-full px-3 py-2 mb-1 bg-gray-100 border border-gray-300 rounded-sm focus:outline-none focus:border-indigo-500 transition-colors" required />
					</div>
					<p class="text-xs text-red-500" v-if="!$v.form.password.required && isSubmitted">{{ $t("form_validation.require.password") }}</p>
					<p class="text-xs text-red-500" v-if="!$v.form.password.minLength && isSubmitted">{{ $t("form_validation.min_length.password") }}</p>
					<p class="text-xs text-red-500" v-if="!$v.form.password.strongPass">{{ $t("form_validation.strong_password") }}</p>
				</div>

				<div>
					<label class="text-gray-600 font-semibold text-sm mb-2 ml-1">{{ $t("profile.confirm_password") }} <span class="text-red-600">*</span></label>
					<div class="relative">
						<div class="absolute z-10 top-2 right-2 cursor-pointer" @click="showPassword2">
							<svg v-if="typeInput2 == 'password' && form.passwordConfirmation" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
								<path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
								<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
							</svg>
							<svg v-else-if="typeInput2 != 'password' && form.passwordConfirmation" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
								<path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
							</svg>
						</div>
						<input v-model="form.passwordConfirmation" :type="typeInput2" class="w-full px-3 py-2 mb-1 bg-gray-100 border border-gray-300 rounded-sm focus:outline-none focus:border-indigo-500 transition-colors" required />
					</div>
					<p class="text-xs text-red-500" v-if="!$v.form.passwordConfirmation.sameAsPassword && isSubmitted">{{ $t("form_validation.same_as.confirm_password") }}</p>
				</div>
			</div>
			<div class="flex justify-center gap-4 mt-3">
				<button class="w-20 py-2 text-center bg-gray-500 rounded shadow-sm text-white hover:bg-gray-600" @click="$router.push(localePath('/profile'))">
					<span class="text-center">{{ $t("button.close") }}</span>
				</button>
				<button @click="submitForm" class="w-20 py-2 text-white bg-tgo-teal-500 hover:bg-tgo-teal-600 rounded shadow-sm hover:text-theme-white flex items-center justify-center">
					<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
						<path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
					</svg>

					{{ $t("button.save") }}
				</button>
			</div>
		</div>
	</div>
</template>

<script>
	import { required, sameAs, minLength } from "vuelidate/lib/validators";

	export default {
		layout: "ProfileLayout",
		middleware: ["auth"],
		data() {
			return {
				form: {
					password: null,
					passwordConfirmation: null,
				},
				typeInput1: "password",
				typeInput2: "password",
				isSubmitted: false,
			};
		},
		validations() {
			return {
				form: {
					password: {
						required,
						minLength: minLength(8),
						strongPass: (value) => /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]/.test(value),
					},
					passwordConfirmation: {
						sameAsPassword: sameAs("password"),
					},
				},
			};
		},
		methods: {
			showPassword1() {
				if (this.typeInput1 === "password") {
					this.typeInput1 = "text";
				} else {
					this.typeInput1 = "password";
				}
			},
			showPassword2() {
				if (this.typeInput2 === "password") {
					this.typeInput2 = "text";
				} else {
					this.typeInput2 = "password";
				}
			},
			submitForm() {
				this.isSubmitted = true;
				this.$v.$touch();
				if (this.$v.$invalid) {
					return;
				}

				const app = this;

				app.$swal
					.fire({
						icon: "info",
						iconColor: "#00b0d8",
						iconHtml: `
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
									<path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m0-10.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.75c0 5.592 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.57-.598-3.75h-.152c-3.196 0-6.1-1.249-8.25-3.286zm0 13.036h.008v.008H12v-.008z" />
								</svg>
								`,
						title: this.$t("sweetalert.profile.change_password.confirm.title"),
						text: this.$t("sweetalert.profile.change_password.confirm.sub_title"),
						showCancelButton: true,

						confirmButtonColor: "#00b0d8",
						confirmButtonText: this.$t("button.confirm"),
						cancelButtonText: this.$t("button.cancel"),
						reverseButtons:true
					})
					.then((result) => {
						if (result.isConfirmed) {
							app.$swal.fire({
								title: this.$t("sweetalert.waiting"),
								text: this.$t("saving"),
								allowOutsideClick: false,
								showCloseButton: false,
							});
							app.$swal.showLoading();

							app.$axios
								.$put(`/api/v1/auth/changePassword`, app.form)
								.then((resp) => {
									// console.log(resp);
									app.$swal.close();

									// app.$router.push(app.localePath({ name: "da" }));

									// app.getProfile()
									app.form = {
										password: null,
										passwordConfirmation: null,
									};
									app.$swal
										.fire({
											icon: "success",
											iconColor:'#059669',
											confirmButtonColor: "#059669",
											title: app.$t("sweetalert.profile.change_password.success.title"),
											timer: 2000,
											timerProgressBar: true,
										})
										.then(() => {
											app.$router.push(app.localePath("/profile"));
										});
								})
								.catch((err) => {
									app.$swal.close();
									app.$swal.fire({
										icon: "error",
										title: app.$t("sweetalert.profile.change_password.error.title"),
									
									});
									console.log(err);
								});
						}
					});
			},
		},
	};
</script>

<style scoped>
	input::-ms-reveal,
	input::-ms-clear {
		display: none;
	}
</style>
