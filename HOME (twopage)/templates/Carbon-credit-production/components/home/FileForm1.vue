<template>
	<div class="w-full ">
	
		<div>
			<UILabel :text="$t('openAccount.form.document.card_id')" :required="true"></UILabel>
			<UIFileUpload id="guest-upload" @upload="uploadImage" :filename="filename"></UIFileUpload>
			<UIErrorMsg v-if="!$v.form.document.required && isSubmitted">{{ $t("openAccount.validate.document") }}</UIErrorMsg>
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
			filename: "",
			
		};
	},
	validations() {
		return {
			form: {
				document: { required },
			},
		};
	},
	methods: {
		
		async uploadImage(input) {
			// console.log(input.target.files[0]);
			if (input.target.files[0]) {
				const formData = new FormData();
				const fileItem = input.target.files[0];
				// console.log(fileItem);
				formData.append("file", fileItem);
				const resp = await this.uploadImages(formData);
				// console.log(resp);
				this.filename = resp.name
				this.form.document = resp;
			}
		},
	},
};
</script>

<style>
</style>