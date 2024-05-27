<template>
	<div class="w-full pt-4">
		<div class="">
			<p class="text-green-600 text-lg">{{ $t("openAccount.form.title") }}</p>
			<p class="text-sm">{{ $t("openAccount.form.guest.subtitle") }}</p>
		</div>
		<div class="border-t my-4"></div>
		<div>
			<UILabel :text="$t('openAccount.form.document.card_id')" :required="true"></UILabel>
			<UIFileUpload id="guest-upload" @upload="uploadImage" :filename="this.form.guest.document?.name"></UIFileUpload>
			<UIErrorMsg v-if="!$v.form.guest.document.required && isSubmitted">{{ $t("openAccount.validate.document") }}</UIErrorMsg>
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
			filename: "",
			isSubmitted: false,
		};
	},
	validations() {
		return {
			form: {
				guest: {
					document: { required },
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
		async uploadImage(input) {
			// console.log(input.target.files[0]);
			if (input.target.files[0]) {
				const formData = new FormData();
				const fileItem = input.target.files[0];
				// console.log(fileItem);
				formData.append("file", fileItem);
				const resp = await this.uploadImages(formData);
				// console.log(resp);
				this.form.guest.document = resp;
			}
		},
	},
};
</script>

<style>
</style>