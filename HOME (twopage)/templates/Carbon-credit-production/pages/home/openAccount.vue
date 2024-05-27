<template>
	<section class="pt-2 pb-4 flex items-center justify-center">
		<div class="container mx-auto flex flex-col items-center justify-center">
			<div class="bg-white lg:w-6/12 md:w-100 rounded p-4">
				<div class="grid grid-cols-2 gap-4">
					<div class="col-span-2 bg-blue-100 border rounded border-blue-200 p-3">
						<p class="font-bold">{{ $t("openAccount.instructions") }}</p>
						<p class="text-sm">{{ $t("openAccount.accountOpening") }}</p>
					</div>
					<div class="col-span-2">
						<UILabel :text="$t('openAccount.accountName')" :required="true" />
						<UITextInput v-model="form.account_name" />
						<!-- <span class="text-right text-red-500" v-if="!$v.form.accountName.required && isSubmitted">{{ $t("project.create_page.form_validation.project_developer") }}</span> -->
						<UIErrorMsg v-if="!$v.form.account_name.required && isSubmitted">{{ $t("openAccount.validate.accountName") }}</UIErrorMsg>
						<UIErrorMsg v-if="!$v.form.account_name.containsNotSpecial && isSubmitted">{{ $t("openAccount.validate.containsNotSpecial") }}</UIErrorMsg>
						<UIErrorMsg v-if="!$v.form.account_name.minLength && isSubmitted">{{ $t("openAccount.validate.minLength2") }}</UIErrorMsg>
					</div>

					<div class="col-span-2">
						<UILabel :text="$t('openAccount.accountType') + '/' + $t('openAccount.document')" :required="true" />
						<div class="space-y-2">
							<div>
								<label for="guest" class="cursor-pointer">
									<div class="w-full px-2 py-3 border flex items-center gap-2 hover:bg-gray-50" :class="{ 'bg-gray-100': form.account_type === 0 }">
										<input v-model="form.account_type" class="w-4 h-4" :value="0" type="radio" name="accountType" id="guest" />
										<span class="text-sm">{{ $t("openAccount.account_type.option.guest") }}</span>
									</div>
									<div class="p-4 border border-t-0" v-show="form.account_type === 0">
										<HomeFileForm1 ref="file1" :isSubmitted="isSubmitted" :form="form" />
									</div>
								</label>
							</div>
							<div>
								<label for="juristic" class="cursor-pointer">
									<div class="w-full px-2 py-3 border flex items-center gap-2 hover:bg-gray-50" :class="{ 'bg-gray-100': form.account_type === 1 }">
										<input v-model="form.account_type" class="w-4 h-4" :value="1" type="radio" name="accountType" id="juristic" />
										<span class="text-sm">{{ $t("openAccount.account_type.option.juristic") }}</span>
									</div>
									<div class="p-4 border border-t-0" v-show="form.account_type === 1">
										<HomeFileForm2 ref="file2" :isSubmitted="isSubmitted" :form="form" />
									</div>
								</label>
							</div>
							<div>
								<label for="government" class="cursor-pointer">
									<div class="w-full px-2 py-3 border flex items-center gap-2 hover:bg-gray-50" :class="{ 'bg-gray-100': form.account_type === 2 }">
										<input v-model="form.account_type" class="w-4 h-4" :value="2" type="radio" name="accountType" id="government" />
										<span class="text-sm">{{ $t("openAccount.account_type.option.government") }}</span>
									</div>
									<div class="p-4 border border-t-0" v-show="form.account_type === 2">
										<HomeFileForm3 ref="file3" :isSubmitted="isSubmitted" :form="form" />
									</div>
								</label>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div class="flex items-center justify-center gap-4 mt-10">
				<nuxt-link :to="localePath('/')" class="bg-gray-300 hover:bg-gray-400 rounded w-40 text-center py-2">{{ $t("openAccount.cancel") }}</nuxt-link>

				<button @click="submitForm()" class="bg-tgo-teal-500 hover:bg-tgo-teal-600 text-gray-100 rounded w-40 text-center py-2">{{ $t("openAccount.submit") }}</button>
			</div>
		</div>
	</section>
