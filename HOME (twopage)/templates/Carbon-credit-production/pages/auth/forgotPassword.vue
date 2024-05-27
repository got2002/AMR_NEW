<template>
	<div class="w-full h-full">
		<div class="container mx-auto flex justify-center items-center my-32">
			<div class="w-8/12 bg-white border rounded shadow-sm flex">
				<div class="w-1/2 p-6">
					<div class="py-4 border-b">
						<h1 class="text-3xl font-medium text-green-600">{{ $t("auth.forgotPassword.title") }}</h1>
						<h1 class="text-sm">{{ $t("auth.forgotPassword.subtitle") }}</h1>
					</div>

					<div class="grid grid-cols-1 gap-6 py-4">
						<div class="col-span-1">
							<label class="font-thin">{{ $t("auth.email") }}</label>
							<input v-model="form.email" type="text" class="w-full p-3 mb-1 border border-gray-200 rounded-md outline-none focus:border-green-600 transition-colors" required />
						</div>
					</div>
					<div class="w-full flex flex-col items-center gap-4 mt-4">
						<button class="text-center w-full bg-tgo-teal-500 hover:bg-tgo-teal-600 border border-gray-600 rounded-md text-white py-3 font-medium" @click="submitForm()">
							{{ $t("button.confirm") }}
						</button>
						<nuxt-link class="text-gray-500 hover:underline hover:text-green-500" to="/auth/signin">{{ $t("button.login") }}</nuxt-link>
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
	middleware: "guest",
	data() {
		return {
			isSubmitted: false,

			form: {
				email: "",
			},

			errors: null,
		};
	},
	validations() {
		return {
			form: {
				email: { required, email },
			},
		};
	},

	methods: {
		submitForm() {
			const app = this;
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
				.$post("/api/v1/auth/reset-password-request", app.form)
				.then((resp) => {
					// console.log(app.form);
					app.$swal
						.fire({
							icon: "success",
							iconColor:'#059669',
							title: app.$t("sweetalert.auth.forgotPassword.success.title"),
							text: app.$t("sweetalert.auth.forgotPassword.success.sub_title"),
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
						title: app.$t("sweetalert.auth.forgotPassword.error.title"),
						text: app.$t("sweetalert.auth.forgotPassword.error.sub_title"),
					});
					// if (error.response) {
					// 	console.log(error.response);

					// 	app.$toast.error(error.response.data.errors[0]);
					// 	setTimeout(app.$toast.clear, 3000);
					// }
				});
		},
	},
};
</script>

<style>
</style>
