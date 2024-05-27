<template>
	<div class="w-full pt-4">
		<div class="">
			<p class="text-green-600 text-lg">{{ $t("openAccount.form.title") }}</p>
			<p class="text-sm">{{ $t("openAccount.form.juristic.subtitle") }}</p>
		</div>
		<div class="border-t my-4"></div>
		<div class="grid grid-cols-1 gap-4">
			<div>
				<UILabel :text="$t('openAccount.form.document.verified')" :required="true"></UILabel>
				<UIFileUpload id="doc-upload-1" @upload="uploadImage($event, 'verified')" :filename="form.juristic.juristic_document.verified.name"></UIFileUpload>
				<UIErrorMsg v-if="!$v.form.juristic.juristic_document.verified.required && isSubmitted">{{ $t("openAccount.validate.document") }}</UIErrorMsg>
			</div>
			<div>
				<UILabel :text="$t('openAccount.form.document.authorize')" :required="true"></UILabel>
				<UIFileUpload id="doc-upload-2" @upload="uploadImage($event, 'authorize')" :filename="form.juristic.juristic_document.authorize.name"></UIFileUpload>
				<UIErrorMsg v-if="!$v.form.juristic.juristic_document.authorize.required && isSubmitted">{{ $t("openAccount.validate.document") }}</UIErrorMsg>
			</div>
			<!-- <div>
				<UILabel :text="$t('openAccount.form.document.card_id_owner')" :required="true"></UILabel>
				<UIFileUpload id="doc-upload-3" @upload="uploadImage($event, 'card_id_owner')" :filename="form.juristic.juristic_document.card_id_owner.name"></UIFileUpload>
				<UIErrorMsg v-if="!$v.form.juristic.juristic_document.card_id_owner.required && isSubmitted">{{ $t("openAccount.validate.document") }}</UIErrorMsg>
			</div> -->
			<div>
				<UILabel :text="$t('openAccount.form.document.card_id_representative')" :required="true"></UILabel>
				<UIFileUpload id="doc-upload-4" @upload="uploadImage($event, 'card_id_representative')" :filename="form.juristic.juristic_document.card_id_representative.name"></UIFileUpload>
				<UIErrorMsg v-if="!$v.form.juristic.juristic_document.card_id_representative.required && isSubmitted">{{ $t("openAccount.validate.document") }}</UIErrorMsg>
			</div>
			<!-- <div>
				<UILabel :text="$t('openAccount.form.document.employment_certificate')" :required="true"></UILabel>
				<UIFileUpload id="doc-upload-5" @upload="uploadImage($event, 'employment_certificate')" :filename="form.juristic.juristic_document.employment_certificate.name"></UIFileUpload>
				<UIErrorMsg v-if="!$v.form.juristic.juristic_document.employment_certificate.required && isSubmitted">{{ $t("openAccount.validate.document") }}</UIErrorMsg>
			</div> -->
		</div>

		<div class="h-20"></div>
		<div class="flex flex-col items-center text-sm gap-5">
			<button @click="next_step" class="w-80 bg-tgo-teal-500 border shadow-md rounded text-center py-2 text-white">{{ $t("button.next") }}</button>
			<button @click="$emit('back')">{{ $t("button.back") }}</button>
			<button @click="$emit('cancel')">{{ $t("button.cancel") }}</button>
		</div>
		<div class="my-4"></div>
	</div>
</template>

<script>
import { required } from "vuelidate/lib/validators";
import UploadImage from "../../static/mixins/upload-image";
export default {
	props: ["form"],
	mixins: [UploadImage],
	data() {
		return {
			filename: {
				verified: "",
				authorize: "",
				card_id_owner: "",
				card_id_representative: "",
				employment_certificate: "",
			},

			isSubmitted: false,
		};
	},
	validations() {
		return {
			form: {
				juristic: {
					juristic_document: {
						verified: { required },
						authorize: { required },
						// card_id_owner: { required },
						card_id_representative: { required },
						// employment_certificate: { required },
					},
				},
			},
		};
	},
	methods: {
		next_step() {
			this.isSubmitted = true;
			this.$v.$touch();
			if (this.$v.$invalid) {
				this.$swal.fire({
					icon: "error",
					iconColor: "#ef4444",
					confirmButtonColor: "#ef4444",
					title: this.$t("sweetalert.invalid"),
					text: this.$t("openAccount.validate.document"),
				});
				return 0;
			}
			this.$emit("click");
		},
		async uploadImage(input, key) {
			if (input.target.files[0]) {
				const formData = new FormData();
				const fileItem = input.target.files[0];
				// console.log(fileItem);
				formData.append("file", fileItem);
				const resp = await this.uploadImages(formData);
				// console.log(resp);
				this.form.juristic.juristic_document[key] = resp;
			}
		},
	},
};
</script>

<style>
</style>