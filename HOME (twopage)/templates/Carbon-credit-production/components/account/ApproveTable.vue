<template>
	<div class="w-full grid grid-cols-1 xl:grid-cols-1 2xl:grid-cols-1 2xl:overflow-hidden overflow-x-scroll shadow-sm rounded">
		<table class="items-center w-full space-y-6 shadow-sm rounded-sm">
			<thead>
				<tr>
					<template v-for="(item, idx) in head">
						<ApiHeadSlotDark :text="item.name" :key="idx" :align="item.align" />
					</template>
				</tr>
			</thead>
			<tbody class="bg-white">
				<template v-for="(data, index) in tData">
					<tr :key="index" :class="{ 'shadow-sm': drop == index }" class="border-t text-xs h-12 rounded hover:bg-theme-green-100 align-middle">
						<AccountTDSlot :text="data.desAccountNumber" align="center" />
						<AccountTDSlot :text="data.accountName" align="center" />
						<AccountTDSlot :text="accountTypeText(data.account_type)" align="center" />

						<AccountTDSlot :text="datetime(data.createdAt)" align="center" />
						<AccountTDSlot text="" align="center">
							<div class="flex items-center justify-center gap-2">
								<button @click="approve(1, data._id)" class="bg-green-500 rounded px-2 py-1 shadow-sm text-white text-xs">{{ $t("button.approve") }}</button>
								<button @click="approve(2, data._id)" class="bg-red-500 rounded px-2 py-1 shadow-sm text-white text-xs">{{ $t("button.reject") }}</button>

								<button v-if="drop != index" @click="drop = index" class="bg-blue-500 rounded px-2 py-1 shadow-sm text-white text-xs">{{ $t("button.expand_document") }}</button>
								<button v-if="drop == index" @click="drop = null" class="bg-blue-500 rounded px-2 py-1 shadow-sm text-white text-xs">{{ $t("button.close") }}</button>
							</div>
						</AccountTDSlot>
					</tr>
					<tr :key="index + 'children'" v-if="drop == index">
						<td colspan="5" class="border-l-4 border-tgo-teal-500">
							<div class="w-full flex justify-center p-4">
								<table class="border w-full" v-if="data.account_type == 0">
									<tr class="border divide-x h-20 text-sm">
										<td class="w-1/12 text-center p-2 bg-gray-100">1.</td>
										<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.card_id") }}</td>
										<td class="w-5/12 p-2 text-center">
											<span v-if="checkfile(data.documents.src) === 'pdf'" class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(data.documents.src)">{{ data.documents.name }}</span>
											<span v-else class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="showImage(data.documents.src)">{{ data.documents.name }}</span>
										</td>
									</tr>
								</table>

								<table class="border w-full" v-if="data.account_type == 1">
									<tr class="border divide-x h-20 text-sm">
										<td class="w-1/12 text-center p-2 bg-gray-100">1.</td>
										<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.verified") }}</td>
										<td class="w-5/12 p-2 text-center">
											<span v-if="checkfile(data.documents.verified.src) === 'pdf'" class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(data.documents.verified.src)">{{ data.documents.verified.name }}</span>
											<span v-else class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="showImage(data.documents.verified.src)">{{ data.documents.verified.name }}</span>
										</td>
									</tr>
									<tr class="border divide-x h-20 text-sm">
										<td class="w-1/12 text-center p-2 bg-gray-100">2.</td>
										<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.authorize") }}</td>
										<td class="w-5/12 p-2 text-center">
											<span v-if="checkfile(data.documents.authorize.src) === 'pdf'" class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(data.documents.authorize.src)">{{ data.documents.authorize.name }}</span>
											<span v-else class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="showImage(data.documents.authorize.src)">{{ data.documents.authorize.name }}</span>
										</td>
									</tr>
									<tr class="border divide-x h-20 text-sm">
										<td class="w-1/12 text-center p-2 bg-gray-100">3.</td>
										<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.card_id_owner") }}</td>
										<td class="w-5/12 p-2 text-center">
											<span v-if="checkfile(data.documents.card_id_owner.src) === 'pdf'" class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(data.documents.card_id_owner.src)">{{ data.documents.card_id_owner.name }}</span>
											<span v-else class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="showImage(data.documents.card_id_owner.src)">{{ data.documents.card_id_owner.name }}</span>
										</td>
									</tr>
									<tr class="border divide-x h-20 text-sm">
										<td class="w-1/12 text-center p-2 bg-gray-100">4.</td>
										<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.card_id_representative") }}</td>
										<td class="w-5/12 p-2 text-center">
											<span v-if="checkfile(data.documents.card_id_representative.src) === 'pdf'" class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(data.documents.card_id_representative.src)">{{ data.documents.card_id_representative.name }}</span>
											<span v-else class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="showImage(data.documents.card_id_representative.src)">{{ data.documents.card_id_representative.name }}</span>
										</td>
									</tr>
									<tr class="border divide-x h-20 text-sm">
										<td class="w-1/12 text-center p-2 bg-gray-100">5.</td>
										<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.employment_certificate") }}</td>
										<td class="w-5/12 p-2 text-center">
											<span v-if="checkfile(data.documents.employment_certificate.src) === 'pdf'" class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(data.documents.employment_certificate.src)">{{ data.documents.employment_certificate.name }}</span>
											<span v-else class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="showImage(data.documents.employment_certificate.src)">{{ data.documents.employment_certificate.name }}</span>
										</td>
									</tr>
								</table>

								<table class="border w-full" v-if="data.account_type == 2">
									<tr class="border divide-x h-20 text-sm">
										<td class="w-1/12 text-center p-2 bg-gray-100">1.</td>
										<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.verified1") }}</td>
										<td class="w-5/12 p-2 text-center">
											<span v-if="checkfile(data.documents.verified.src) === 'pdf'" class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(data.documents.verified.src)">{{ data.documents.verified.name }}</span>
											<span v-else class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="showImage(data.documents.verified.src)">{{ data.documents.verified.name }}</span>
										</td>
									</tr>
									<tr class="border divide-x h-20 text-sm">
										<td class="w-1/12 text-center p-2 bg-gray-100">2.</td>
										<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.authorize") }}</td>
										<td class="w-5/12 p-2 text-center">
											<span v-if="checkfile(data.documents.authorize.src) === 'pdf'" class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(data.documents.authorize.src)">{{ data.documents.authorize.name }}</span>
											<span v-else class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="showImage(data.documents.authorize.src)">{{ data.documents.authorize.name }}</span>
										</td>
									</tr>
									<tr class="border divide-x h-20 text-sm">
										<td class="w-1/12 text-center p-2 bg-gray-100">3.</td>
										<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.card_id_owner") }}</td>
										<td class="w-5/12 p-2 text-center">
											<span v-if="checkfile(data.documents.card_id_owner.src) === 'pdf'" class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(data.documents.card_id_owner.src)">{{ data.documents.card_id_owner.name }}</span>
											<span v-else class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="showImage(data.documents.card_id_owner.src)">{{ data.documents.card_id_owner.name }}</span>
										</td>
									</tr>
									<tr class="border divide-x h-20 text-sm">
										<td class="w-1/12 text-center p-2 bg-gray-100">4.</td>
										<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.card_id_representative") }}</td>
										<td class="w-5/12 p-2 text-center">
											<span v-if="checkfile(data.documents.card_id_representative.src) === 'pdf'" class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(data.documents.card_id_representative.src)">{{ data.documents.card_id_representative.name }}</span>
											<span v-else class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="showImage(data.documents.card_id_representative.src)">{{ data.documents.card_id_representative.name }}</span>
										</td>
									</tr>
								</table>
								<PDFModal v-if="pdfModal" @close="pdfModal = false" :pdfURL="pdfURL" />
								<client-only placeholder="loading...">
									<EasyLightBox :imgs="[imgURL]" :visible="visible" @hide="visible = false"> </EasyLightBox>
								</client-only>
							</div>
						</td>
					</tr>
				</template>
			</tbody>
		</table>
	</div>
