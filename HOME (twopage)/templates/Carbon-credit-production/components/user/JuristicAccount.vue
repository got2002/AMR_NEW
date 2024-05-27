<template>
	<div class="w-full pt-4">
		<!-- <div class="">
			<p class="text-green-600 text-lg">{{ $t("openAccount.form.title") }}</p>
			<p class="text-sm">{{ $t("openAccount.form.juristic.subtitle") }}</p>
		</div>
		<div class="border-t my-4"></div> -->

		<div class="grid grid-cols-4 gap-4">
			<div class="col-span-4 text-base font-bold border-b-2">
				<p class="uppercase">{{ $t("user.view.form.part", { number: 1 }) }}: {{ $t("user.view.form.profile_title") }}</p>
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.juristic.name')" />
				<UIShowInput :value="form.company?.companyName" />
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.phone_number')" />
				<UIShowInput :value="form.phone_number" />
			</div>
			<div class="col-span-4">
				<UILabel :text="$t('openAccount.form.juristic.address')" />
				<UIShowInput :value="form.address" />
			</div>

			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.province')" />
				<UIShowInput :value="form.province" />
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.district')" />
				<UIShowInput :value="form.district" />
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.subdistrict')" />
				<UIShowInput :value="form.subdistrict" />
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.postcode')" />
				<UIShowInput :value="form.postcode" />
			</div>

			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.juristic.number')" :required="false" />
				<UIShowInput :value="form.company?.juristicNumber" />
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.juristic.alien_id')" :required="false" />
				<UIShowInput :value="form.company?.alienNumber" />
			</div>

			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.email')" />
				<UIShowInput :value="form.email" />
			</div>

			<div class="col-span-4"></div>
			<div class="col-span-4 border-t border-dashed"></div>
			<div class="col-span-4"></div>

			<div class="col-span-4">
				<p class="text-base underline">{{ $t("openAccount.form.juristic.grantee_info.title") }}</p>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.firstname')" />
				<UIShowInput :value="form.firstname" />
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.lastname')" />
				<UIShowInput :value="form.lastname" />
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.card_id')" />
				<UIShowInput :value="form.card_id" />
			</div>

			<div class="col-span-4"></div>
			<div class="col-span-4"></div>
			<div class="col-span-4 text-base font-bold border-b-2">
				<p class="uppercase">{{ $t("user.view.form.part", { number: 2 }) }}: {{ $t("user.view.form.account_title") }}</p>
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.accountName')" />
				<UIShowInput :value="form.account?.accountName" />
			</div>

			<div class="col-span-2 space-y-3">
				<UILabel :text="$t('openAccount.form.request_permission.title')" />
				<AuthRequestPermission :form="form" :disable="true" />
			</div>

			<div class="col-span-4"></div>
			<div class="col-span-4 text-base font-bold border-b-2">
				<p class="uppercase">{{ $t("user.view.form.part", { number: 3 }) }}: {{ $t("user.view.form.document") }}</p>
			</div>

			<div class="col-span-4">
				<table class="border w-full">
					<tr class="border divide-x h-20 text-sm">
						<td class="w-1/12 text-center p-2 bg-gray-100">1.</td>
						<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.verified") }}</td>
						<td class="w-5/12 p-2 text-center">
							<span class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(form.company.document?.verified.src)">{{ form.company.document?.verified.name }}</span>
						</td>
					</tr>
					<tr class="border divide-x h-20 text-sm">
						<td class="w-1/12 text-center p-2 bg-gray-100">2.</td>
						<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.authorize") }}</td>
						<td class="w-5/12 p-2 text-center">
							<span class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(form.company.document?.authorize.src)">{{ form.company.document?.authorize.name }}</span>
						</td>
					</tr>
					<!-- <tr class="border divide-x h-20 text-sm">
						<td class="w-1/12 text-center p-2 bg-gray-100">3.</td>
						<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.card_id_owner") }}</td>
						<td class="w-5/12 p-2 text-center">
							<span class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(form.company.document?.card_id_owner.src)">{{ form.company.document?.card_id_owner.name }}</span>
						</td>
					</tr> -->
					<tr class="border divide-x h-20 text-sm">
						<td class="w-1/12 text-center p-2 bg-gray-100">3.</td>
						<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.card_id_representative") }}</td>
						<td class="w-5/12 p-2 text-center">
							<span class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(form.company.document?.card_id_representative.src)">{{ form.company.document?.card_id_representative.name }}</span>
						</td>
					</tr>
					<!-- <tr class="border divide-x h-20 text-sm">
						<td class="w-1/12 text-center p-2 bg-gray-100">5.</td>
						<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.employment_certificate") }}</td>
						<td class="w-5/12 p-2 text-center">
							<span class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(form.company.document?.employment_certificate.src)">{{ form.company.document?.employment_certificate.name }}</span>
						</td>
					</tr> -->
				</table>
				<PDFModal v-if="pdfModal" @close="pdfModal = false" :pdfURL="pdfURL" />
				<client-only placeholder="loading...">
					<EasyLightBox :imgs="imgSrc" :visible="visible" :index="index" @hide="visible = false"> </EasyLightBox>
				</client-only>
			</div>
		</div>
	</div>
</template>

<script>
import EasyLightBox from "vue-easy-lightbox";
export default {
	props: ["form"],
	components: {
		EasyLightBox,
	},
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
			visible: false,
			index: 0,
			imgSrc:''
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
			this.imgSrc = process.env.baseUrl + src;
			if (/(.png|.jpg|.jpeg)/.test(src)) {
				this.visible = true;
			} else {
				this.pdfModal = true;
			}
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
				.$get(`/api/v1/dropdown/district?province=${this.form.province}`)
				.then((resp) => resp)
				.catch((err) => {
					console.log(err);
				});
		},
		async getSubdistrict() {
			const app = this;

			this.dropdowns.subdistrict = await this.$axios
				.$get(`/api/v1/dropdown/subdistrict?province=${this.form.province}&district=${this.form.district}`)
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