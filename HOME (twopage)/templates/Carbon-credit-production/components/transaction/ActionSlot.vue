<template>
	<td class="border-t-0 px-4 w-1/12">
		<div v-if="status === 0" class="flex items-center gap-2">
			<button @click="approve(1)" :disabled="loading" :class="{'bg-gray-400':loading,'bg-green-500 hover:bg-green-600':!loading}" class="w-20 text-center py-1 text-white rounded shadow-sm text-xs">{{ $t("button.approve") }}</button>
			<button @click="approve(2)" :disabled="loading" :class="{'bg-gray-400':loading,'bg-red-500 hover:bg-red-600':!loading}" class="w-20 text-center py-1 text-white rounded shadow-sm text-xs">{{ $t("button.reject") }}</button>
		</div>
		<div v-else-if="canCertified" class="flex items-center justify-center gap-2">
			<a target="_blank" :href="transactionDetailURL" :class="{'bg-gray-400':loading,'bg-blue-500 hover:bg-blue-600':!loading}" class="w-20 text-center py-1 text-white rounded shadow-sm text-xs">{{ $t("button.see") }}</a>
		</div>
	</td>
</template>

<script>
	export default {
		props: ["id", "status","loading", "encryptID", "transferTypeID"],
		computed: {
			transactionDetailURL() {
				const id = this.encryptID;
				return `/transactions/${id}/document`;
			},
			canCertified() {
				console.log(this.transferTypeID)
				return this.status === 2 && [1000,400, 410].includes(this.transferTypeID);
			}
		},
		methods: {
			confirmOption(approveValue) {
				if (approveValue === 1) {
					return {
						icon: "info",
						iconColor: "#10b981",
						iconHtml: `
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
									<path stroke-linecap="round" stroke-linejoin="round" d="M10.125 2.25h-4.5c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125v-9M10.125 2.25h.375a9 9 0 019 9v.375M10.125 2.25A3.375 3.375 0 0113.5 5.625v1.5c0 .621.504 1.125 1.125 1.125h1.5a3.375 3.375 0 013.375 3.375M9 15l2.25 2.25L15 12" />
								</svg>`,
						title: this.$t("sweetalert.transaction.approval.title.confirm_approve"),
						text: this.$t("sweetalert.transaction.approval.text.confirm_approve"),
						showCancelButton: true,
						reverseButtons: true,

						confirmButtonColor: "#10b981",
						confirmButtonText: this.$t("button.confirm"),
						cancelButtonText: this.$t("button.cancel"),

						input: "text",
						inputLabel: this.$t("sweetalert.transaction.approval.input.label1"),

						inputPlaceholder: this.$t("sweetalert.transaction.approval.input.placeholder"),
					};
				} else {
					return {
						icon: "info",
						iconColor: "#ef4444",
						iconHtml: `
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
									<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m6.75 12H9m1.5-12H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
								</svg>`,
						title: this.$t("sweetalert.transaction.approval.title.confirm_reject"),
						text: this.$t("sweetalert.transaction.approval.text.confirm_reject"),
						showCancelButton: true,
						reverseButtons: true,

						confirmButtonColor: "#ef4444",
						confirmButtonText: this.$t("button.confirm"),
						cancelButtonText: this.$t("button.cancel"),

						input: "text",
						inputLabel: this.$t("sweetalert.transaction.approval.input.label2"),
						inputPlaceholder: this.$t("sweetalert.transaction.approval.input.placeholder"),
						inputValidator: (value) => {
							if (!value) {
								return this.$t("sweetalert.transaction.approval.input.error_msg");
							}
						},
					};
				}
			},
			approve(approveValue) {
				const app = this;
				this.$swal.fire(this.confirmOption(approveValue)).then((result) => {
					// console.log(result);
					if (result.isConfirmed) {
						app.$swal.fire({
							title: this.$t("sweetalert.waiting"),
							text: this.$t("saving"),
							allowOutsideClick: false,
							showCloseButton: false,
						});
						app.$swal.showLoading();
						app.$axios
							.$post(`/api/v1/transaction/${this.id}/approval`, {
								status: approveValue,
								remark: result.value,
							})
							.then((resp) => {
								app.$swal.close();
								// console.log(resp);

								// app.form = resp;
								app.$swal
									.fire({
										icon: "success",
										iconColor:'#059669',
										confirmButtonColor: "#059669",
										title: approveValue === 1 ? this.$t("sweetalert.transaction.approval.title.success_approve") : this.$t("sweetalert.transaction.approval.title.success_reject"),
										timer: 2000,
										timerProgressBar: true,
									})
									.then(() => {
										app.$emit("reload");
									});
							})
							.catch((err) => {
								app.$swal.close();
								app.$swal.fire({
									icon: "error",
									title: approveValue === 1 ? this.$t("sweetalert.transaction.approval.title.error_approve") : this.$t("sweetalert.transaction.approval.title.error_reject"),
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
