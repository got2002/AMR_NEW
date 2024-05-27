<template>
	<div class="w-full pt-4">
		<div class="">
			<p class="text-green-600 text-lg">{{ $t("openAccount.form.title") }}</p>
			<p class="text-sm">{{ $t("openAccount.form.guest.subtitle") }}</p>
		</div>
		<div class="border-t my-4"></div>

		<div class="grid grid-cols-4 gap-4">
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.firstname')" />
				<UIShowInput :value="form.guest.firstname" />
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.lastname')" />
				<UIShowInput :value="form.guest.lastname" />
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.card_id')" />

				<UIShowInput :value="form.guest.card_id" />
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.issued_by')" :required="false" />
				<UIShowInput :value="form.guest.issued_by" />
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.phone_number')" />
				<UIShowInput :value="form.guest.phone_number" />
			</div>

			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.address')" />
				<UIShowInput :value="form.guest.address" />
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.province')" />
				<UIShowInput v-model="form.guest.province" />
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.district')" />
				<UIShowInput v-model="form.guest.district" />
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.subdistrict')" />
				<UIShowInput v-model="form.guest.subdistrict" />
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.postcode')" />
				<UIShowInput :value="form.guest.postcode" />
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.email')" />
				<UIShowInput :value="form.guest.email" />
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.password')" />
				<UIPasswordInput :disable="true" v-model="form.guest.password" />
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.passwordConfirmation')" />
				<UIPasswordInput :disable="true" v-model="form.guest.passwordConfirmation" />
			</div>
			<div class="col-span-4"></div>
			<div class="col-span-4 border-t"></div>
			<div class="col-span-4"></div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.accountName')" />
				<UIShowInput :value="form.guest.accountName" />
			</div>

			<div class="col-span-2 space-y-3">
				<UILabel :text="$t('openAccount.form.request_permission.title')" />
				<AuthRequestPermission :form="form.guest" :disable="true"/>
			</div>

			<div class="col-span-4 border-t my-2"></div>
			<div class="col-span-4">
				<p class="text-base underline">{{ $t("openAccount.showDocument.title") }}</p>
			</div>

			<div class="col-span-4">
				<table class="border w-full">
					<tr class="border divide-x h-20 text-sm">
						<td class="w-1/12 text-center p-2 bg-gray-100">1.</td>
						<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.card_id") }}</td>
						<td class="w-5/12 p-2 text-center">
							<span class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(form.guest.document.src)">{{ form.guest.document.name }}</span>
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
			dropdowns: {
				provinces: [],
				district: [],
				subdistrict: [],
			},
			pdfModal: false,
			pdfURL: "",
		};
	},
	async mounted() {
		await this.getProvince();
		await this.getDistrict();
		await this.getSubdistrict();
	},
	methods: {
		openPDF(src) {
			console.log(this.document);
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
				.$get(`/api/v1/dropdown/district?province=${this.form.guest.province}`)
				.then((resp) => resp)
				.catch((err) => {
					console.log(err);
				});
		},
		async getSubdistrict() {
			const app = this;

			this.dropdowns.subdistrict = await this.$axios
				.$get(`/api/v1/dropdown/subdistrict?province=${this.form.guest.province}&district=${this.form.guest.district}`)
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