<template>
	<div class="w-full mx-auto rounded-lg bg-white border border-gray-200 text-gray-800 font-light mb-6 mt-6">
		<div class="w-full p-3">
			<form>
				<!-- Email, Phone -->
				<div class="mb-3 border-b pb-4 border-dashed">
					<div class="grid grid-cols-1">
						<div>
							<label class="text-gray-600 font-semibold text-sm mb-2 ml-1"> {{ $t("form.forgot_password.title.forgot_password_form") }} </label>
							<div>
								<form @submit.prevent="handleSubmit">
									<div class="w-full flex justify-center p-2 mb-5">
										<span class="black--text">
											หากคุณไม่ได้รับ SMS
											<a href="#" class="text-center bg-caat-600 hover:bg-caat-700 rounded-md text-white py-1 px-1 font-medium" @click="resendOTP()" input-classes="a1">{{ $t("form.forgot_password.button.clickHere") }}</a>
											{{ $t("form.forgot_password.text.toRequestANewOTP") }}
										</span>
									</div>
									<div class="w-full flex justify-center p-2 mb-5">
										<span>{{ $t("form.forgot_password.text.PleaseConfirmWithin") }} {{ otp_text }} {{ $t("form.forgot_password.text.minutesBeforeTheOTPCodeExpires") }}</span>
									</div>
									<div class="md:col-span-1 col-span-2 mb-2 flex justify-center items-center">
										<OtpInput style="display: -webkit-inline-box; flex-direction: box" ref="otpInput" input-classes="otp-input" separator="-" :num-inputs="6" :should-auto-focus="true" :is-input-num="true" @on-change="handleOnChange" @on-complete="handleOnComplete" />
									</div>

									<hr class="mb-5 mt-4" />
								</form>
							</div>
						</div>
					</div>
				</div>
			</form>
		</div>
	</div>
</template>

<script>
import { required, email } from "vuelidate/lib/validators";
import OtpInput from "@bachdgvn/vue-otp-input";
import moment from "moment";
export default {
	props: {
		form: {
			type: Object,
			required: true,
		},
	},
	computed: {
		otp_text() {
			if (this.otp_timeout < 1) return this.$t("form.forgot_password.text.TheOTPHasExpired");
			const duration = moment.duration(this.otp_timeout, "seconds");
			return ` ${moment(duration._milliseconds).format("mm:ss")} `;
		},
	},
	components: {
		OtpInput,
	},
	data() {
		return {
			formx: this.form,
			otp_class: "otp_input",
			otp_timeout: 600,
			isSubmitted: false,
			otp_countdown: setInterval(() => {}),
		};
	},
	validations() {
		return {
			formx: {
				phoneNumber: { required },
			},
		};
	},
	mounted() {
		this.resetOTPTimeout();
		console.log(this.formx);
	},
	methods: {
		changeSteps() {
			this.$emit("changeSteps");
		},
		resetOTPTimeout() {
			const app = this;
			this.otp_class = "otp_input";
			app.otp_timeout = 600;
			clearInterval(app.otp_countdown);
			app.otp_countdown = setInterval(() => {
				app.otp_timeout -= 1;
				if (app.otp_timeout < 1) clearInterval(app.otp_countdown);
			}, 1000);
		},
		resendOTP() {
			this.$axios
				.$post("/api/v1/otp/request", this.formx)
				.then((resp) => {
					this.formx.transactionId = resp.data.transaction_id;
					console.log(this.formx);
					this.$toast.success(this.$t("text.Otphasbeensent"));
					// this.$router.push('/auth/changePassword')
					setTimeout(this.$toast.clear, 3000);
				})
				.catch((error) => {
					console.log(error);
					if (error.response) {
						console.log(error.response);
						this.errors = error.response.data.errors;
						this.$toast.error(`ไม่พบเบอร์โทรศัพท์ของคุณ`);
						setTimeout(this.$toast.clear, 3000);
					}
				});
			console.log("resendOTP");
			this.resetOTPTimeout();
		},
		submitForm() {
			this.isSubmitted = true;
			// this.updateComponentData();
			this.$v.$touch();
			console.log(this.$v.$invalid);
			if (this.$v.$invalid) {
				return;
			}
			console.log(this.formx);
			this.$axios
				.$post("/api/v1/otp/temptoken", this.formx)
				.then((resp) => {
          console.log(resp)
          this.formx.token = resp.token;
					this.$toast.success(this.$t("text.VerifyYourIdentitySuccessfully"));
					setTimeout(this.$toast.clear, 3000);
					this.changeSteps();
				})
				.catch((error) => {
					console.log(error);
					if (error.response) {
						console.log(error.response);
						this.errors = error.response.data.errors;
						this.$toast.error(`${this.$t("text.InvalidPin")}`);
						setTimeout(this.$toast.clear, 3000);
					}
				});
		},
		handleOnComplete(value) {
			this.formx.pin = value;
			this.submitForm();
		},
		handleOnChange(value) {
			this.formx.pin = value;
		},
		handleClearInput() {
			this.$refs.otpInput.clearInput();
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
