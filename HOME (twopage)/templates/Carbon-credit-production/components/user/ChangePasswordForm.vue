<template>
	<div class="w-full pt-4 flex p-2">
		<div class="grid grid-cols-2 gap-4 w-2/4 m-2 pr-4 border-r">
			<div class="col-span-2">
				<p class="text-green-600 text-lg">{{ $t("user.change_password_typing_option") }}</p>
			</div>
			<div class="col-span-2">
				<p class="text-sm text-red-500 p-2 bg-red-50 rounded-md">{{ $t("form_validation.strong_password") }}</p>
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.password')" :required="true" />
				<UIPasswordInput v-model="form.password" />
				<UIErrorMsg v-if="!$v.form.password.required && isSubmitted">{{ $t("openAccount.validate.password") }}</UIErrorMsg>
				<UIErrorMsg v-if="(!$v.form.password.minLength && !$v.form.password.containsUppercase || !$v.form.password.containsLowercase || !$v.form.password.containsNumber || !$v.form.password.containsSpecial) && isSubmitted">{{ $t("form_validation.strong_password") }}</UIErrorMsg>
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.passwordConfirmation')" :required="true" />
				<UIPasswordInput v-model="form.passwordConfirmation" />
				<UIErrorMsg v-if="!$v.form.passwordConfirmation.sameAsPassword && isSubmitted">{{ $t("openAccount.validate.passwordConfirmation") }}</UIErrorMsg>
			</div>
			<div class="col-span-2">
				<div class="flex justify-end">
					<button @click="submitForm" class="w-1/4 bg-green-500 hover:bg-green-600 text-white p-2 rounded-md">{{ $t("button.save") }}</button>
				</div>
			</div>
		</div>
        <div class="grid grid-cols-2 gap-4 w-2/4 m-2  h-full">
			<div class="col-span-2 ">
				<p class="text-green-600 text-lg">{{ $t("user.change_password_sent_mail_option") }}</p>
			</div>
            <div class="col-span-2">
				<p class="text-sm text-blue-500 p-2 bg-blue-50 rounded-md" v-html='$t("user.change_password_sent_mail_message", {email: userForm.email})'></p>
                
			</div>
			<div class="col-span-2 flex w-full h-full items-end justify-end">
				<button @click="sendEmail" class="w-1/4 bg-green-500 hover:bg-green-600 text-white p-2 rounded-md">{{ $t("user.change_password_sent_mail_option_button") }}</button>
			</div>
			
		</div>
	</div>
</template>

<script>
	import { required, minLength, sameAs } from "vuelidate/lib/validators";
	export default {
		props: ["userForm"],
		data() {
			return {
				isSubmitted: false,
				form: {
					password: null,
					passwordConfirmation: null,
				},
			};
		},
		validations() {
			return {
				form: {
					password: {
						required,
						minLength: minLength(8), // I assume you'd want something like this too
						containsUppercase: (value) => /[A-Z]/.test(value),
						containsLowercase: (value) => /[a-z]/.test(value),
						containsNumber: (value) => /[0-9]/.test(value),
						containsSpecial: (value) => /[#?!@$%^&*+-]/.test(value),
					},
					passwordConfirmation: {
						required,
						sameAsPassword: sameAs("password"),
					},
				},
			};
		},
		methods: {
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
						reverseButtons: true,
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
								.$put(`/api/v1/user/${app.$route.params.id}/change_password`, app.form)
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
											iconColor: "#059669",
											confirmButtonColor: "#059669",
											title: app.$t("sweetalert.profile.change_password.success.title"),
											timer: 2000,
											timerProgressBar: true,
										})
										.then(() => {
											app.$router.push(app.localePath("/users"));
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
			sendEmail() {
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
						reverseButtons: true,
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
								.$put(`/api/v1/user/${app.$route.params.id}/generate_password`, app.form)
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
											iconColor: "#059669",
											confirmButtonColor: "#059669",
											title: app.$t("sweetalert.profile.change_password.success.title"),
											timer: 2000,
											timerProgressBar: true,
										})
										.then(() => {
											app.$router.push(app.localePath("/users"));
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

<style></style>
