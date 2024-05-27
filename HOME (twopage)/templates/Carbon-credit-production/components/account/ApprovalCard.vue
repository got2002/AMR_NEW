<template>
	<div class="col-span-1 border transition delay-75 ease-in hover:border-tgo-yellow-500 bg-white shadow-sm rounded-md space-y-3">
		<div class="flex items-center justify-between bg-gray-50 rounded-t-md py-3">
			<div class="text-xs px-2 py-1 font-semibold">{{ data.desAccountNumber }}</div>
			<div class="px-2 text-xs flex items-center gap-1 text-gray-500">
				<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
					<path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
				</svg>
				{{ dateLocale(data.createdAt) }}
			</div>
		</div>

		<div class="px-2 overflow-x-auto">
			<input disabled v-model="data.accountName" class="px-2 py-3 border w-full bg-gray-100 text-center" />
		</div>
		<div class="px-2">
			<label class="font-bold text-sm">{{ $t("account.card.attach_files", { item: data.documents.length }) }}</label>
			<div class="flex items-center whitespace-nowrap overflow-x-auto gap-2">
				<div @click="showPDF(doc.src)" v-for="(doc, idx) in data.documents" :key="idx" class="col-span-1 border cursor-pointer rounded flex items-center justify-center hover:bg-gray-50">
					<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-20 h-20">
						<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
					</svg>
				</div>
				<div v-if="data.documents.length === 0" class="h-20 col-span-4 flex items-center justify-center bg-gray-100 border w-full">
					{{ $t("no_file") }}
				</div>
			</div>
		</div>

		<PDFModal v-if="pdfModal" @close="pdfModal = false" :pdfURL="pdfURL"></PDFModal>

		<div class="flex items-cnter text-xs rounded-b-md border-t divide-x">
			<div class="w-1/2 p-3 hover:bg-green-500 hover:text-white rounded-bl-md flex items-center justify-center cursor-pointer">
				<button class="flex items-center justify-center gap-1" @click="approve(1)">
					<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
						<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
					</svg>

					{{ $t("button.approve") }}
				</button>
			</div>
			<div class="w-1/2 p-3 hover:bg-red-500 hover:text-white rounded-br-md flex items-center justify-center cursor-pointer">
				<button class="flex items-center justify-center gap-1" @click="approve(2)">
					<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
						<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
					</svg>

					{{ $t("button.reject") }}
				</button>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	props: ["data", "index"],
	data() {
		return {
			edit: false,
			pdfModal: false,
			pdfURL: "",
		};
	},
	mounted() {
		// console.log(this.loggedInUser, this.isAuthenticated)
	},
	methods: {
		showPDF(url) {
			this.pdfModal = true;
			this.pdfURL = process.env.baseUrl + url;
			// this.$swal('test')
			// window.open(url, '_blank');
		},
		dateLocale(date) {
			if (this.$i18n.locale === "th") {
				return this.$dayjs(date).locale("th").format("DD MMM BBBB");
			}
			return this.$dayjs(date).locale("en").format("DD MMM YYYY");
		},
		approve(approveValue) {
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
							.$post(`/api/v1/account/approval/${app.data._id}`, {
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
										if (approveValue === 1) app.$router.push(app.localePath(`/accounts/${app.data._id}`));
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

<style></style>