</template>

<script>
import { required, minLength } from "vuelidate/lib/validators";
// import Dropzone from "nuxt-dropzone";
// import "nuxt-dropzone/dropzone.css";
export default {
	name: "CreditManagement",
	layout: "MainLayout",
	middleware: ["auth"],
	// components: {
	// 	Dropzone,
	// },

	data() {
		return {
			dropzoneOptions: {
				url: process.env.baseUrl + "/api/v1/form/upload",
				disablePreviews: true,
				previewsContainer: false,
				parallelUploads: 10,
				maxFiles: 10,
				acceptedFiles: "application/pdf",
			},
			isSubmitted: false,

			form: {
				// organization: "",
				account_type: 0,
				account_name: "",

				document: {},
				verified: {},
				authorize: {},
				card_id_owner: {},
				card_id_representative: {},
				employment_certificate: {},
			},
		};
	},
	validations() {
		return {
			form: {
				account_name: { required, containsNotSpecial: (value) => !/[?!$^*]/.test(value), minLength: minLength(2) },

				
			},
		};
	},

	async mounted() {},
	methods: {
		
		
		submitForm() {
			const app = this;
			this.isSubmitted = true;
			this.$v.$touch();
			if (this.$v.$invalid) {
				this.$swal.fire({
					icon: "error",
					iconColor: "#ef4444",
					confirmButtonColor: "#ef4444",
					title: this.$t("sweetalert.invalid"),
					
				});
				return;
			}
			if (this.$refs?.file1.$v.$invalid && this.form.account_type === 0) {
				this.$swal.fire({
					icon: "error",
					iconColor: "#ef4444",
					confirmButtonColor: "#ef4444",
					title: this.$t("sweetalert.invalid"),
					text: this.$t("openAccount.validate.document"),
				});
				return;
			}
			if (this.$refs?.file2.$v.$invalid && this.form.account_type === 1) {
				this.$swal.fire({
					icon: "error",
					iconColor: "#ef4444",
					confirmButtonColor: "#ef4444",
					title: this.$t("sweetalert.invalid"),
					text: this.$t("openAccount.validate.document"),
				});
				return;
			}
			if (this.$refs?.file3.$v.$invalid && this.form.account_type === 2) {
				this.$swal.fire({
					icon: "error",
					iconColor: "#ef4444",
					confirmButtonColor: "#ef4444",
					title: this.$t("sweetalert.invalid"),
					text: this.$t("openAccount.validate.document"),
				});
				return;
			}

			app.$swal
				.fire({
					icon: "info",
					iconColor: "#00b0d8",
					title: this.$t("alert.title.warning"),
					text: this.$t("alert.text.warning.create"),
					showCancelButton: true,

					confirmButtonColor: "#00b0d8",
					confirmButtonText: `${app.$t("button.confirm")}`,
					cancelButtonText: `${app.$t("button.cancel")}`,
					reverseButtons: true,
				})
				.then((result) => {
					if (result.isConfirmed) {
						app.$swal.fire({
							title: this.$t("sweetalert.waiting"),
							text: this.$t("loading"),
							allowOutsideClick: false,
							showCloseButton: false,
						});
						app.$swal.showLoading();
						app.$axios
							.$post(`/api/v1/auth/account`, app.form)
							.then(() => {
								app.$swal.close();
								app.$swal
									.fire({
										icon: "success",
										iconColor: "#059669",
										confirmButtonColor: "#059669",
										title: app.$t("alert.title.success.create"),
										text: app.$t("openAccount.accountOpening"),
									})
									.then(() => {
										app.$router.push(this.localePath("/home/credit"));
									});
							})
							.catch((err) => {
								app.$swal.close();
								app.$swal.fire({
									icon: "error",
									title: app.$t("alert.title.error.create"),
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
