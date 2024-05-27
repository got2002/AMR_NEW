<template>
	<div class="w-full pt-4">
		<div class="">
			<p class="text-green-600 text-lg">{{ $t("openAccount.form.title") }}</p>
			<p class="text-sm">{{ $t("openAccount.form.juristic.subtitle") }}</p>
		</div>
		<div class="border-t my-4"></div>

		<div class="grid grid-cols-4 gap-4">
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.juristic.name')" />
				<UIShowInput :value="form.juristic.juristic_name" />
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.phone_number')" />
				<UIShowInput :value="form.juristic.phone_number" />
			</div>
			<div class="col-span-4">
				<UILabel :text="$t('openAccount.form.juristic.address')" />
				<UIShowInput :value="form.juristic.address" />
			</div>

			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.province')" />
				<UIShowInput :value="form.juristic.province" />
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.district')" />
				<UIShowInput :value="form.juristic.district" />
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.subdistrict')" />
				<UIShowInput :value="form.juristic.subdistrict" />
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.postcode')" />
				<UIShowInput :value="form.juristic.postcode" />
			</div>

			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.juristic.number')" :required="false" />
				<UIShowInput :value="form.juristic.juristic_number" />
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.juristic.alien_id')" :required="false" />
				<UIShowInput :value="form.juristic.alien_number" />
			</div>

			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.email')" />
				<UIShowInput :value="form.juristic.email" />
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.password')" />
				<UIPasswordInput :disable="true" v-model="form.juristic.password" />
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.passwordConfirmation')" />
				<UIPasswordInput :disable="true" v-model="form.juristic.passwordConfirmation" />
			</div>
			<div class="col-span-4"></div>
			<div class="col-span-4 border-t"></div>
			<div class="col-span-4"></div>

			<div class="col-span-4">
				<p class="text-base underline">{{ $t("openAccount.form.juristic.grantee_info.title") }}</p>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.firstname')" />
				<UIShowInput :value="form.juristic.firstname" />
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.lastname')" />
				<UIShowInput :value="form.juristic.lastname" />
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.card_id')" />
				<UIShowInput :value="form.juristic.card_id" />
			</div>

			<div class="col-span-4"></div>
			<div class="col-span-4 border-t"></div>
			<div class="col-span-4"></div>
			<div class="col-span-4">
				<p class="text-base underline">{{ $t("openAccount.form.juristic.account_detail.title") }}</p>
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.accountName')" />
				<UIShowInput :value="form.juristic.accountName" />
			</div>

			<div class="col-span-2 space-y-3">
				<UILabel :text="$t('openAccount.form.request_permission.title')" />
				<AuthRequestPermission :form="form.juristic" :disable="true" />
			</div>

			<div class="col-span-4 border-t my-2"></div>
			<div class="col-span-4">
				<p class="text-base underline">{{ $t("openAccount.showDocument.title") }}</p>
			</div>

			<div class="col-span-4">
				<table class="border w-full">
					<tr class="border divide-x h-20 text-sm">
						<td class="w-1/12 text-center p-2 bg-gray-100">1.</td>
						<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.verified") }}</td>
						<td class="w-5/12 p-2 text-center">
							<span 
							class="truncate hover:underline cursor-pointer" :title="$t('button.see')" 
							@click="openPDF(form.juristic.juristic_document.verified.src)">
							{{ form.juristic.juristic_document.verified.name }}
						</span>
						</td>
					</tr>
					<tr class="border divide-x h-20 text-sm">
						<td class="w-1/12 text-center p-2 bg-gray-100">2.</td>
						<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.authorize") }}</td>
						<td class="w-5/12 p-2 text-center">
							<span class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(form.juristic.juristic_document.authorize.src)">{{ form.juristic.juristic_document.authorize.name }}</span>
						</td>
					</tr>
					<!-- <tr class="border divide-x h-20 text-sm">
						<td class="w-1/12 text-center p-2 bg-gray-100">3.</td>
						<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.card_id_owner") }}</td>
						<td class="w-5/12 p-2 text-center">
							<span class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(form.juristic.juristic_document.card_id_owner.src)">{{ form.juristic.juristic_document.verified.name }}</span>
						</td>
					</tr> -->
					<tr class="border divide-x h-20 text-sm">
						<td class="w-1/12 text-center p-2 bg-gray-100">3.</td>
						<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.card_id_representative") }}</td>
						<td class="w-5/12 p-2 text-center">
							<span class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(form.juristic.juristic_document.card_id_representative.src)">{{ form.juristic.juristic_document.card_id_representative.name }}</span>
						</td>
					</tr>
					<!-- <tr class="border divide-x h-20 text-sm">
						<td class="w-1/12 text-center p-2 bg-gray-100">5.</td>
						<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.employment_certificate") }}</td>
						<td class="w-5/12 p-2 text-center">
							<span class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(form.juristic.juristic_document.employment_certificate.src)">{{ form.juristic.juristic_document.verified.name }}</span>
						</td>
					</tr> -->
				</table>
				<PDFModal v-if="pdfModal" @close="pdfModal = false" :pdfURL="pdfURL" />
			</div>

			<div class="col-span-4 my-4"></div>
			<div class="col-span-4 flex flex-col items-center text-sm gap-5">
				<button @click="$emit('click')" class="w-80 bg-tgo-teal-500 border shadow-md rounded text-center py-2 text-white">{{ $t("button.submit") }}</button>
				<button @click="$emit('back')">{{ $t("button.back") }}</button>
				<button @click="$emit('cancel')">{{ $t("button.cancel") }}</button>
			</div>

			<div class="col-span-4"></div>
		</div>
	</div>
</template>

<script>
export default {
	props: ["form"],
	data() {
		return {
			dropzoneOptions: {
				url: process.env.baseUrl + "/api/v1/form/upload",
				disablePreviews: true,
				previewsContainer: false,
				parallelUploads: 10,
				maxFiles: 10,
				acceptedFiles: "image/png,image/jpeg,application/pdf",
			},
			dropdowns: {
				provinces: [],
				district: [],
				subdistrict: [],
			},
			isSubmitted: false,
			pdfModal: false,
		};
	},

	async mounted() {
		await this.getProvince();
		await this.getDistrict();
		await this.getSubdistrict();
	},
	methods: {
		openPDF(src) {
			this.pdfURL = process.env.baseUrl + src;
			this.pdfModal = true;
		},

		async getProvince() {
			const app = this;
			this.dropdowns.provinces = await this.$axios
				.$get(`/api/v1/dropdown/provinces`)
				.then((resp) => resp)
				.catch((err) => {
					console.log(err);
				});
		},
		async getDistrict() {
			const app = this;
			// console.log("province");

			this.dropdowns.district = await this.$axios
				.$get(`/api/v1/dropdown/district?province=${this.form.juristic.province}`)
				.then((resp) => resp)
				.catch((err) => {
					console.log(err);
				});
		},
		async getSubdistrict() {
			const app = this;

			this.dropdowns.subdistrict = await this.$axios
				.$get(`/api/v1/dropdown/subdistrict?province=${this.form.juristic.province}&district=${this.form.juristic.district}`)
				.then((resp) => resp)
				.catch((err) => {
					console.log(err);
				});
		},
	},
};
</script>

<style>
</style>