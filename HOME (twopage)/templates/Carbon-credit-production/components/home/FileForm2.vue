<template>
	<div class="w-full pt-4">
		
	
		<div class="grid grid-cols-1 gap-4">
			<div>
				<UILabel :text="$t('openAccount.form.document.verified')" :required="true"></UILabel>
				<UIFileUpload id="doc-upload-1" @upload="uploadImage($event, 'verified')" :filename="form.verified?.name"></UIFileUpload>
				<UIErrorMsg v-if="!$v.form.verified.required && isSubmitted">{{ $t("openAccount.validate.document") }}</UIErrorMsg>
			</div>
			<div>
				<UILabel :text="$t('openAccount.form.document.authorize')" :required="true"></UILabel>
				<UIFileUpload id="doc-upload-2" @upload="uploadImage($event, 'authorize')" :filename="form.authorize?.name"></UIFileUpload>
				<UIErrorMsg v-if="!$v.form.authorize.required && isSubmitted">{{ $t("openAccount.validate.document") }}</UIErrorMsg>
			</div>
			<div>
				<UILabel :text="$t('openAccount.form.document.card_id_owner')" :required="true"></UILabel>
				<UIFileUpload id="doc-upload-3" @upload="uploadImage($event, 'card_id_owner')" :filename="form.card_id_owner?.name"></UIFileUpload>
				<UIErrorMsg v-if="!$v.form.card_id_owner.required && isSubmitted">{{ $t("openAccount.validate.document") }}</UIErrorMsg>
			</div>
			<div>
				<UILabel :text="$t('openAccount.form.document.card_id_representative')" :required="true"></UILabel>
				<UIFileUpload id="doc-upload-4" @upload="uploadImage($event, 'card_id_representative')" :filename="form.card_id_representative?.name"></UIFileUpload>
				<UIErrorMsg v-if="!$v.form.card_id_representative.required && isSubmitted">{{ $t("openAccount.validate.document") }}</UIErrorMsg>
			</div>
			<div>
				<UILabel :text="$t('openAccount.form.document.employment_certificate')" :required="true"></UILabel>
				<UIFileUpload id="doc-upload-5" @upload="uploadImage($event, 'employment_certificate')" :filename="form.employment_certificate?.name"></UIFileUpload>
				<UIErrorMsg v-if="!$v.form.employment_certificate.required && isSubmitted">{{ $t("openAccount.validate.document") }}</UIErrorMsg>
			</div>
		</div>

		
	</div>
</template>

<script>
import { required } from "vuelidate/lib/validators";
import UploadImage from "../../static/mixins/upload-image";
export default {
	props: ["form","isSubmitted"],
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

			
		};
	},
	validations() {
		return {
			form: {
				verified: { required },
				authorize: { required },
				card_id_owner: { required },
				card_id_representative: { required },
				employment_certificate: { required },
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
				this.form[key] = resp;
			}
		},
	},
};
</script>

<style>
</style>