</template>

<script>
import EasyLightBox from "vue-easy-lightbox";
export default {
	props: {
		tData: {
			type: Array,
			require: true,
		},
	},
	components: {
	
		EasyLightBox,
	},
	data() {
		return {
			drop: null,
			pdfURL: "",
			pdfModal: false,
			imgURL: "",
			visible: false,
			head: [
				{
					name: this.$t("account.table.header.account_id"),
					align: "center",
					filterable: false,
				},
				{
					name: this.$t("account.table.header.name"),
					align: "center",
					filterable: false,
				},
				{
					name: this.$t("account.table.header.accountType"),
					align: "center",
					filterable: false,
				},

				{
					name: this.$t("account.table.header.createAt"),
					align: "center",
					filterable: false,
				},
				{
					name: this.$t("account.table.header.tool"),
					align: "center",
					filterable: false,
				},
			],
		};
	},
	computed: {
		// fullName() {
		// 	return `${this.loggedInUser.firstname} ${this.loggedInUser.lastname}`;
		// },
	},
	mounted() {
		// console.log(this.loggedInUser, this.isAuthenticated)
	},
	methods: {
		accountTypeText(val) {
			switch (val) {
				case 0:
					return this.$t("account.accountType.guest");
				case 1:
					return this.$t("account.accountType.juristic");
				case 2:
					return this.$t("account.accountType.government");
			}
		},
		checkfile(filename) {
			let parts = filename.split(".");
			parts = parts[parts.length - 1];
			return parts.toLowerCase();
		},
		showImage(src) {
			this.imgURL = process.env.baseUrl + src;
			this.visible = true;
		},
		openPDF(src) {
			this.pdfURL = process.env.baseUrl + src;
			this.pdfModal = true;
		},
		dateLocale(date) {
			if (this.$i18n.locale === "th") {
				return this.$dayjs(date).locale("th").format("DD MMM BBBB");
			}
			return this.$dayjs(date).locale("en").format("DD MMM YYYY");
		},
		datetime(date) {
			if (this.$i18n.locale === "th") {
				return this.$dayjs(date).locale("th").format("DD MMM BBBB (HH:mm)");
			}
			return this.$dayjs(date).locale("en").format("DD MMM YYYY (HH:mm)");
		},

		approve(approveValue, accountId) {
			const app = this;
			this.$swal
				.fire({
					icon: "info",
					iconColor: approveValue === 1 ? "#10b981" : "#ef4444",
					iconHtml:
						approveValue === 1
							? `
									<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
										<path stroke-linecap="round" stroke-linejoin="round" d="M10.125 2.25h-4.5c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125v-9M10.125 2.25h.375a9 9 0 019 9v.375M10.125 2.25A3.375 3.375 0 0113.5 5.625v1.5c0 .621.504 1.125 1.125 1.125h1.5a3.375 3.375 0 013.375 3.375M9 15l2.25 2.25L15 12" />
									</svg>
									`
							: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
										<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m6.75 12H9m1.5-12H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
									</svg>
									`,
					title: this.$t("alert.title.warning"),
					// text: this.$t("alert.text.warning.default"),
					showCancelButton: true,

					confirmButtonColor: approveValue === 1 ? "#10b981" : "#ef4444",
					confirmButtonText: this.$t("button.confirm"),
					cancelButtonText: this.$t("button.cancel"),
					reverseButtons: true,

					input: "text",
					inputLabel: approveValue === 1 ? app.$t("sweetalert.account.input.label1") : app.$t("sweetalert.account.input.label2"),

					inputPlaceholder: app.$t("sweetalert.account.input.placeholder"),
					inputValidator: (value) => {
						if (!value && approveValue === 2) {
							return app.$t("sweetalert.account.input.error_msg");
						}
					},
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
							.$post(`/api/v1/account/approval/${accountId}`, {
								status: approveValue,
								remark: result.value,
							})
							.then((resp) => {
								// console.log(resp);

								// app.form = resp;
								app.$swal.close();
								app.$swal
									.fire({
										icon: "success",
										iconColor: "#059669",
										title: this.$t("alert.title.success.default"),
										timer: 2000,
										timerProgressBar: true,
									})
									.then(() => {
										if (approveValue === 1) app.$router.push(app.localePath(`/accounts/${accountId}`));
										else app.$emit("reload");
									});
							})
							.catch((err) => {
								app.$swal.fire({
									icon: "error",
									title: this.$t("alert.title.error.default"),
								});
								console.log(err);
							});
					}
				});
		},
	},
};
</script>