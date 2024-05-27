<template>
	<div class="w-full pt-4">
		<div class="">
			<p class="text-green-600 text-lg">{{ $t("openAccount.form.title") }}</p>
			<p class="text-sm">{{ $t("openAccount.form.government.subtitle") }}</p>
		</div>
		<div class="border-t my-4"></div>

		<div class="grid grid-cols-4 gap-4">
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.government.name')" />
				<UIShowInput :value="form.government.government_name" />
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.phone_number')" />
				<UIShowInput :value="form.government.phone_number" />
			</div>
			<div class="col-span-4">
				<UILabel :text="$t('openAccount.form.government.address')" />
				<UIShowInput :value="form.government.address" />
			</div>

			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.province')" />
				<UIShowInput :value="form.government.province" />
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.district')" />
				<UIShowInput :value="form.government.district"  />
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.subdistrict')" />
				<UIShowInput :value="form.government.subdistrict"/>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.postcode')" />
				<UIShowInput :value="form.government.postcode" />
			</div>

			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.email')" />
				<UIShowInput :value="form.government.email" />
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.password')" />
				<UIPasswordInput :disable="true" :value="form.government.password" />
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.passwordConfirmation')" />
				<UIPasswordInput :disable="true" :value="form.government.passwordConfirmation" />
			</div>
			<div class="col-span-4"></div>
			<div class="col-span-4 border-t"></div>
			<div class="col-span-4"></div>

			<div class="col-span-4">
				<p class="text-base underline">{{ $t("openAccount.form.juristic.grantee_info.title") }}</p>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.firstname')" />
				<UIShowInput :value="form.government.firstname" />
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.lastname')" />
				<UIShowInput :value="form.government.lastname" />
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.card_id')" />
				<UIShowInput :value="form.government.card_id" />
			</div>

			<div class="col-span-4"></div>
			<div class="col-span-4 border-t"></div>
			<div class="col-span-4"></div>
			<div class="col-span-4">
				<p class="text-base underline">{{ $t("openAccount.form.juristic.account_detail.title") }}</p>
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.accountName')" />
				<UIShowInput :value="form.government.accountName" />
			</div>

			<div class="col-span-2 space-y-3">
				<UILabel :text="$t('openAccount.form.request_permission.title')" />
				<AuthRequestPermission :form="form.government" :disable="true"/>
			</div>

			<div class="col-span-4 border-t my-2"></div>
			<div class="col-span-4">
				<p class="text-base underline">{{ $t("openAccount.showDocument.title") }}</p>
			</div>

			<div class="col-span-4">
				<table class="border w-full">
				<tr class="border divide-x h-20 text-sm">
						<td class="w-1/12 text-center p-2 bg-gray-100">1.</td>
						<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.verified1") }}</td>
						<td class="w-5/12 p-2 text-center">
							<span class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(form.government.government_document.verified.src)">{{ form.government.government_document.verified.name }}</span>
						</td>
					</tr>
					<tr class="border divide-x h-20 text-sm">
						<td class="w-1/12 text-center p-2 bg-gray-100">2.</td>
						<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.authorize") }}</td>
						<td class="w-5/12 p-2 text-center">
							<span class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(form.government.government_document.authorize.src)">{{ form.government.government_document.authorize.name }}</span>
						</td>
					</tr>
					<!-- <tr class="border divide-x h-20 text-sm">
						<td class="w-1/12 text-center p-2 bg-gray-100">3.</td>
						<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.card_id_owner") }}</td>
						<td class="w-5/12 p-2 text-center">
							<span class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(form.government.government_document.card_id_owner.src)">{{ form.government.government_document.card_id_owner.name }}</span>
						</td>
					</tr> -->
					<tr class="border divide-x h-20 text-sm">
						<td class="w-1/12 text-center p-2 bg-gray-100">3.</td>
						<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.card_id_representative") }}</td>
						<td class="w-5/12 p-2 text-center">
							<span class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(form.government.government_document.card_id_representative.src)">{{ form.government.government_document.card_id_representative.name }}</span>
						</td>
					</tr>
					
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
			idOption: "idcard",
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
		next_step() {
			this.isSubmitted = true;
			this.$v.$touch();
			if (this.$v.$invalid) {
				this.$swal.fire({
					icon: "error",
					iconColor: "#ef4444",
					confirmButtonColor: "#ef4444",
					title: this.$t("sweetalert.complete_information"),
					text: this.$t("sweetalert.complete_information_text"),
				});

				return 0;
			}
			this.$emit("click");
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
				.$get(`/api/v1/dropdown/district?province=${this.form.government.province}`)
				.then((resp) => resp)
				.catch((err) => {
					console.log(err);
				});
		},
		async getSubdistrict() {
			const app = this;
			
			this.dropdowns.subdistrict = await this.$axios
				.$get(`/api/v1/dropdown/subdistrict?province=${this.form.government.province}&district=${this.form.government.district}`)
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