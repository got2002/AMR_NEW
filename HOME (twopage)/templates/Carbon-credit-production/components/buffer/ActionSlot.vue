<template>
	<td class="border-t-0 px-1">
		<div class="flex items-center gap-2">
			<button @click="$emit('openModal', { type: 0, data: data })" class="flex items-center gap-2 bg-green-500 px-2 py-1 rounded shadow-md hover:bg-green-600 text-white">
				
				{{ $t("button.issued") }}
			</button>
			<button @click="$emit('openModal', { type: 1, data: data })" class="flex items-center gap-2 bg-status px-2 py-1 rounded shadow-md hover:bg-yellow-800 text-white">
				{{ $t("button.reversal") }}
			</button>
		</div>
	</td>
</template>

<script>
export default {
	props: ["data"],
	computed: {
		checkEndDate() {
			const endDate = this.$dayjs(this.data.project_end_date).toDate();
			const currentDate = this.$dayjs().toDate();
			return currentDate > endDate;
		},
	},
	methods: {
		reversal() {
			const app = this;
			this.$swal
				.fire({
					icon: "info",
					iconColor: "#C14D0C",
					iconHtml: `
									<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
										<path stroke-linecap="round" stroke-linejoin="round" d="M10.125 2.25h-4.5c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125v-9M10.125 2.25h.375a9 9 0 019 9v.375M10.125 2.25A3.375 3.375 0 0113.5 5.625v1.5c0 .621.504 1.125 1.125 1.125h1.5a3.375 3.375 0 013.375 3.375M9 15l2.25 2.25L15 12" />
									</svg>
									`,
					title: this.$t("alert.title.warning"),
					// text: this.$t("alert.text.warning.default"),
					showCancelButton: true,

					confirmButtonColor: "#C14D0C",
					confirmButtonText: this.$t("button.confirm"),
					cancelButtonText: this.$t("button.cancel"),
					reverseButtons: true,

					input: "text",
					inputLabel: app.$t("sweetalert.buffer.input.label"),

					inputPlaceholder: app.$t("sweetalert.buffer.input.placeholder"),
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
							.$post(`/api/v1/buffercarbons/reversal_retirement/${app.data._id}`, {
								remark: result.value,
							})
							.then((resp) => {
								// console.log(resp);

								// app.form = resp;
								app.$swal.close();
								app.$swal
									.fire({
										icon: "success",
										iconColor: "#10b981",
										title: this.$t("alert.title.success.default"),
										timer: 2000,
										timerProgressBar: true,
									})
									.then(() => {
										app.$emit("reload");
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
